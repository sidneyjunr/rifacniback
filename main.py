from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from api.login import router as login_router
from routes.cartelas import router as cartelas_router
from routes.pedidos import router as pedidos_router

app = FastAPI(title="API de Rifas", description="API para gerenciamento de rifas", version="1.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir qualquer origem
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#app.include_router(login_router)
app.include_router(cartelas_router)
app.include_router(pedidos_router)
