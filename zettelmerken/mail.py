import smtplib
import ssl

from email.message import EmailMessage

from .config import Config


def send_mail(mail_content: str, config: Config) -> None:
    """Send an email containing contents of notes list scheduled for this run"""

    with smtplib.SMTP_SSL(
        config.EMAIL.HOST, config.EMAIL.PORT, context=ssl.create_default_context()
    ) as server:
        server.login(config.EMAIL.USER, config.EMAIL.PASS)

        msg = EmailMessage()
        msg["Subject"] = "Zettel Merken Daily Review"
        msg["From"] = config.EMAIL.USER
        msg["To"] = config.RECEIVERS
        msg.set_content(mail_content)

        server.send_message(msg)
