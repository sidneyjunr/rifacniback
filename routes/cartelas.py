from fastapi import APIRouter, HTTPException
from models.Rifa import Rifa
from db.connection import Connection
from repository.RifaRepository import RifaRepository
import os
from dotenv import load_dotenv

load_dotenv()

repo_cartelas = RifaRepository(Connection("cartelas"))
router = APIRouter(tags=["Cartelas"])
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")

@router.get("/cartelas")
async def get_sealed_points_with_status():
    data = repo_cartelas.getAll()
    if len(data) == 0:
        raise HTTPException(status_code=404, detail="Cartelas não encontradas")
    return {"cartelas": data}

@router.get("/cartelas/all")
async def get_sealed_points_all_data(token:str):
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")
    data = repo_cartelas.getAllSealed()
    if len(data) == 0:
        raise HTTPException(status_code=404, detail="Cartelas não encontradas")
    return {"cartelas": data}

@router.get("/cartela/{id}")
async def get_one_point(id:int,token:str):
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")

    data = repo_cartelas.getOne(id)
    if data is None:
        raise HTTPException(status_code=404, detail="Cartela não encontrada")
    return {"cartela": data}

@router.post("/cartela/{id}")
async def sell_point(rifa:Rifa,token:str):
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")
    data = repo_cartelas.update(rifa)
    if data is None:
        raise HTTPException(status_code=404, detail="Cartela não encontrada")
    return {"cartela": data}

@router.get("/cartela/search/{phone}")
async def search_points_by_phone(phone:str):
    data = repo_cartelas.get_by_phone(phone)
    if data is None:
        raise HTTPException(status_code=404, detail="Cartela não encontrada")
    return {"cartelas": data}