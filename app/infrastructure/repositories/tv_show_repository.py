from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.domain.models.TvShows import TVModel
from uuid import UUID

class TVShowRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, tv_id: UUID):
        query = select(TVModel).filter(TVModel.id == tv_id)
        result = await self.db.execute(query)
        return result.scalars().one_or_none()

    async def create(self, name: str, first_air_date: str, overview: str, user_id: UUID):
        new_tv_show = TVModel(name=name, first_air_date=first_air_date, overview=overview, user_id=user_id)
        self.db.add(new_tv_show)
        await self.db.commit()
        await self.db.refresh(new_tv_show)
        return new_tv_show

    async def delete(self, tv_id: UUID):
        tv_show = await self.get_by_id(tv_id)
        if tv_show:
            await self.db.delete(tv_show)
            await self.db.commit()
        return tv_show
