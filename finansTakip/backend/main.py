from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session
from database import engine, get_session
from schemas import TransactionCreate
from crud import create_transaction, get_transactions, delete_transaction
from models import Transaction

app = FastAPI()

# CORS (React frontend'e izin verir)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB tabloları otomatik oluştur
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

# GET: Tüm işlemleri getir
@app.get("/transactions", response_model=list[Transaction])
def read_transactions(session: Session = Depends(get_session)):
    return get_transactions(session)

# POST: Yeni işlem ekle
@app.post("/transactions", response_model=Transaction)
def add_transaction(data: TransactionCreate, session: Session = Depends(get_session)):
    return create_transaction(session, data)

# DELETE: İşlem sil
@app.delete("/transactions/{transaction_id}")
def remove_transaction(transaction_id: int, session: Session = Depends(get_session)):
    obj = delete_transaction(session, transaction_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"message": "Transaction deleted"}
