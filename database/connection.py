from flask_sqlalchemy import SQLAlchemy
from contextlib import contextmanager
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()

@contextmanager
def transaction_scope():
    session = db.session
    try:
        yield session
        session.commit()
    except IntegrityError:
        session.rollback()
        raise
    finally:
        session.close()
