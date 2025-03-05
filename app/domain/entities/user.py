from uuid import UUID

class User:
    def __init__(self, id: UUID, username: str, email: str, first_name: str, last_name: str, senha: str):
        self.id = id
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.senha = senha

    def update_email(self, new_email: str):
        """Atualiza o e-mail do usuário."""
        if "@" not in new_email:
            raise ValueError("E-mail inválido")
        self.email = new_email
