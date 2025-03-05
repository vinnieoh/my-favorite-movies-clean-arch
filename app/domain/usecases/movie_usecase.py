from app.domain.entities.movie import Movie
from app.infrastructure.repositories.movie_repository import MovieRepository
from uuid import UUID

class MovieUseCase:
    def __init__(self, movie_repository: MovieRepository):
        self.movie_repository = movie_repository

    async def get_movie_by_id(self, movie_id: UUID) -> Movie:
        """Obtém um filme pelo ID"""
        movie_data = await self.movie_repository.get_by_id(movie_id)
        if not movie_data:
            raise ValueError("Filme não encontrado")
        return Movie(**movie_data)

    async def create_movie(self, title: str, release_date: str, overview: str, user_id: UUID) -> Movie:
        """Cria um novo filme"""
        new_movie_data = await self.movie_repository.create(title, release_date, overview, user_id)
        return Movie(**new_movie_data)

    async def delete_movie(self, movie_id: UUID):
        """Exclui um filme"""
        return await self.movie_repository.delete(movie_id)