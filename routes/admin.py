from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(tags=["Admin"])


class LoginData(BaseModel):
    username: str
    password: str


@router.post("/admin/login")
async def admin_login(data: LoginData):
    stored_username = os.getenv("ADMIN_USERNAME")
    stored_hash = os.getenv("ADMIN_PASSWORD_HASH")
    admin_token = os.getenv("ADMIN_TOKEN")

    if data.username != stored_username:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    if not bcrypt.checkpw(data.password.encode(), stored_hash.encode()):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    return {"token": admin_token}
