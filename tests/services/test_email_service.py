import pytest
import logging
from unittest.mock import patch
from app.infrastructure.services.email_service import EmailHandler


@pytest.fixture
def email_handler():
    """Cria uma instância do EmailHandler para os testes."""
    return EmailHandler(
        mailhost="smtp.example.com",
        fromaddr="sender@example.com",
        toaddrs=["recipient@example.com"],
        subject="Test Email"
    )


@patch("app.adapters.email_adapter.email_adapter.send_email")  # Corrigido para a instância correta
def test_emit_success(mock_send_email, email_handler):
    """
    Testa se o e-mail é enviado corretamente ao chamar emit().
    """
    mock_send_email.return_value = {"message": "E-mail enviado com sucesso!"}

    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.ERROR)
    logger.addHandler(email_handler)

    log_message = "Este é um teste de erro no log"
    logger.error(log_message)

    mock_send_email.assert_called_once_with(
        to_email="recipient@example.com",
        subject="Test Email",
        body=log_message
    )


@patch("app.adapters.email_adapter.email_adapter.send_email", side_effect=Exception("Falha ao enviar e-mail"))
def test_emit_failure(mock_send_email, email_handler):
    """
    Testa se a exceção no envio de e-mail é tratada corretamente.
    """
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.ERROR)
    logger.addHandler(email_handler)

    log_message = "Erro de teste para falha no e-mail"

    with patch.object(email_handler, "handleError") as mock_handle_error:
        logger.error(log_message)

        mock_handle_error.assert_called_once()
