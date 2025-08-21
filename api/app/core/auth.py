from fastapi import Depends, HTTPException, Request
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from ..config import settings
from ..db import get_db
from ..models.models import User


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token: str | None = None
    # Authorization header
    auth = request.headers.get("Authorization")
    if auth and auth.lower().startswith("bearer "):
        token = auth.split(" ", 1)[1]
    # Fallback to cookie
    if not token:
        token = request.cookies.get("token")
    if not token:
        raise HTTPException(status_code=401, detail="Token manquant")
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        sub = payload.get("sub")
        if not sub:
            raise HTTPException(status_code=401, detail="Token invalide")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide")
    user = db.query(User).filter(User.id == int(sub)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Utilisateur introuvable")
    return user


