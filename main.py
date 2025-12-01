# Excalidraw Link : https://excalidraw.com/#json=jN6htBbeqfLpaanm5y2yH,h7hTuIP0IQP0XcOKB42FhA

from fastapi import FastAPI
from database import Base, engine
from routers.auth_route import router
from routers.user_route import router2 , router3



Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Authentication & Authorization (0.4v)" ,
    summary="Secure authentication system using OAuth2 and JSON Web Tokens (JWT) via FastAPI." ,
    description= """
    This RESTful API allows user registration , login, and token generation using OAuth2 with JWT.

    It also includes Role-Based Access Control (RBAC) enabling secure access to specific endpoints based on user roles such as admin or regular user.  
    
    Security features includes password hashing, token expiration handling, and protected routes requiring valid tokens.
    """ 
)

app.include_router(router)
app.include_router(router2)
app.include_router(router3)
