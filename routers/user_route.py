from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import schema, models, database, dependencies , auth
from typing import List

router2 = APIRouter(tags=["User Accessible Endpoints"])
router3 = APIRouter(tags=["Admin Accessible Endpoints"])

# API Endpoints (CRUD Operations)
@router2.get("/")
def root():
    return {"message": "ABHINAV (HomePage)"}

@router2.get("/profile" , response_model=schema.UserResponse , description="Gets current logged-in user's profile")
def get_profile(current_user :models.User = Depends(dependencies.get_active_current_user)):
    return current_user

@router3.get("/users/", response_model=List[schema.UserResponse] ,description= """
    This endpoint is used to all the user info stored in the Database.

    Only user with role "admin" has the access to get the list of all users contained in the database.
    """ )
def get_users(current_user :models.User = Depends(dependencies.require_role("admin")) , db: Session = Depends(database.get_db)):
    """Get all users"""
    return db.query(models.User).all()


@router3.get("/users/{user_id}", response_model=schema.UserResponse , description= """
    This endpoint is used to get a particular user info stored in the Database.

    Only user with role "admin" has the access to get the user.
    """ )
def get_user(user_id: int, current_user :models.User = Depends(dependencies.get_active_current_user) ,db: Session = Depends(database.get_db)):
    """Get one user by ID"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="models.User not found")
    return user


@router3.post("/users/", response_model=schema.UserResponse , description= """
    This endpoint is used to create a new user in the Database.

    Only user with role "admin" has the access add the user.
    """ )
def create_new_user(user: schema.UserCreate,current_user :models.User = Depends(dependencies.require_role("admin")), db: Session = Depends(database.get_db)):
    """Create a new user"""
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashpass = auth.hash_pass(user.password)
    db_user = models.User(
        name =user.name ,
        email = user.email ,
        role = "player",
        hashed_pwd = hashpass
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router3.put("/assign-role/{user_id}" , description= """
    This endpoint is used to assign a user's role as "admin" , stored in the Database.

    Only user with role "admin" has the access to get the list of all users contained in the database.
    Every new user is assigned as "player"
    Only admin can change the role.
    """ )
def assign_role(
    user_id: int,
    role: str,
    current_user: models.User = Depends(dependencies.require_role("admin")),
    db: Session = Depends(database.get_db)
    ):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="models.User not found")

    user.role = role
    db.commit()
    return {"message": f"Role updated to {role}"}

@router3.put("/users/{user_id}", response_model=schema.UserResponse , description= """
    This endpoint is used to update user info stored in the Database.

    Only user with role "admin" has the access to update the users contained in the database.
    """ )
def update_user(
    user_id: int,
    update_user: schema.UserCreate,
    current_user :models.User = Depends(dependencies.get_active_current_user) ,
    db: Session = Depends(database.get_db)
    ):          
    """Update a user"""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="models.User not found")
    
    db_user.name = update_user.name
    db_user.email = update_user.email
    
    db.commit()
    db.refresh(db_user)
    return db_user


@router3.delete("/users/{user_id}" , description= """
    This endpoint is used to a user stored in the Database.

    Only user with role "admin" has the access to delete users contained in the database.
    """ )
def delete_user(user_id: int,current_user :models.User = Depends(dependencies.require_role("admin")) , db: Session = Depends(database.get_db)):
    """Delete a user"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="models.User not found")
    if user_id == current_user.id :
         raise HTTPException(status_code=404, detail="You  cant delete yourself")
    
    db.delete(user)
    db.commit()
    return {"message": "models.User deleted"}