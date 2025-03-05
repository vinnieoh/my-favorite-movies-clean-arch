from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Union
from uuid import UUID

from app.domain.usecases.movie_usecase import MovieUseCase
from app.domain.usecases.tv_show_usecase import TVShowUseCase
from app.infrastructure.repositories.movie_repository import MovieRepository
from app.infrastructure.repositories.tv_show_repository import TVShowRepository

from app.schemas.TvShowsSchemas import TVResponseSchema
from app.schemas.MovieSchemas import MovieResponseSchema

from app.api.dependencies import get_current_user, get_session

router = APIRouter()

@router.get('/conteudos', response_model=List[Union[MovieResponseSchema, TVResponseSchema]], status_code=status.HTTP_200_OK)
async def get_all_contents(logado=Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    movie_repo = MovieRepository(db)
    tv_show_repo = TVShowRepository(db)

    movie_usecase = MovieUseCase(movie_repo)
    tv_show_usecase = TVShowUseCase(tv_show_repo)

    movies = await movie_usecase.get_movies_by_user(logado.id)
    tv_shows = await tv_show_usecase.get_tv_shows_by_user(logado.id)

    all_contents = movies + tv_shows

    if not all_contents:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Nenhum conteúdo encontrado para este usuário.')

    return all_contents


@router.get('/filmes', response_model=List[MovieResponseSchema], status_code=status.HTTP_200_OK)
async def get_all_movies(logado=Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    movie_repo = MovieRepository(db)
    movie_usecase = MovieUseCase(movie_repo)

    movies = await movie_usecase.get_movies_by_user(logado.id)

    if not movies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Nenhum filme encontrado para este usuário.')

    return movies


@router.get('/tvshows', response_model=List[TVResponseSchema], status_code=status.HTTP_200_OK)
async def get_all_tv_shows(logado=Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    tv_show_repo = TVShowRepository(db)
    tv_show_usecase = TVShowUseCase(tv_show_repo)

    tv_shows = await tv_show_usecase.get_tv_shows_by_user(logado.id)

    if not tv_shows:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Nenhuma série de TV encontrada para este usuário.')

    return tv_shows
