from app.settings.config import Config

def test_config_values_from_env_file(monkeypatch):
    """
    Testa se a classe Config carrega corretamente os valores do arquivo .env.
    """
    # Simulando um arquivo .env usando monkeypatch
    env_values = {
        "API_MOVIE": "http://fakeapi.com",
        "DB_URL": "postgresql://user:password@localhost/testdb",
        "JWT_SECRET": "supersecretjwt",
        "ALGORITHM": "HS512",
        "HOST_REDIS": "127.0.0.1",
        "PORT_REDIS": "6379",
        "DB_REDIS": "0",
        "EMAIL_LOG": "log@example.com",
        "PASSWORD_LOG": "securepassword",
        "EMAIL_SEND_LOG_01": "send1@example.com",
        "EMAIL_SEND_LOG_02": "send2@example.com",
    }

    for key, value in env_values.items():
        monkeypatch.setenv(key, value)

    config = Config()  # Criando a instância da configuração

    assert config.API_MOVIE == env_values["API_MOVIE"]
    assert config.DB_URL == env_values["DB_URL"]
    assert config.JWT_SECRET == env_values["JWT_SECRET"]
    assert config.ALGORITHM == env_values["ALGORITHM"]
    assert config.HOST_REDIS == env_values["HOST_REDIS"]
    assert config.PORT_REDIS == env_values["PORT_REDIS"]
    assert config.DB_REDIS == env_values["DB_REDIS"]
    assert config.EMAIL_lOG == env_values["EMAIL_LOG"]
    assert config.PASSWORD_LOG == env_values["PASSWORD_LOG"]
    assert config.EMAIL_SEND_LOG_01 == env_values["EMAIL_SEND_LOG_01"]
    assert config.EMAIL_SEND_LOG_02 == env_values["EMAIL_SEND_LOG_02"]

def test_default_values():
    """
    Testa se a classe Config usa os valores padrão corretamente quando as variáveis de ambiente não estão definidas.
    """
    config = Config()
    
    assert config.API_MOVIE == "default_api_movie_url"
    assert config.JWT_SECRET == "default_jwt_secret"
    assert config.ALGORITHM == "HS256"
    assert config.HOST_REDIS == "default_redis_host"
    assert config.PORT_REDIS == "default_redis_port"
    assert config.DB_REDIS == "default_redis_db"
    assert config.EMAIL_lOG == "default_email_log"
    assert config.PASSWORD_LOG == "default_password_log"
    assert config.EMAIL_SEND_LOG_01 == "default_email_send_log_01"
    assert config.EMAIL_SEND_LOG_02 == "default_email_send_log_02"
