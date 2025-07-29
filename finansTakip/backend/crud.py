from sqlalchemy.orm import Session
from models import Transaction
from schemas import TransactionCreate

def create_transaction(db: Session, transaction: TransactionCreate):
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transactions(db: Session):
    return db.query(Transaction).all()

def delete_transaction(db: Session, transaction_id: int):
    obj = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return obj
