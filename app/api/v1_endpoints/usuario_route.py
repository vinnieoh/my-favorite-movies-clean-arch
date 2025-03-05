from typing import List
from uuid import UUID

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.domain.usecases.user_usecase import UserUseCase
from app.infrastructure.repositories.user_repository import UserRepository
from app.schemas.UsuarioSchemas import (
    UsuarioSchemaBase, 
    UsuarioSchemaCreate, 
    UsuarioSchemaUpdate, 
    UsuarioIdSchemas, 
    UsuarioSchemaEmail
)
from app.api.dependencies import get_current_user, get_session
from app.infrastructure.services.security_service import gerar_hash_senha
from app.infrastructure.services.auth_service import autenticar, criar_token_acesso

router = APIRouter()

# ✅ POST - Login do Usuário
@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario = await autenticar(email=form_data.username, senha=form_data.password, db=db)

    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Dados de acesso incorretos.')
        
    response_content = {
        "id": str(usuario.id),  
        "username": usuario.username,
        "email": usuario.email,
        "token": criar_token_acesso(sub=str(usuario.id)),
        "token_type": "bearer"
    }

    return JSONResponse(content=response_content, status_code=status.HTTP_200_OK)


# ✅ POST - Criar um novo Usuário (Signup)
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaBase)
async def post_usuario(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)):
    usuario_repo = UserRepository(db)
    user_usecase = UserUseCase(usuario_repo)

    try:
        novo_usuario = await user_usecase.create_user(
            username=usuario.username,
            email=usuario.email,
            first_name=usuario.firstName,
            last_name=usuario.lastName,
            senha=gerar_hash_senha(usuario.senha)
        )
        return novo_usuario
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail='Já existe um usuário com este email ou username cadastrado.'
        )


# ✅ GET - Buscar Usuário por ID
@router.get('/usuario-id/{usuario_id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_200_OK)
async def get_usuario_id(usuario_id: UUID, db: AsyncSession = Depends(get_session)):
    usuario_repo = UserRepository(db)
    user_usecase = UserUseCase(usuario_repo)

    usuario = await user_usecase.get_user_by_id(usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado.')
    
    return usuario


# ✅ GET - Buscar Usuário por Email
@router.get('/usuario-email/{email_id}', response_model=UsuarioSchemaEmail, status_code=status.HTTP_200_OK)
async def get_usuario_email(email_id: str, db: AsyncSession = Depends(get_session)):
    usuario_repo = UserRepository(db)
    user_usecase = UserUseCase(usuario_repo)

    usuario = await user_usecase.get_user_by_email(email_id.replace("%40", "@"))
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado.')

    return usuario


# ✅ GET - Listar Todos os Usuários
@router.get('/', response_model=List[UsuarioIdSchemas])
async def get_usuarios(db: AsyncSession = Depends(get_session)):
    usuario_repo = UserRepository(db)
    user_usecase = UserUseCase(usuario_repo)

    return await user_usecase.list_users()


# ✅ PUT - Atualizar Usuário
@router.put('/{usuario_id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_usuario(
    usuario_id: UUID, 
    usuario: UsuarioSchemaUpdate, 
    logado: UsuarioSchemaBase = Depends(get_current_user), 
    db: AsyncSession = Depends(get_session)
):
    usuario_repo = UserRepository(db)
    user_usecase = UserUseCase(usuario_repo)

    if logado.id != usuario_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a modificar este usuário.")
    
    updated_user = await user_usecase.update_user(usuario_id, usuario)
    return updated_user


# ✅ DELETE - Deletar Usuário
@router.delete('/{usuario_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: UUID, logado: UsuarioSchemaBase = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    usuario_repo = UserRepository(db)
    user_usecase = UserUseCase(usuario_repo)

    if logado.id != usuario_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a excluir este usuário.")

    deleted_user = await user_usecase.delete_user(usuario_id)
    if not deleted_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
