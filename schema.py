from pydantic import BaseModel , Field , EmailStr  , field_validator
from typing import Optional , Annotated 
import re

# Pydantic Models 
class UserCreate(BaseModel):
    name: Annotated[str , Field(... , max_length=30)]
    email: Annotated[EmailStr , Field(... , max_length=30)]
    password : Annotated[str , Field(..., min_length= 5 , max_length=15 )]

    @field_validator("password")
    def validate_password(cls, v: str) -> str:
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*]", v):
            raise ValueError("Password must contain at least one special character (!@#$%^&*)")
        return v

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active : bool
    
    class Config:
        from_attributes = True

class Userlogin(BaseModel):
    email : str
    pwd : str

class Token(BaseModel):
    access_token : str
    token_type : str

class Tokendata(BaseModel):
    email : Optional[str] = None

