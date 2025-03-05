from app.domain.entities.comment import Comment
from app.infrastructure.repositories.comment_repository import CommentRepository
from uuid import UUID
from datetime import datetime

class CommentUseCase:
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository

    async def get_comments_by_media_id(self, media_id: int):
        """Obtém comentários por media_id"""
        return await self.comment_repository.get_by_media_id(media_id)

    async def create_comment(self, user_id: UUID, media_id: int, media_type: str, content: str):
        """Cria um novo comentário"""
        new_comment_data = await self.comment_repository.create(user_id, media_id, media_type, content)
        return Comment(**new_comment_data)

    async def delete_comment(self, comment_id: UUID):
        """Exclui um comentário"""
        return await self.comment_repository.delete(comment_id)
