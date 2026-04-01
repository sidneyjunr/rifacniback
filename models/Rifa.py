from pydantic import BaseModel

class Rifa(BaseModel):
    """Modelo para rifas"""
    number:int
    draw_date:str
    draw_hour:str
    status:str = "disponivel"
    phone:str = "99999999999"
    owner:str = "none"

class RifaFront(BaseModel):
    number:int
    status:str

class RifaPhone(BaseModel):
    number:int
    draw_date:str