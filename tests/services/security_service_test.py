import pytest
from app.infrastructure.services.security_service import gerar_hash_senha, verificar_senha

@pytest.fixture
def setup():
    """
    Retorna um dicionário com senhas de teste.
    """
    return {
        "password_01": "teste12345",
        "password_02": "teste54321"
    }

def test_gerar_hash(setup):
    """
    Testa se a função gerar_hash_senha retorna um hash válido.
    """
    password = setup["password_01"]
    hash_01 = gerar_hash_senha(password)

    assert verificar_senha(password, hash_01) == True
    assert verificar_senha("senha_errada", hash_01) == False


def test_verificar_senha(setup):
    """
    Testa se a função verificar_senha valida corretamente uma senha.
    """
    password = setup["password_02"]
    hash_02 = gerar_hash_senha(password)

    assert verificar_senha(password, hash_02) == True  # Senha correta
    assert verificar_senha("outra_senha", hash_02) == False  # Senha errada

def test_verificar_senha_invalida():
    """
    Testa se a função verificar_senha levanta erro ao receber senha ou hash vazios.
    """
    with pytest.raises(ValueError, match="Senha ou hash invalido!"):
        verificar_senha("", "algum_hash")

    with pytest.raises(ValueError, match="Senha ou hash invalido!"):
        verificar_senha("senha123", "")

    with pytest.raises(ValueError, match="Senha ou hash invalido!"):
        verificar_senha("", "")
        
def test_verificar_hash_invalida():
    """
    Testa se a função gerar_hash_senha levanta erro ao receber senha vazios.
    """
    
    with pytest.raises(ValueError, match="Senha invalida!"):
        gerar_hash_senha("")