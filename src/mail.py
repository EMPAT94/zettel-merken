import smtplib
import ssl

from email.message import EmailMessage

from . import config as cfg


def send_mail(mail_content: str, config: cfg.Config) -> None:
    """Send an email containing contents of notes list scheduled for this run"""

    msg = EmailMessage()
    msg["Subject"] = "Zettel Merken Daily Review"
    msg["From"] = config.EMAIL.USER
    msg["To"] = config.RECEIVERS
    msg.set_content(mail_content)

    with smtplib.SMTP_SSL(
        config.EMAIL.HOST, config.EMAIL.PORT, context=ssl.create_default_context()
    ) as server:
        server.login(config.EMAIL.USER, config.EMAIL.PASS)
        # SMTPHeloError            The server didn't reply properly to the helo greeting.
        # SMTPAuthenticationError  The server didn't accept the username password combination.
        # SMTPNotSupportedError    The AUTH command is not supported by the server.
        # SMTPException            No suitable authentication method was found.
        server.send_message(msg)
