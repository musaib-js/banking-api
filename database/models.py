from .connection import db

class Account(db.Model):
    account_id = db.Column(db.Integer, primary_key=True)
    holder_name = db.Column(db.String(100), nullable=False)
    available_balance = db.Column(db.Float, nullable=False, default=0.0)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(100), nullable=False)
    from_account_id = db.Column(db.Integer, db.ForeignKey('account.account_id'), nullable=False)
    to_account_id = db.Column(db.Integer, db.ForeignKey('account.account_id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False) 
    status = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)