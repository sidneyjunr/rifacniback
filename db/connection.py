from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os


class Connection:
    def __init__(self,collection:str):
        """Inicializa uma instância de conexão com o banco de dados"""
        load_dotenv()  # Load environment variables from .env file

        try:
            mongo_uri = os.getenv("MONGO_URI")
            if not mongo_uri:
                raise ValueError("MONGO_URI environment variable not set")

            # Create a MongoClient instance
            self.client = MongoClient(mongo_uri, server_api=ServerApi('1'))
            db_name = os.getenv("DB_NAME", "rifacni")
            self.db = self.client[db_name]
            self.collection = self.db.get_collection(collection)
         
            print("Conexão estabelecida com o banco de dados")
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            raise
            

    '''def execute_query(self, query,params:tuple=None):
        """Executa uma intrução sql no banco de dados"""
        if not self.__client:
            print("Conexão não inicializada")  
            return
        try: 
            if not params:
                self.__client.execute(query)
                return self.__client.execute(query)
            
            return self.__client.execute(query,params)
        except Exception as e:
            print(f"Erro ao realizar query no banco de dados: {e}")
            return None'''
        
    def fetch_all(self,params = {})->list:
        """Retorna todas as linhas de uma consulta"""
        if params:
            return self.collection.find(params)
        return self.collection.find()

    def fetch_one(self,params = {})->dict:
        """Retorna a primeira linha de uma consulta"""
        if self.client:
            return self.collection.find_one(params)
        print("Nenhuma consulta foi realizada")
        return {}
    
    def update_one(self, params:dict, data:dict)->bool:
        """Atualiza um registro no banco de dados"""
        if self.client:
            return self.collection.update_one(params, {"$set":data})
        print("Nenhuma consulta foi realizada")
        return False
    
    def insert_one(self, data:dict)->bool:
        """Insere um registro no banco de dados"""
        if self.client:
            return self.collection.insert_one(data)
        print("Nenhuma consulta foi realizada")
        return False
    def fetch_last(self)->dict:
        """Retorna a última linha de uma consulta"""
        if self.client:
            return self.collection.find_one(sort=[("_id", -1)])
        print("Nenhuma consulta foi realizada")
        return {}
    
    '''def refresh(self, object)->None:
        """Recarrega um objeto do banco de dados"""
        if self.collection:
            self.collection.commit()
            print(f"Recarregando objeto {object.__class__.__name__} com id {object.id}")
            self.collection.execute(f"SELECT * FROM {object.__class__.__name__} WHERE id = ?", (object.id,))
            row = self.collection.fetchone()
            if row:
                for key in row.keys():
                    setattr(object, key, row[key])
        raise Exception("Conexão não inicializada")'''
        
        
'''    def __del__(self)->None:
        """Encerra a conexão com o banco de dados"""
        if self.client:
            print("Encerrando conexão com o banco de dados")
            self.client.close()
        raise Exception("Conexão não inicializada")
        '''
