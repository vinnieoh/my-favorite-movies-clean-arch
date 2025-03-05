from app.domain.entities.user import User
from app.infrastructure.repositories.user_repository import UserRepository
from uuid import UUID

class UserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_user_by_id(self, user_id: UUID) -> User:
        """Obtém um usuário pelo ID"""
        user_data = await self.user_repository.get_by_id(user_id)
        if not user_data:
            raise ValueError("Usuário não encontrado")
        return User(**user_data)

    async def create_user(self, username: str, email: str, first_name: str, last_name: str, senha: str) -> User:
        """Cria um novo usuário"""
        new_user_data = await self.user_repository.create(username, email, first_name, last_name, senha)
        return User(**new_user_data)

    async def delete_user(self, user_id: UUID):
        """Exclui um usuário"""
        return await self.user_repository.delete(user_id)