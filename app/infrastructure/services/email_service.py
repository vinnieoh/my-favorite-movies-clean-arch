import logging
from app.adapters.email_adapter import email_adapter

class EmailHandler(logging.Handler):
    def __init__(self, mailhost, fromaddr, toaddrs, subject, credentials=None, secure=None):
        logging.Handler.__init__(self)
        self.mailhost = mailhost
        self.fromaddr = fromaddr
        self.toaddrs = toaddrs
        self.subject = subject
        self.credentials = credentials
        self.secure = secure

    def emit(self, record):
        try:
            msg = self.format(record)
            for recipient in self.toaddrs:
                email_adapter.send_email(to_email=recipient, subject=self.subject, body=msg)
        except Exception:
            self.handleError(record)
