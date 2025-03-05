from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.domain.models.Comentario import CommentModel
from uuid import UUID

class CommentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_media_id(self, media_id: int):
        query = select(CommentModel).filter(CommentModel.media_id == media_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create(self, user_id: UUID, media_id: int, media_type: str, content: str):
        new_comment = CommentModel(user_id=user_id, media_id=media_id, media_type=media_type, content=content)
        self.db.add(new_comment)
        await self.db.commit()
        await self.db.refresh(new_comment)
        return new_comment

    async def delete(self, comment_id: UUID):
        comment = await self.get_by_media_id(comment_id)
        if comment:
            await self.db.delete(comment)
            await self.db.commit()
        return comment
