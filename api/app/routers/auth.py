from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from ..db import get_db
from ..models.models import User
from ..core.security import hash_password, verify_password, create_jwt_token
from ..core.auth import get_current_user

router = APIRouter()


class RegisterIn(BaseModel):
    email: EmailStr
    password: str


@router.post("/auth/register")
def register(data: RegisterIn, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    user = User(email=str(data.email), password_hash=hash_password(data.password), plan="free")
    db.add(user)
    db.commit()
    return {"status": "ok"}


class LoginIn(BaseModel):
    email: EmailStr
    password: str


@router.post("/auth/login")
def login(data: LoginIn, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == str(data.email)).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    token = create_jwt_token(sub=str(user.id))
    response.set_cookie("token", token, httponly=True, samesite="lax")
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return {"email": user.email, "plan": user.plan}


