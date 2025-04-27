from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from models import User  # Import SQLAlchemy model
from database import get_db  # Database session
from hashing import Hash  # Import hashing utility
from sqlalchemy.exc import SQLAlchemyError
from token_1 import create_access_token
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()


@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    if not Hash.verify(user.hashed_password, request.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect Password")

    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}