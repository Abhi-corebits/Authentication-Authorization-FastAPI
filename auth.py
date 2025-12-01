from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from fastapi import HTTPException 
from schema import Tokendata
from typing import Optional
from config import SECRET_KEY , ALGO , EXPIRES

pwd_context = CryptContext(schemes=["bcrypt"])

# Security Components

def hash_pass(org_pass:str) -> str:
    return pwd_context.hash(org_pass)

def verify_pwd(org_pass:str , hash_pass: str) -> bool:
    return pwd_context.verify(org_pass , hash_pass)

def create_access_token(data:dict , delta_expiry : Optional[timedelta] = None ):
    to_encode = data.copy()
    if delta_expiry:
            expiry = datetime.utcnow() + delta_expiry
    else:
        expiry = datetime.utcnow() + timedelta(minutes= EXPIRES)
    
    to_encode.update({"exp":expiry , "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode , SECRET_KEY , algorithm= ALGO)
    return encoded_jwt

def verify_token(token:str):
    try:
        payload = jwt.decode(token , SECRET_KEY , algorithms=[ALGO])
        email : str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=404 , detail="Email not verified")
        return Tokendata(email=email)
    except jwt.PyJWTError:
        raise HTTPException(status_code=404 , detail="Email not verified")
    


