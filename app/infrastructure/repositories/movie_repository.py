from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.domain.models.Movie import MovieModel
from uuid import UUID

class MovieRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, movie_id: UUID):
        query = select(MovieModel).filter(MovieModel.id == movie_id)
        result = await self.db.execute(query)
        return result.scalars().one_or_none()

    async def create(self, title: str, release_date: str, overview: str, user_id: UUID):
        new_movie = MovieModel(title=title, release_date=release_date, overview=overview, user_id=user_id)
        self.db.add(new_movie)
        await self.db.commit()
        await self.db.refresh(new_movie)
        return new_movie

    async def delete(self, movie_id: UUID):
        movie = await self.get_by_id(movie_id)
        if movie:
            await self.db.delete(movie)
            await self.db.commit()
        return movie