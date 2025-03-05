import json
import httpx
from fastapi import HTTPException
from app.settings.config import config
from app.infrastructure.repositories.redis_database import redis_repository

# Configurações da API
AUTHORIZATION = f"Bearer {config.API_MOVIE}"
BASE_URL = "https://api.themoviedb.org/3/"

HEADERS = {
    "accept": "application/json",
    "Authorization": AUTHORIZATION
}

class MovieAPIAdapter:
    @staticmethod
    def _get_from_cache(cache_key: str):
        """Tenta obter dados do Redis antes de fazer uma requisição."""
        cached_data = redis_repository.get(cache_key)
        if cached_data:
            return json.loads(cached_data)
        return None

    @staticmethod
    def _request_api(url: str, cache_key: str = None):
        """Faz uma requisição à API e armazena no cache se necessário."""
        cached_data = MovieAPIAdapter._get_from_cache(cache_key) if cache_key else None
        if cached_data:
            return cached_data

        response = httpx.get(url, headers=HEADERS)
        
        if response.is_success:
            data = response.json()
            if cache_key:
                redis_repository.insert(cache_key, data)
            return data
        else:
            raise HTTPException(status_code=response.status_code, detail="Erro ao acessar a API")

    @classmethod
    def get_trending_all_week(cls):
        """Retorna os filmes e séries mais populares da semana no Brasil."""
        url = f"{BASE_URL}trending/all/week?language=pt-BR"
        return cls._request_api(url, "trending_all_week_br")

    @classmethod
    def get_trending_all_day(cls):
        """Retorna os filmes e séries mais populares do dia no Brasil."""
        url = f"{BASE_URL}trending/all/day?language=pt-BR"
        return cls._request_api(url, "trending_all_day_br")

    @classmethod
    def search_content(cls, query: str):
        """Pesquisa conteúdo (filmes/séries) pelo nome."""
        url = f"{BASE_URL}search/multi?query={query}&include_adult=false&language=pt-BR&page=1"
        return cls._request_api(url, f"search_{query}")

    @classmethod
    def get_movie_by_id(cls, movie_id: int):
        """Busca detalhes de um filme pelo ID."""
        url = f"{BASE_URL}movie/{movie_id}?language=pt-BR"
        return cls._request_api(url, f"movie_{movie_id}")

    @classmethod
    def get_tv_show_by_id(cls, tv_id: int):
        """Busca detalhes de uma série pelo ID."""
        url = f"{BASE_URL}tv/{tv_id}?language=pt-BR"
        return cls._request_api(url, f"tv_show_{tv_id}")
