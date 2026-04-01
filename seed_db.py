"""
Script para popular o novo MongoDB com 300 pontos disponíveis.
Execute uma vez: python seed_db.py
"""
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["rifacni"]

# Limpa coleções existentes
db.cartelas.drop()
db.orders.drop()

cartelas = [
    {
        "numero": i,
        "status": "disponivel",
        "owner": "none",
        "phone": "",
        "draw_date": "",
        "draw_hour": "",
    }
    for i in range(1, 301)
]

db.cartelas.insert_many(cartelas)
print(f"{len(cartelas)} pontos inseridos na colecao 'cartelas'")
print("Colecao 'orders' limpa e pronta")
client.close()
