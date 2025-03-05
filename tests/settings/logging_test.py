import logging
import pytest
import os
from app.settings.logs import setup_logging  

@pytest.fixture(scope="function", autouse=True)
def configure_logging():
    """Configura o logging antes de cada teste."""
    setup_logging()

def test_logging_to_file():
    """Testa se as mensagens de log são gravadas corretamente no arquivo app.log."""
    logger = logging.getLogger("test_logger")
    log_message = "Teste de logging no arquivo"

    logger.info(log_message)

    # Verifica se a mensagem foi gravada no arquivo
    with open("./loggings_files/app.log", "r") as log_file:
        log_contents = log_file.read()

    assert log_message in log_contents  # Verifica se a mensagem está no log

def test_logging_email_handler(mocker):
    """Testa se o EmailHandler é chamado corretamente ao registrar um erro."""
    mock_email_handler = mocker.patch("app.infrastructure.services.email_service.EmailHandler.emit")

    logger = logging.getLogger("test_logger")
    error_message = "Teste de erro no log"

    logger.error(error_message)  # Deve acionar o EmailHandler

    # Verifica se o EmailHandler foi chamado
    mock_email_handler.assert_called_once()
