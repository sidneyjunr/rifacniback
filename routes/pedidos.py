from models.Order import Order
from db.connection import Connection
from repository.OrderRepository import OrderRepository
from fastapi import APIRouter, HTTPException
import logging
import os
from dotenv import load_dotenv

load_dotenv()

pedidos = Connection("cartelas")
repo_order = OrderRepository(Connection("orders"),pedidos)
router = APIRouter(tags=["pedidos"])
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")


@router.post("/order/new_order/")
async def new_order(order:Order):
    data = repo_order.create(order)
    if data is None:
        raise HTTPException(status_code=404, detail="Erro ao criar pedido, escolha novos pontos, atualize a página e tente novamente!")
    
    return {"pedidos": data}

@router.get("/orders/")
async def get_orders(token:str):
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    data = repo_order.getAll()
    return {"pedidos": data}

@router.post("/order/confirm_order/{order_id}")
async def confirm_order(order_id:int,token:str):
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    data = repo_order.confirm_order(order_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return {"pedido": data}

@router.post("/order/reject_order/{order_id}")
async def reject_order(order_id:int,token:str):
    logging.info("comecando a rejeitar pedido: "+str(order_id))
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    data = repo_order.reject_order(order_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return {"pedido": data}