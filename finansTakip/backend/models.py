from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    amount: float
    type: str  # "income" veya "expense"
    category: Optional[str] = None
    date: datetime = Field(default_factory=datetime.utcnow)
