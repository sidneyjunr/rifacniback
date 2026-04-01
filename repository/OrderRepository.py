from db.connection import Connection
from models.Order import Order
import logging
from datetime import datetime

class OrderRepository:
    def __init__(self, db_order: Connection, db_cartelas: Connection):
        self.db_order = db_order
        self.db_cartelas = db_cartelas

    def create(self, order: Order):
        # Apenas valida que os pontos existem e não estão vendidos
        for point in order.points:
            data = self.db_cartelas.fetch_one({"numero": point})
            if data is None:
                logging.error(f"{datetime.now()}: Cartela {point} não encontrada")
                return None
            if data["status"] == "vendido":
                logging.error(f"{datetime.now()}: O ponto {point} já foi vendido")
                return None

        # Gera order_id incremental
        ultima_order = self.db_order.fetch_last()
        if ultima_order:
            order.order_id = ultima_order["order_id"] + 1
        else:
            order.order_id = 1

        data = Order(
            order_id=order.order_id,
            points=order.points,
            order_date=order.order_date,
            order_hour=order.order_hour,
            status="pendente",
            phone=order.phone,
            owner=order.owner,
        )
        self.db_order.insert_one(data.model_dump())
        return data.model_dump()

    def getAll(self):
        data = self.db_order.fetch_all({"status": "pendente"})
        if data is None:
            return []
        return [
            Order(
                order_id=d["order_id"], points=d["points"], order_date=d["order_date"],
                order_hour=d["order_hour"], status=d["status"], phone=d["phone"], owner=d["owner"],
            )
            for d in data
        ]

    def confirm_order(self, order_id: int):
        data_mongo = self.db_order.fetch_one({"order_id": order_id})
        if data_mongo is None:
            return None

        data_order = Order(
            order_id=data_mongo["order_id"], points=data_mongo["points"],
            order_date=data_mongo["order_date"], order_hour=data_mongo["order_hour"],
            status=data_mongo["status"], phone=data_mongo["phone"], owner=data_mongo["owner"],
        )

        # Atualiza cada cartela com os dados DO PEDIDO CONFIRMADO
        for point in data_order.points:
            cartela = self.db_cartelas.fetch_one({"numero": point})
            if cartela and cartela["status"] == "vendido":
                logging.error(f"{datetime.now()}: Ponto {point} já vendido")
                return {"detail": f"Ponto {point} já foi vendido por outro pedido"}
            self.db_cartelas.update_one(
                {"numero": point},
                {
                    "status": "vendido",
                    "owner": data_order.owner,
                    "phone": data_order.phone,
                    "draw_date": data_order.order_date,
                    "draw_hour": data_order.order_hour,
                },
            )

        # Confirma este pedido
        self.db_order.update_one({"order_id": order_id}, {"status": "confirmado"})

        obj_return = self.db_order.fetch_one({"order_id": order_id})
        return Order(
            order_id=obj_return["order_id"], points=obj_return["points"],
            order_date=obj_return["order_date"], order_hour=obj_return["order_hour"],
            status=obj_return["status"], phone=obj_return["phone"], owner=obj_return["owner"],
        ).model_dump()

    def reject_order(self, order_id: int):
        data_mongo = self.db_order.fetch_one({"order_id": order_id})
        if data_mongo is None:
            return None

        # Apenas marca o pedido como rejeitado (cartela não foi tocada)
        self.db_order.update_one({"order_id": order_id}, {"status": "rejeitado"})

        obj_return = self.db_order.fetch_one({"order_id": order_id})
        return Order(
            order_id=obj_return["order_id"], points=obj_return["points"],
            order_date=obj_return["order_date"], order_hour=obj_return["order_hour"],
            status=obj_return["status"], phone=obj_return["phone"], owner=obj_return["owner"],
        ).model_dump()
