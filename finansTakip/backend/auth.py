from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from schemas import TokenData

# Güvenlik ayarları
SECRET_KEY = "supersecretkey"  # 🔒 Gerçek projede bunu .env'den çek!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Şifreleme algoritması (bcrypt önerilir)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 🔐 Şifre hashleme
def hash_password(password: str):
    return pwd_context.hash(password)

# ✅ Şifre doğrulama
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# 🎫 JWT token oluştur
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "sub": data.get("sub")})  # "sub" anahtarını tekrar ekliyoruz
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ✅ Token çözümle ve kullanıcıyı ayıkla
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            return None
        return TokenData(user_id=int(user_id))
    except JWTError:
        return None
