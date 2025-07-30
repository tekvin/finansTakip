from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordRequestForm
from sqlmodel import Session, select

from models import User
from schemas import UserCreate, UserOut, Token
from auth import hash_password, verify_password, create_access_token, decode_token
from database import get_session

router = APIRouter()
security = HTTPBearer()  # Swagger'da "Bearer <token>" girebilmek için

# ✅ Kullanıcı Kaydı
@router.post("/register", response_model=UserOut)
def register(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Kullanıcı adı zaten kullanılıyor")
    hashed_pw = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_pw, role="user")
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

# ✅ Giriş ve JWT Token Alma
@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Geçersiz kullanıcı adı veya şifre")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

# ✅ Token'dan Kullanıcıyı Al
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    token = credentials.credentials
    token_data = decode_token(token)
    if not token_data or not token_data.user_id:
        raise HTTPException(status_code=401, detail="Geçersiz token")
    user = session.get(User, token_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    return user

# ✅ Giriş Yapmış Kullanıcıyı Getir
@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
