from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Dependências
from app.api.dependencies import get_current_user, get_session

# Schemas
from app.schemas.MovieSchemas import MovieCreateSchema, MovieUpdateSchema, MovieResponseSchema
from app.schemas.TvShowsSchemas import TVCreateSchema, TVUpdateSchema, TVResponseSchema

# Models
from app.domain.models.TvShows import TVModel
from app.domain.models.Movie import MovieModel
from app.domain.models.User import UsuarioModel

# Adapter para comunicação com API externa
from app.adapters.movie_api_adapter import MovieAPIAdapter

router = APIRouter()


# 🔹 Rota para buscar conteúdos populares da semana no Brasil
@router.get('/trending-all-week-br')
async def get_trending_all_week_br():
    return MovieAPIAdapter.get_trending_all_week()


# 🔹 Rota para buscar conteúdos populares do dia no Brasil
@router.get('/trending-all-day-br')
async def get_trading_all_day_br():
    return MovieAPIAdapter.get_trending_all_day()


# 🔹 Rota para pesquisar conteúdo pelo nome
@router.get('/search-conteudo/{conteudo}')
async def get_search_conteudo(conteudo: str):
    return MovieAPIAdapter.search_content(conteudo)


# 🔹 Rota para buscar detalhes de um filme pelo ID
@router.get('/movie-id/{id}', response_model=MovieResponseSchema, status_code=status.HTTP_200_OK)
async def get_movie_id(id: int):
    return MovieAPIAdapter.get_movie_by_id(id)


# 🔹 Rota para buscar detalhes de uma série de TV pelo ID
@router.get('/tv-show-id/{id}', response_model=TVResponseSchema, status_code=status.HTTP_200_OK)
async def get_tv_show_id(id: int):
    return MovieAPIAdapter.get_tv_show_by_id(id)


# 🔹 Rota para registrar um novo filme no banco
@router.post('/registra-filme', status_code=status.HTTP_201_CREATED, response_model=MovieCreateSchema)
async def cria_filme(filme: MovieCreateSchema, db: AsyncSession = Depends(get_session), logado: UsuarioModel = Depends(get_current_user)):
    novo_filme = MovieModel(**filme.dict(), user_id=logado.id)

    async with db as session:
        try:
            session.add(novo_filme)
            await session.commit()
            await session.refresh(novo_filme)
            return novo_filme
        except Exception:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Não foi possível cadastrar este filme!')


# 🔹 Rota para registrar uma nova série de TV no banco
@router.post('/registra-tvshow', status_code=status.HTTP_201_CREATED, response_model=TVCreateSchema)
async def cria_tvshow(tv_show: TVCreateSchema, db: AsyncSession = Depends(get_session), logado: UsuarioModel = Depends(get_current_user)):
    novo_tv_show = TVModel(**tv_show.dict(), user_id=logado.id)

    async with db as session:
        try:
            session.add(novo_tv_show)
            await session.commit()
            await session.refresh(novo_tv_show)
            return novo_tv_show
        except Exception:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Não foi possível cadastrar este TV show!')


# 🔹 Rota para deletar um filme
@router.delete('/delete-filme/{filme_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_filme(filme_id: str, logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(MovieModel).filter(MovieModel.id == filme_id)
        result = await session.execute(query)
        filme_del = result.scalars().one_or_none()

        if not filme_del:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Filme não encontrado.')

        if logado.id != filme_del.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a deletar este filme.")

        await session.delete(filme_del)
        await session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)


# 🔹 Rota para deletar um TV Show
@router.delete('/delete-tvshow/{tv_show_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_tv_show(tv_show_id: str, logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(TVModel).filter(TVModel.id == tv_show_id)
        result = await session.execute(query)
        tv_show_del = result.scalars().one_or_none()

        if not tv_show_del:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='TV show não encontrado.')

        if logado.id != tv_show_del.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a deletar este TV show.")

        await session.delete(tv_show_del)
        await session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)


# 🔹 Rota para atualizar um filme
@router.put('/update-filme/{filme_id}', response_model=MovieUpdateSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_filme(filme_id: str, filme: MovieUpdateSchema, logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(MovieModel).filter(MovieModel.id == filme_id)
        result = await session.execute(query)
        filme_up = result.scalars().one_or_none()

        if not filme_up:
            raise HTTPException(detail='Filme não encontrado.', status_code=status.HTTP_404_NOT_FOUND)

        if logado.id != filme_up.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a modificar este filme.")

        for key, value in filme.dict(exclude_unset=True).items():
            setattr(filme_up, key, value)

        await session.commit()
        return filme_up


# 🔹 Rota para atualizar um TV Show
@router.put('/update-tvshow/{tv_show_id}', response_model=TVUpdateSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_tv_show(tv_show_id: str, tv_show: TVUpdateSchema, logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(TVModel).filter(TVModel.id == tv_show_id)
        result = await session.execute(query)
        tv_show_up = result.scalars().one_or_none()

        if not tv_show_up:
            raise HTTPException(detail='TV show não encontrado.', status_code=status.HTTP_404_NOT_FOUND)

        if logado.id != tv_show_up.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Não autorizado a modificar este TV show.")

        for key, value in tv_show.dict(exclude_unset=True).items():
            setattr(tv_show_up, key, value)

        await session.commit()
        return tv_show_up
