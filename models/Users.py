from pydantic import BaseModel

class Token(BaseModel):
    """Classe modelo para token de autenticação"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Modelo para token com usuário"""
    username: str | None = None
    
class User(BaseModel):
    """Modelo para usuário"""
    username: str
    full_name: str
    email: str
    password: str
    
class UserGetToken(BaseModel):
    """Modelo para autenticação de usuário que acessa uma rota"""
    username: str
    password: str

class UserNoPassword(BaseModel):
    """Modelo para usuário sem senha"""
    username: str
    full_name: str
    email: str
    
class UserInDB(BaseModel):
    """Modelo para usuário no banco de dados"""
    hashed_password: str

class Card(BaseModel):
    """Modelo para cartões"""
    id:int
    question:str
    answer:str
    category_id:int
    theme_id:int

class Category(BaseModel):
    """Modelo para categorias"""
    id:int
    category_name:str

class Theme(BaseModel):
    """Modelo para temas"""
    id:int
    theme_name:str
    category_id:int