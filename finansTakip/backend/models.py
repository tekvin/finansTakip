from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    hashed_password: str
    role: str = "user"
    balance: float = 0.0  # 💰 Kullanıcının mevcut bakiyesi

    transactions: List["Transaction"] = Relationship(back_populates="owner")


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    amount: float
    type: str
    category: Optional[str]
    date: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")

    owner: Optional[User] = Relationship(back_populates="transactions")
