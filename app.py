from flask import Flask, jsonify, request
from database.models import Account, Transaction
from database.connection import db, transaction_scope
from datetime import datetime
import uuid

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://user:password@db:5432/banking_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


def validate_request(data, required_fields):
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return {"error": f"Missing fields: {', '.join(missing_fields)}"}
    return None


@app.route("/transactions/create", methods=["POST"])
def create_transaction():
    try:
        data = request.json

        from_account = data.get("from_account", None)
        to_account = data.get("to_account", None)
        amount = data.get("amount", None)

        required_fields = ["from_account", "to_account", "amount"]

        validation_error = validate_request(data, required_fields)

        if validation_error:
            return jsonify(validation_error), 400

        with transaction_scope() as session:
            from_account_obj = (
                session.query(Account)
                .filter_by(account_id=from_account)
                .with_for_update()
                .first()
            )
            to_account_obj = (
                session.query(Account)
                .filter_by(account_id=to_account)
                .with_for_update()
                .first()
            )

            if not from_account_obj:
                return jsonify({"error": "The account to debit from seems invalid"}), 400

            if not to_account_obj:
                return jsonify({"error": "The account to credit seems invalid"}), 400

            if from_account_obj.available_balance < amount:
                return jsonify({"error": "Insufficient funds"}), 400

            if amount <= 0:
                return jsonify({"error": "Amount should be greater than 0"}), 400

            from_account_obj.available_balance -= amount
            to_account_obj.available_balance += amount

            transaction_id = str(uuid.uuid4())

            debit_transaction = Transaction(
                transaction_id=transaction_id,
                from_account_id=from_account_obj.account_id,
                to_account_id=to_account_obj.account_id,
                amount=amount,
                transaction_type="Debit",
                status="Pending",
                timestamp=datetime.utcnow(),
            )

            credit_transaction = Transaction(
                transaction_id=transaction_id,
                from_account_id=from_account_obj.account_id,
                to_account_id=to_account_obj.account_id,
                amount=amount,
                transaction_type="Credit",
                status="Pending",
                timestamp=datetime.now(),
            )

            db.session.add(debit_transaction)
            db.session.add(credit_transaction)
            db.session.commit()
            
            debit_transaction.status = "Completed"
            credit_transaction.status = "Completed"
            
            db.session.commit()

            return (
                jsonify(
                    {
                        "message": "Transaction created successfully", 
                        "transaction_id": debit_transaction.transaction_id,
                        "from_account": from_account_obj.account_id,
                        "to_account": to_account_obj.account_id,
                        "amount": amount,
                        "status": "Pending",
                        "timestamp": debit_transaction.timestamp,
                    }
                ),
                201,
            )
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e), "message": "Oops! Something went wrong at our end. We'll fix it soon."}), 500


if __name__ == "__main__":
    with app.app_context():
        
        # Delete the existing tables if they exist
        db.drop_all()
        
        db.create_all()
        
        # Create two accounts for testing
        account1 = Account(holder_name="John Doe", available_balance=1000.0)
        account2 = Account(holder_name="Jane Smith", available_balance=500.0)
        
        db.session.add(account1)
        db.session.add(account2)
        
        db.session.commit()
        print("Database and tables created successfully.")
    app.run(host="0.0.0.0",debug=True, port=5002)