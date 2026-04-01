from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.cartelas import router as cartelas_router
from routes.pedidos import router as pedidos_router
from routes.admin import router as admin_router

app = FastAPI(title="API de Rifas", description="API para gerenciamento de rifas", version="1.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir qualquer origem
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin_router)
app.include_router(cartelas_router)
app.include_router(pedidos_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
