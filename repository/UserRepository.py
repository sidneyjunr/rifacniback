
from models.Users import User
from db.connection import Connection
import logging

class UserRepository:
    def __init__(self, db:Connection):
        self.db = db

    def get_user_by_username(self, username: str)->User:
        logging.info(f"Buscando usuário: {username} data: {self.db.fetch_one({'username':username})}")
        return self.db.fetch_one({"username":username})

    def create_user(self, user:User)->User:
        try:
            self.db.insert_one(user.model_dump())
            logging.info(f"Usuário criado com sucesso: {user}")
            return user
        except Exception as e:
            raise Exception(f"Erro ao criar usuário: {e}")
    
    def get_user_by_email(self, email: str):
        return self.db.fetch_one({"email":email})
