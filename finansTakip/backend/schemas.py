from pydantic import BaseModel
from typing import Optional

class TransactionCreate(BaseModel):
    title: str
    amount: float
    type: str
    category: Optional[str] = None
