from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.settings.config import config
from app.settings.logs import setup_logging

# Configurar logging
#setup_logging()

app = FastAPI(title=config.PROJECT_NAME)

# Definindo a rota raiz
@app.get("/")
async def read_root():
    return {"message": "Hello World"}

# Cors Config
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Config Rotas
app.include_router(api_router, prefix=config.API_V1_STR)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level='info', reload=True)