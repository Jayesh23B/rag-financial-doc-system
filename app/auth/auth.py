from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db import models
from app.core.security import hash_password
from app.core.security import verify_password
from app.core.jwt import create_access_token
from fastapi import HTTPException
from fastapi import Depends
from app.dependencies import get_current_user
from app.db.schemas import UserCreate


router = APIRouter(prefix="/auth", tags=["Auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from fastapi import HTTPException

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(models.User).filter(models.User.email == user.email).first()
        if existing_user:
            return {"message": "Email already exists"}

        hashed_pwd = hash_password(user.password)

        new_user = models.User(
            email=user.email,
            password=hashed_pwd,
            role_id=1
        )

        db.add(new_user)
        db.commit()

        return {"message": "User registered"}

    except Exception as e:
        print("ERROR:", e)  # 👈 IMPORTANT
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = db.query(models.User).filter(models.User.email == user.email).first()

        if not db_user:
            return {"message": "User not found"}

        # 🔍 DEBUG (just once)
        print("INPUT PASSWORD:", user.password)
        print("HASHED PASSWORD:", db_user.password)

        # ✅ VERIFY
        if not verify_password(str(user.password), db_user.password):
            return {"message": "Invalid password"}

        token = create_access_token({
            "sub": db_user.email,
            "role": db_user.role.name
        })

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    except Exception as e:
        print("LOGIN ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))