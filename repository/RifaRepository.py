from models.Rifa import Rifa, RifaFront,RifaPhone
from db.connection import Connection
import logging

logging.basicConfig(level=logging.INFO)
class RifaRepository:
    def __init__(self, db:Connection):
        self.db = db

    def getAll(self):
        try:
            data = self.db.fetch_all({"status": "vendido"})
            logging.info("Buscando cartelas no banco de dado ")
            logging.info("Busca finalizada")
            if data is None:
                return []
            objs = [RifaFront(number=d['numero'],status=d['status']) for d in data]
            print("Criado lista de cartelas e retornando")
            return objs
        except Exception as e:
            logging.error(f"Erro ao buscar cartelas no banco de dados: {e}")
            raise Exception("Erro ao buscar cartelas no banco de dados")

    def getAllSealed(self):
        try:
            data = self.db.fetch_all({"status": "vendido"})
            if data is None:
                return []
            objs = [Rifa(number=d['numero'],status=d['status'],draw_date=d['draw_date'],draw_hour=d['draw_hour'],phone=d['phone'],owner=d['owner']) for d in data]
            print("Buscando cartelas no banco de dados")
            return objs
        except Exception as e:
            logging.error(f"Erro ao buscar cartelas no banco de dados: {e}")
            raise Exception("Erro ao buscar cartelas no banco de dados")
        
    def getOne(self, id: int):
        try:
            data = self.db.fetch_one({"numero": id})
            if data is None:
                return None
            obj = Rifa(number=data['numero'], draw_date=data['draw_date'], draw_hour=data['draw_hour'], status=data['status'], phone=data['phone'], owner=data['owner'])
            print("Buscando uma cartela no banco de dados")
            return obj
        except Exception as e:
            logging.error(f"Erro ao buscar cartela no banco de dados: {e}")
            raise Exception(f"Erro ao buscar cartela no banco de dados: {e}")

    def update(self, rifa: Rifa):
        try:
            data = self.db.fetch_one({"numero": rifa.number})
            if data is None:
                logging.error(f"Cartela {rifa.number} não encontrada")
                return None
            
            if data['status'] == "vendido":
                print(f"O ponto: {rifa.number} já foi vendido. Escolha outro ponto")
                logging.error(f"O ponto: {rifa.number} já foi vendido. Escolha outro ponto")
                return None

            self.db.update_one({"numero": rifa.number}, rifa.model_dump())
            print("Cartela atualizada com sucesso")
            return rifa
        except Exception as e:
            logging.error(f"Erro ao atualizar cartela no banco de dados: {e}")
            raise Exception(f"Erro ao atualizar cartela no banco de dados: {e}")
        
    def get_by_phone(self, phone: str)->list:
        try:
            data = self.db.fetch_all({"phone": phone, "status": "vendido"})
            if data is None:
                raise Exception("Cartela não encontrada")
            data = [RifaPhone(number=d['numero'], draw_date=d['draw_date']) for d in data]
            return data
        except Exception as e:
            logging.error(f"Erro ao atualizar cartela no banco de dados: {e}")
            raise Exception(f"Erro ao atualizar cartela no banco de dados: {e}")
        