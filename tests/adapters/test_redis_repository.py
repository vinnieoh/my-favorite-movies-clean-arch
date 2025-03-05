import pytest
import json
from unittest.mock import MagicMock
from app.infrastructure.repositories.redis_database import RedisRepository


@pytest.fixture
def mock_redis():
    """Cria um mock para a conexão com o Redis."""
    return MagicMock()


@pytest.fixture
def redis_repository(mock_redis):
    """Cria uma instância do RedisRepository com o Redis mockado."""
    return RedisRepository(mock_redis)


def test_insert_and_get(redis_repository, mock_redis):
    """
    Testa se um valor pode ser armazenado e recuperado do Redis corretamente.
    """
    key = "test_key"
    value = {"data": "teste"}

    # Simula comportamento do Redis
    mock_redis.set.return_value = True
    mock_redis.get.return_value = json.dumps(value).encode("utf-8")

    # Insere e busca no Redis
    redis_repository.insert(key, value)
    result = redis_repository.get(key)

    assert result == json.dumps(value)  # O retorno de get() é uma string JSON
    mock_redis.set.assert_called_once_with(key, json.dumps(value), ex=86400)  # 24h = 86400s
    mock_redis.get.assert_called_once_with(key)


def test_insert_hash_and_get_hash(redis_repository, mock_redis):
    """
    Testa se um valor pode ser armazenado e recuperado de um hash no Redis.
    """
    key = "test_hash"
    field = "field1"
    value = "hash_value"

    # Simula comportamento do Redis
    mock_redis.hset.return_value = True
    mock_redis.hget.return_value = value.encode("utf-8")

    # Insere e busca no Redis
    redis_repository.insert_hash(key, field, value)
    result = redis_repository.get_hash(key, field)

    assert result == value
    mock_redis.hset.assert_called_once_with(key, field, value)
    mock_redis.hget.assert_called_once_with(key, field)


def test_insert_with_expiration(redis_repository, mock_redis):
    """
    Testa se um valor pode ser armazenado no Redis com tempo de expiração.
    """
    key = "test_expire_key"
    value = "expire_value"
    expiration = 3600  # 1 hora

    # Simula comportamento do Redis
    mock_redis.set.return_value = True

    redis_repository.insert(key, value, ex=expiration)

    mock_redis.set.assert_called_once_with(key, json.dumps(value), ex=expiration)


def test_insert_hash_ex(redis_repository, mock_redis):
    """
    Testa se um valor pode ser armazenado em um hash no Redis com tempo de expiração.
    """
    key = "test_hash_expire"
    field = "field2"
    value = "hash_expire_value"
    expiration = 1800  # 30 minutos

    # Simula comportamento do Redis
    mock_redis.hset.return_value = True
    mock_redis.expire.return_value = True

    redis_repository.insert_hash_ex(key, field, value, ex=expiration)

    mock_redis.hset.assert_called_once_with(key, field, value)
    mock_redis.expire.assert_called_once_with(key, expiration)
