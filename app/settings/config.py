from typing import ClassVar
from dotenv import dotenv_values
from pydantic_settings import BaseSettings
from sqlalchemy.orm import declarative_base

class Config(BaseSettings):
    _config_env = dotenv_values("./dotenv_files/.env")
    
    API_V1_STR: str = '/api/v1'
    PROJECT_NAME: str = "My Favorite Movies"
    API_MOVIE: str = _config_env.get("API_MOVIE", "default_api_movie_url")
    DBBaseModel: ClassVar = declarative_base() 
    
    DB_HOST: str = _config_env.get("DB_HOST", "localhost")
    DB_PORT: int = int(_config_env.get("DB_PORT", 5432))
    DB_NAME: str = _config_env.get("DB_NAME", "default_db")
    DB_USER: str = _config_env.get("DB_USER", "postgres")
    DB_PASSWORD: str = _config_env.get("DB_PASSWORD", "password")
    DB_URL: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    JWT_SECRET: str = _config_env.get("JWT_SECRET", "default_jwt_secret")
    ALGORITHM: str = _config_env.get("ALGORITHM", "HS256")

    # Configuração de expiração de token
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 semana
    
    # Redis Configs
    HOST_REDIS: str = _config_env.get("HOST_REDIS", "default_redis_host")
    PORT_REDIS: str = _config_env.get("PORT_REDIS", "default_redis_port")
    DB_REDIS: str = _config_env.get("DB_REDIS", "default_redis_db")
    REDIS_EXPIRATION_TIME_24H: int = 24 * 60 * 60  # 24 horas em segundos
    
    # Email Configs Log
    EMAIL_lOG: str = _config_env.get("EMAIL_LOG", "default_email_log")
    PASSWORD_LOG: str = _config_env.get("PASSWORD_LOG", "default_password_log")
    EMAIL_SEND_LOG_01: str = _config_env.get("EMAIL_SEND_LOG_01", "default_email_send_log_01")
    EMAIL_SEND_LOG_02: str = _config_env.get("EMAIL_SEND_LOG_02", "default_email_send_log_02")
    
    # Configuração de E-mail
    EMAIL_SMTP_SERVER: str = _config_env.get("EMAIL_SMTP_SERVER", "smtp.example.com")  # Servidor SMTP
    EMAIL_SMTP_PORT: int = int(_config_env.get("EMAIL_SMTP_PORT", 587))  # Porta do SMTP (convertida para int)
    EMAIL_USER: str = _config_env.get("EMAIL_USER", "seu-email@example.com")  # Usuário do SMTP
    EMAIL_PASSWORD: str = _config_env.get("EMAIL_PASSWORD", "sua-senha")  # Senha do SMTP

    

config: Config = Config()
