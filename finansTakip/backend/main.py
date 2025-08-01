from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session, select

from database import engine, get_session
from models import Transaction
from schemas import TransactionCreate
from users import router as user_router, get_current_user

app = FastAPI()

# Kullanıcı rotalarını dahil et
app.include_router(user_router)

# CORS ayarları (frontend erişimi için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev sunucusu
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Veritabanı tablolarını başlat
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# 🔍 Tüm işlemleri getir (giriş yapan kullanıcıya özel)
@app.get("/transactions")
def read_transactions(
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    if current_user.role == "admin":
        # Admin tüm işlemleri görebilir
        return session.exec(select(Transaction)).all()
    # Diğer kullanıcılar yalnızca kendi işlemlerini görür
    return session.exec(
        select(Transaction).where(Transaction.user_id == current_user.id)
    ).all()

# ➕ Yeni işlem ekle
@app.post("/transactions")
def add_transaction(
    txn: TransactionCreate,
    current_user=Depends(get_current_user),
    session: Session = Depends(get_session)
):
    transaction = Transaction(**txn.dict(), user_id=current_user.id)
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction
