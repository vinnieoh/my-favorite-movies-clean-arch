from typing import List
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

# Dependências
from app.api.dependencies  import get_current_user, get_session

# Models
from app.domain.models.Comentario import CommentModel
from app.domain.models.User import UsuarioModel

# Schemas
from app.schemas.ComentarioSchemas import CommentCreateSchema, CommentUpdateSchema, CommentResponseSchema

router = APIRouter()


# 🔹 Buscar todos os comentários de uma mídia específica
@router.get('/comentarios/{media_id}', response_model=List[CommentResponseSchema], status_code=status.HTTP_200_OK)
async def get_comments_by_media(media_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CommentModel).filter(CommentModel.media_id == media_id)
        result = await session.execute(query)
        comentarios = result.scalars().all()

        if not comentarios:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Nenhum comentário encontrado para este media_id.')

        return comentarios


# 🔹 Criar um novo comentário
@router.post('/comentarios', status_code=status.HTTP_201_CREATED, response_model=CommentResponseSchema)
async def create_comment(comment: CommentCreateSchema, db: AsyncSession = Depends(get_session), logado: UsuarioModel = Depends(get_current_user)):
    
    novo_comentario = CommentModel(
        user_id=logado.id,
        media_id=comment.media_id,
        media_type=comment.media_type,
        content=comment.content,
        likes=comment.likes,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    async with db as session:
        try:
            session.add(novo_comentario)
            await session.commit()
            await session.refresh(novo_comentario)
            return novo_comentario
        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Erro ao criar o comentário. Verifique se todos os campos estão corretos.')


# 🔹 Atualizar um comentário existente
@router.put('/comentarios/{comment_id}', response_model=CommentResponseSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_comment(comment_id: UUID, comment: CommentUpdateSchema, logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CommentModel).filter(CommentModel.id == comment_id)
        result = await session.execute(query)
        comentario_up = result.scalars().one_or_none()

        if not comentario_up:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Comentário não encontrado.')

        if logado.id != comentario_up.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a modificar este comentário.")
        
        # Atualização de campos condicional
        for key, value in comment.dict(exclude_unset=True).items():
            setattr(comentario_up, key, value)

        comentario_up.updated_at = datetime.utcnow()
        
        try:
            await session.commit()
            await session.refresh(comentario_up)
            return comentario_up
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# 🔹 Deletar um comentário
@router.delete('/comentarios/{comment_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: UUID, db: AsyncSession = Depends(get_session), logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(CommentModel).filter(CommentModel.id == comment_id, CommentModel.user_id == logado.id)
        result = await session.execute(query)
        comment_to_delete = result.scalars().one_or_none()

        if not comment_to_delete:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comentário não encontrado.")

        await session.delete(comment_to_delete)
        await session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
