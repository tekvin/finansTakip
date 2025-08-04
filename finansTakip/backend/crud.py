from sqlmodel import Session, select
from models import Transaction, User
from schemas import TransactionCreate

def create_transaction(db: Session, txn: TransactionCreate, current_user: User):
    if txn.amount < 0:
        raise ValueError("Tutar pozitif olmalı")

    transaction = Transaction(**txn.dict(), user_id=current_user.id)
    db.add(transaction)

    # 💸 Balance güncelleme
    user = db.get(User, current_user.id)
    if txn.type.lower() == "income":
        user.balance += txn.amount
    elif txn.type.lower() == "expense":
        if user.balance < txn.amount:
            raise ValueError("Yetersiz bakiye")
        user.balance -= txn.amount

    db.commit()
    db.refresh(transaction)
    return transaction

def get_user_transactions(db: Session, user: User):
    return db.exec(select(Transaction).where(Transaction.user_id == user.id)).all()

def delete_transaction(db: Session, transaction_id: int, current_user: User):
    txn = db.get(Transaction, transaction_id)
    if txn and txn.user_id == current_user.id:
        db.delete(txn)
        db.commit()
        return txn
    return None
