import smtplib, ssl

from pathlib import Path
from email.message import EmailMessage

from config import Config


def build_mail_content(notes: list[Path]) -> str:
    """Create a mail from a list of notes"""
    return "\n\n".join(str(note) + "\n" + open(note).read() for note in notes)


def send_mail(mail_content: str, config: Config) -> None:
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
        server.send_message(msg)
