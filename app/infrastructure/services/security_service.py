from passlib.context import CryptContext


CRIPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verificar_senha(senha: str, hash_senha: str) -> bool:
    
    if senha == "" or hash_senha == "":
        raise ValueError("Senha ou hash invalido!")
    
    return CRIPTO.verify(senha, hash_senha)


def gerar_hash_senha(senha: str) -> str:
    
    if senha == "":
        raise ValueError("Senha invalida!")
    
    return CRIPTO.hash(senha)