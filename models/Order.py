from pydantic import BaseModel

class Order(BaseModel):
    """Modelo para pedidos"""
    order_id:int
    points:list[int]
    order_date:str
    order_hour:str
    status:str = "pendente"
    phone:str
    owner:str = "none"