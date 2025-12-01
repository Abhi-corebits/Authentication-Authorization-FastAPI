from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
import schema, models, auth, database
from datetime import datetime , timedelta
from config import EXPIRES

router = APIRouter(tags=["Registration"])

@router.post("/register" , response_model=schema.UserResponse ,description= """
    This endpoint is used to register a new user in the Database.

    The provided password is hashed using passlib (bcrypt) 
    Fields like name, email, password are taken & validated via Pydantic BaseModel.
    This record is stored in the User table.
    """ )  
def create_user(user: schema.UserCreate , db : Session = Depends(database.get_db)):
    does_exists = db.query(models.User).filter(models.User.email == user.email ).first()
    if does_exists:
         raise HTTPException(status_code=404 , detail="User with provided Email already exists")
    
    hashed_password = auth.hash_pass(user.password)
    push_db = models.User(
        name = user.name ,
        email = user.email ,
        role = "player" ,
        hashed_pwd = hashed_password
    )
    db.add(push_db)
    db.commit()
    db.refresh(push_db)
    return push_db

@router.post("/token" ,
           response_model=schema.Token ,
           description= """
    This endpoint is used to get the token.
    """ ,
           include_in_schema=False
)
def get_token(data: OAuth2PasswordRequestForm = Depends() , db : Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == data.username).first()
    if not user or not auth.verify_pwd( data.password , user.hashed_pwd ):
         raise HTTPException(status_code=404 , detail="Wrong Info")
    
    token_expiry = timedelta(minutes=EXPIRES)
    access_token = auth.create_access_token(data={"sub" : user.email} , delta_expiry=token_expiry)
    return {"access_token": access_token , "token_type":"bearer"}
 
