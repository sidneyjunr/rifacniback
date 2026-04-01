from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status,APIRouter
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic.types import Annotated
from repository.UserRepository import UserRepository
from models.Users import TokenData, User
from core.configs import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
import re
from db.connection import Connection
import logging

import shutil
from pathlib import Path


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    logging.info(f"Token: {token}")
    db = Connection("users")
    user_repository = UserRepository(db)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = user_repository.get_user_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# funcao para saber se o usuario esta ativo
async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# funcao para buscar o usuario atual


# função para criar o token de acesso
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Função de hash da senha
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_user(user:User)->bool:
    db = Connection("users")
    user_repository = UserRepository(db)

    existing_user = user_repository.get_user_by_username(user.username)
    existing_email = user_repository.get_user_by_email(user.email)
    pattern_email = r"[a-zA-Z0-9._]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    pattern_password = r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#.])[A-Za-z\d@$!%#.*?&]{8,}$"

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    if not re.match(pattern_email, user.email):
        raise HTTPException(status_code=400, detail="Invalid email")
    if not re.match(pattern_password, user.password):
        raise HTTPException(status_code=400, detail="Invalid password")
    return True
    