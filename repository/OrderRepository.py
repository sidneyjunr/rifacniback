from db.connection import Connection
from models.Order import Order
import logging
from datetime import datetime

class OrderRepository:
    def __init__(self,db_order:Connection, db_cartelas:Connection):
        self.db_order = db_order
        self.db_cartelas = db_cartelas

    def create(self,order:Order):
        """
    order_id:int
    points:list
    order_date:str
    order_hour:str
    status:str = "pendente"
    phone:str
    owner:str = "none"
    """
        for point in order.points:
            data = self.db_cartelas.fetch_one({"numero":point})
            if data is None:
                logging.error(f"{datetime.now()}: Cartela {point} não encontrada")
                return None
            if data["status"] == "vendido":
                print(f"O ponto: {point} já foi vendido. Escolha outros pontos")
                logging.error(f"{datetime.now()}: O ponto: {point} já foi vendido. Escolha outros pontos")
                return None
        for point in order.points:
            print(f"Vendendo ponto: {point}")
            self.db_cartelas.update_one({"numero":point},{"status":"pendente","owner":order.owner,"phone":order.phone,"draw_date":order.order_date,"draw_hour":order.order_hour})
        print("Venda realizada com sucesso")
        ultima_order = self.db_order.fetch_last()
        
        if ultima_order:
            order.order_id = ultima_order["order_id"] + 1
        else:
            order.order_id = 1

        data = Order(order_id=order.order_id,points=order.points,order_date=order.order_date,order_hour=order.order_hour,status=order.status,phone=order.phone,owner=order.owner)
        self.db_order.insert_one(data.model_dump())
        return data.model_dump()
    
    def getAll(self):
        data = self.db_order.fetch_all({"status":"pendente"})
        if data is None:
            logging.error(f"{datetime.now()}: Nenhum pedido encontrado")
            return []
        data = [Order(order_id=d["order_id"],points=d["points"],order_date=d["order_date"],order_hour=d["order_hour"],status=d["status"],phone=d["phone"],owner=d["owner"]) for d in data]
        print(data)
        return data
    
    def confirm_order(self,order_id:int):
        data_mongo = self.db_order.fetch_one({"order_id":order_id})
        data_order = Order(order_id=data_mongo["order_id"],points=data_mongo["points"],order_date=data_mongo["order_date"],order_hour=data_mongo["order_hour"],status=data_mongo["status"],phone=data_mongo["phone"],owner=data_mongo["owner"])
        if data_order.points is None:
            logging.error(f"{datetime.now()}: Pedido {order_id} não encontrado")
            return None
        for point in data_order.points:
            print(f"Status {self.db_cartelas.fetch_one({"numero":point})["status"]}")
            if self.db_cartelas.fetch_one({"numero":point})["status"] == "vendido":
                logging.error(f"{datetime.now()}: Ponto {point} já vendido")
                return {"detail":"Ponto já vendido"}
            self.db_cartelas.update_one({"numero":point},{"status":"vendido"})
        self.db_order.update_one({"order_id":order_id},{"status":"confirmado"})
        obj_order_rejected = self.db_order.fetch_one({"order_id":order_id})
        obj_return = Order(order_id=obj_order_rejected["order_id"],points=obj_order_rejected["points"],order_date=obj_order_rejected["order_date"],order_hour=obj_order_rejected["order_hour"],status=obj_order_rejected["status"],phone=obj_order_rejected["phone"],owner=obj_order_rejected["owner"])
        logging.info(f"{datetime.now()}: Pedido {order_id} confirmado")
        return obj_return.model_dump()
    
    def reject_order(self,order_id:int):
        data_mongo = self.db_order.fetch_one({"order_id":order_id})
        obj_order = Order(order_id=data_mongo["order_id"],points=data_mongo["points"],order_date=data_mongo["order_date"],order_hour=data_mongo["order_hour"],status=data_mongo["status"],phone=data_mongo["phone"],owner=data_mongo["owner"])
        if obj_order.points is None:
            logging.error(f"{datetime.now()}: Pedido {order_id} não encontrado")
            return None
        for point in obj_order.points:
            if self.db_cartelas.fetch_one({"numero":point})["status"] == "vendido":
                logging.error(f"{datetime.now()}- Pulando cancelamento de ponto: Ponto {point} já vendido")
                continue
        
            self.db_cartelas.update_one({"numero":point},{"status":"disponivel"})
        self.db_order.update_one({"order_id":order_id},{"status":"rejeitado"})
        print("=====================")
        obj_order_rejected = self.db_order.fetch_one({"order_id":order_id})
        obj_return = Order(order_id=obj_order_rejected["order_id"],points=obj_order_rejected["points"],order_date=obj_order_rejected["order_date"],order_hour=obj_order_rejected["order_hour"],status=obj_order_rejected["status"],phone=obj_order_rejected["phone"],owner=obj_order_rejected["owner"])
        print("=====================")

        logging.info(f"{datetime.now()}: Pedido {order_id} rejeitado")
        #data_mongo = Order(order_id=data["order_id"],points=data["points"],order_date=data["order_date"],order_hour=data["order_hour"],status=data["status"],phone=data["phone"],owner=data["owner"])
        return {"pedido":obj_return.model_dump()}