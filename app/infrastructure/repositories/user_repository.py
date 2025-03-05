from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.domain.models.User import UsuarioModel
from uuid import UUID

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: UUID):
        query = select(UsuarioModel).filter(UsuarioModel.id == user_id)
        result = await self.db.execute(query)
        return result.scalars().one_or_none()

    async def get_by_email(self, email: str):
        query = select(UsuarioModel).filter(UsuarioModel.email == email)
        result = await self.db.execute(query)
        return result.scalars().one_or_none()

    async def create(self, username: str, email: str, first_name: str, last_name: str, senha: str):
        new_user = UsuarioModel(username=username, email=email, firstName=first_name, lastName=last_name, senha=senha)
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    async def delete(self, user_id: UUID):
        user = await self.get_by_id(user_id)
        if user:
            await self.db.delete(user)
            await self.db.commit()
        return user

