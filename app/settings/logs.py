import logging
import os
import logging.config
from app.infrastructure.services.email_service import EmailHandler
from app.settings.config import config

# Caminho para os logs
LOG_DIR = "loggings_files"
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Criar o diretório de logs se não existir
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.FileHandler",
            "filename": LOG_FILE,
            "mode": "a",
        },
        "email": {
            "level": "ERROR",
            "formatter": "standard",
            "class": "app.infrastructure.services.email_service.EmailHandler",
            "mailhost": ("smtp.example.com", 587),
            "fromaddr": "your_email@example.com",
            "toaddrs": [config.EMAIL_SEND_LOG_01, config.EMAIL_SEND_LOG_02],
            "subject": "Error Log",
            "credentials": (config.EMAIL_lOG, config.PASSWORD_LOG),
            "secure": None
        }
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["default", "file", "email"],
            "level": "INFO",
            "propagate": True
        },
        "uvicorn.error": {
            "handlers": ["default", "file", "email"],
            "level": "INFO",
            "propagate": False
        },
        "uvicorn.access": {
            "handlers": ["default", "file"],
            "level": "INFO",
            "propagate": False
        },
    }
}

def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)