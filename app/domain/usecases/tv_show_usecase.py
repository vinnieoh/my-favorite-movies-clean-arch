from app.domain.entities.tv_show import TVShow
from app.infrastructure.repositories.tv_show_repository import TVShowRepository
from uuid import UUID

class TVShowUseCase:
    def __init__(self, tv_show_repository: TVShowRepository):
        self.tv_show_repository = tv_show_repository

    async def get_tv_show_by_id(self, tv_id: UUID) -> TVShow:
        """Obtém uma série pelo ID"""
        tv_data = await self.tv_show_repository.get_by_id(tv_id)
        if not tv_data:
            raise ValueError("Série não encontrada")
        return TVShow(**tv_data)

    async def create_tv_show(self, name: str, first_air_date: str, overview: str, user_id: UUID) -> TVShow:
        """Cria uma nova série"""
        new_tv_data = await self.tv_show_repository.create(name, first_air_date, overview, user_id)
        return TVShow(**new_tv_data)

    async def delete_tv_show(self, tv_id: UUID):
        """Exclui uma série"""
        return await self.tv_show_repository.delete(tv_id)
