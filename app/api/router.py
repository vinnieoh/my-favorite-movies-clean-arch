from fastapi import APIRouter



api_router = APIRouter()

api_router.include_router(usuario_route.router, prefix='/usuario', tags=['usuario'])
api_router.include_router(usuario_conteudos_route.router, prefix='/usuario-conteudos', tags=['usuario-conteudos'])
api_router.include_router(conteudos_route.router, prefix='/conteudos', tags=['conteudos'])
api_router.include_router(comentario_route.router, prefix='/comentario', tags=['comentario'])