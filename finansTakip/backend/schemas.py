from pydantic import BaseModel
from typing import Optional

# 🔐 Kullanıcı kayıt için gelen veri
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# 🔓 Sistemde kullanıcı bilgisi dönerken kullanılan veri
class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str
    balance: float  # 💰 Bakiye bilgisi eklendi

    class Config:
        orm_mode = True

# 🔑 JWT token modeli
class Token(BaseModel):
    access_token: str
    token_type: str

# 🔍 Token çözümleme sonrası kullanılacak veri modeli
class TokenData(BaseModel):
    user_id: Optional[int] = None

# ➕ Gelir veya gider oluştururken kullanılan model
class TransactionCreate(BaseModel):
    title: str
    amount: float
    type: str  # "income" veya "expense"
    category: Optional[str] = None

# 💸 Bakiyeyi doğrudan artırma/azaltma için kullanılacak model
class BalanceUpdate(BaseModel):
    amount: float  # Pozitifse ekleme, negatifse çıkarma
