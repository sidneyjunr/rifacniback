import dotenv
import os
dotenv.load_dotenv()
# Definir a chave secreta e o algoritmo para o JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7