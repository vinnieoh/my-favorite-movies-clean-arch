from redis import Redis
import json

from app.adapters.redis_adapter import __redis_connection
from app.settings.config import config

class RedisRepository:

    def __init__(self, redis_conn: Redis) -> None:
        self.__redis_conn = redis_conn
    
    def get(self, key: str) -> any:
        value = self.__redis_conn.get(key)
        
        if value:
            return value.decode('utf-8')
        return None

    def insert_hash(self, key: str, field: str, value: any) -> None:
        self.__redis_conn.hset(key, field, value)

    def get_hash(self, key: str, field: str) -> any:
        value = self.__redis_conn.hget(key, field)
        
        if value:
            return value.decode('utf-8')
        return None

    def insert(self, key: str, value: any, ex: int = config.REDIS_EXPIRATION_TIME_24H) -> None:
        value = json.dumps(value)
        self.__redis_conn.set(key, value, ex=ex)

    def insert_hash_ex(self, key: str, field: str, value: any, ex: int = config.REDIS_EXPIRATION_TIME_24H) -> None:
        self.__redis_conn.hset(key, field, value)
        self.__redis_conn.expire(key, ex)
        
        
redis_repository = RedisRepository(__redis_connection)