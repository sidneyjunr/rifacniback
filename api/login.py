from fastapi import APIRouter, Depends, HTTPException
from core.security import create_access_token, pwd_context,hash_password,verify_user
from repository.UserRepository import UserRepository
from models.Users import User, UserNoPassword,UserGetToken
from core.security import get_current_user
from db.connection import Connection
import logging

router = APIRouter(tags=["Login"])


# Rota de login
@router.post("/token")
async def login_for_access_token(
    form_data: UserGetToken):
    db = Connection("users")
    user_repository = UserRepository(db)

    user = user_repository.get_user_by_username(form_data.username)
    if not pwd_context.verify(form_data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")


    # Gerar o token JWT
    access_token = create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
async def register_user(user: User):
    db = Connection("users")
    user_repository = UserRepository(db)

    # Verificações quanto aos dados enviados pelo usuário
    if not verify_user(user):
        raise HTTPException(status_code=400, detail="Invalid user data")
        
    try:
        # Gerar o hash da senha
        hashed_password = hash_password(user.password)

        # Criar o novo usuário
        new_user = User(
            username=user.username,
            full_name=user.full_name,
            email=user.email,
            password=hashed_password,
        )

        # Salvar o usuário no banco de dados
        user_repository.create_user(new_user)
        
        user_no_pasword= UserNoPassword(
            username=new_user.username,
            full_name=new_user.full_name,
            email=new_user.email
        )

        return user_no_pasword
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid user data {e}")
    
@router.post("/verify_token")
def verify_token(current_user: User = Depends(get_current_user)):
    if current_user is None:
        return {"error": "Not authorized"}
    return {"message": "Token is valid"}