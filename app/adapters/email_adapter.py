import smtplib
from email.message import EmailMessage
from app.settings.config import config

class EmailAdapter:
    def __init__(self):
        """
        Inicializa o adaptador de e-mail com as configurações definidas no projeto.
        """
        self.smtp_server = config.EMAIL_SMTP_SERVER
        self.smtp_port = config.EMAIL_SMTP_PORT
        self.username = config.EMAIL_USER
        self.password = config.EMAIL_PASSWORD
        self.from_email = self.username  # O remetente padrão será o usuário de login

    def send_email(self, to_email: str, subject: str, body: str):
        """
        Envia um e-mail para o destinatário especificado.
        
        :param to_email: Endereço de e-mail do destinatário.
        :param subject: Assunto do e-mail.
        :param body: Corpo do e-mail.
        """
        try:
            email = EmailMessage()
            email.set_content(body)
            email["Subject"] = subject
            email["From"] = self.from_email
            email["To"] = to_email

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Habilita segurança TLS
                server.login(self.username, self.password)
                server.send_message(email)

            return {"message": "E-mail enviado com sucesso!"}

        except Exception as e:
            return {"error": str(e)}

# Criando uma instância reutilizável do adaptador
email_adapter = EmailAdapter()
