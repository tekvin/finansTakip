from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session, select
from database import engine, get_session
from models import Transaction, User
from schemas import TransactionCreate, BalanceUpdate
from users import router as user_router, get_current_user

app = FastAPI(
    title="Finans Takip API",
    version="1.0.0",
    description="Kullanıcı bazlı gelir-gider takibi ve bakiye yönetim sistemi."
)

# Routerları dahil et
app.include_router(user_router)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Veritabanı tablolarını oluştur
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# Tüm işlemleri getir
@app.get("/transactions", tags=["Transactions"])
def read_transactions(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if current_user.role == "admin":
        return session.exec(select(Transaction)).all()
    return session.exec(select(Transaction).where(Transaction.user_id == current_user.id)).all()

# Yeni işlem ekle
@app.post("/transactions", tags=["Transactions"])
def add_transaction(
    txn: TransactionCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    transaction = Transaction(**txn.dict(), user_id=current_user.id)
    session.add(transaction)

    user = session.get(User, current_user.id)
    if txn.amount < 0:
        raise HTTPException(status_code=400, detail="Tutar pozitif olmalı.")
    if txn.type.lower() == "income":
        user.balance += txn.amount
    elif txn.type.lower() == "expense":
        if user.balance < txn.amount:
            raise HTTPException(status_code=400, detail="Yetersiz bakiye.")
        user.balance -= txn.amount

    session.add(user)  # 🔧 Değişiklikleri veritabanına yansıt
    session.commit()
    session.refresh(transaction)
    return transaction

# Bakiye görüntüle
@app.get("/balance", tags=["Balance"])
def get_balance(current_user: User = Depends(get_current_user)):
    return {"balance": current_user.balance}

# Bakiye güncelle (para ekle/çıkar)
@app.post("/balance", tags=["Balance"], summary="Bakiye Güncelle (Artı/Eksi)")
def update_balance(
    data: BalanceUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    user = session.get(User, current_user.id)
    user.balance += data.amount
    if user.balance < 0:
        raise HTTPException(status_code=400, detail="Bakiye negatif olamaz.")
    session.add(user)
    session.commit()
    return {"balance": user.balance}
