import pytest
from unittest.mock import patch, MagicMock
from app.adapters.email_adapter import EmailAdapter

@pytest.fixture
def email_adapter():
    """Cria uma instância do EmailAdapter para os testes"""
    return EmailAdapter()

@patch("smtplib.SMTP")  # Mocka o SMTP para evitar envios reais
def test_send_email_success(mock_smtp, email_adapter):
    """
    Testa se o e-mail é enviado com sucesso
    """
    # Criando um mock para o servidor SMTP
    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server

    # Dados do e-mail de teste
    to_email = "destinatario@example.com"
    subject = "Teste de E-mail"
    body = "Este é um e-mail de teste."

    # Chamando a função
    response = email_adapter.send_email(to_email, subject, body)

    # Verificando se o e-mail foi enviado corretamente
    mock_server.starttls.assert_called_once()
    mock_server.login.assert_called_once_with(email_adapter.username, email_adapter.password)
    mock_server.send_message.assert_called_once()
    
    assert response == {"message": "E-mail enviado com sucesso!"}

@patch("smtplib.SMTP", side_effect=Exception("Erro ao conectar ao SMTP"))
def test_send_email_failure(mock_smtp, email_adapter):
    """
    Testa se o e-mail falha corretamente quando há erro no SMTP
    """
    to_email = "destinatario@example.com"
    subject = "Teste de Erro"
    body = "Este e-mail não será enviado."

    response = email_adapter.send_email(to_email, subject, body)

    assert "error" in response
    assert response["error"] == "Erro ao conectar ao SMTP"
