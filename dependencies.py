from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models import User
from auth import verify_token

oauth2_scheme =  OAuth2PasswordBearer(tokenUrl="token")

# Aunthentication Components
def get_user(token:str = Depends(oauth2_scheme) , db : Session = Depends(get_db)):
    verified = verify_token(token)
    user = db.query(User).filter(User.email == verified.email).first()
    if user is None:
        raise HTTPException(status_code=404 , detail="User Not Found")
    return user

def get_active_current_user(current_user : User = Depends(get_user)):
    if current_user is None:
        raise HTTPException(status_code=404 , detail="User Not Found")
    return current_user

def require_role(role: str):
    def role_checker(current_user: User = Depends(get_active_current_user)):
        if current_user.role != role:
            raise HTTPException(
                status_code=403,
                detail=f"Access denied. Requires {role} role."
            )
        return current_user
    return role_checker

