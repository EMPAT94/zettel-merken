#!/usr/bin/env python

import os, json, smtplib, ssl, sqlite3

from email.message import EmailMessage
from pathlib import Path
from typing import Sequence
from datetime import date, timedelta

# For testing purpose only
if __name__ != "__main__":
    import config_example as config


def create_schema():
    """Create database schema for zettel-merken note schedules"""
    with sqlite3.connect(config.DB_PATH) as cx:
        cu = cx.cursor()

        cu.execute(
            """CREATE TABLE IF NOT EXISTS note_schedule (
                id INTEGER PRIMARY KEY ASC,
                note TEXT NOT NULL UNIQUE,
                stats JSON NOT NULL,
                schedule JSON,
                sent JSON
            )"""
        )

        cu.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_note ON note_schedule (note)")


def notes_list(dirs: Sequence[str]):
    """Get a list of notes from a list of directories"""

    for dir in dirs:
        for note in os.listdir(dir):
            if Path(note).suffix in [
                ".md",
                ".txt",
                ".org",
                ".norg",
            ]:
                yield Path(dir + os.sep + note).resolve()


class ScheduleNotFound(Exception):
    """When a note schedule is not found in database"""


class ScheduleExhausted(Exception):
    """When the note has beeen sent on all the scheduled days"""


def create_note_schedule(note: Path, schedule_days: tuple):
    """Create a schedule for a given note"""

    stats = {"mtime": os.stat(note).st_mtime}
    schedule = sorted(
        date.toordinal(date.today() + timedelta(s)) for s in schedule_days
    )
    sent = "[]"

    with sqlite3.connect(config.DB_PATH) as cx:
        cx.cursor().execute(
            "insert into note_schedule (note, stats, schedule, sent) values (?, ?, ?, ?)",
            (str(note), json.dumps(stats), json.dumps(schedule), sent),
        )


def is_note_scheduled(note: Path):
    """Check if a note is scheduled for this run"""

    with sqlite3.connect(config.DB_PATH) as cx:
        data = (
            cx.cursor()
            .execute(f"SELECT schedule FROM note_schedule WHERE note = '{note}'")
            .fetchone()
        )

        if not data:
            raise ScheduleNotFound

        if not data[0]:
            raise ScheduleExhausted

        schedule = json.loads(data[0])
        today = date.toordinal(date.today())
        for day in schedule:
            if day <= today:
                return True

        return False


def build_mail_content(notes: list[Path]):
    """Create a mail from a list of notes"""
    return "\n\n".join(open(note).read() for note in notes)


def send_mail(mail_content: str):
    """Send an email containing contents of notes list scheduled for this run"""

    msg = EmailMessage()
    msg["Subject"] = "Zettel Merken Daily Review"
    msg["From"] = config.EMAIL["USER"]
    msg["To"] = config.RECEIVERS
    msg.set_content(mail_content)

    with smtplib.SMTP_SSL(
        config.EMAIL["HOST"], config.EMAIL["PORT"], context=ssl.create_default_context()
    ) as server:
        server.login(config.EMAIL["USER"], config.EMAIL["PASS"])
        server.send_message(msg)


def update_schedule(notes: list[Path]):
    """If a note was mailed, update in database"""

    notes_list = [str(note) for note in notes]

    with sqlite3.connect(config.DB_PATH) as cx:
        cu = cx.cursor()

        notes_to_update = cu.execute(
            f"SELECT id, schedule, sent FROM note_schedule WHERE note IN ({', '.join('?' * len(notes_list))})",
            notes_list,
        )

        today = date.toordinal(date.today())
        for (id, schedule, sent) in notes_to_update:
            schedule = json.loads(schedule).pop()
            sent = json.loads(sent).append(today)
            cu.execute(
                "UPDATE note_schedule SET schedule = (?) and sent = (?) WHERE id = (?)",
                (schedule, sent, id),
            )


def main():
    create_schema()

    scheduled_notes: list[Path] = []

    for note in notes_list(config.NOTE_DIRS):
        try:
            if is_note_scheduled(note):
                scheduled_notes.append(note)
                if len(scheduled_notes) > config.MAX_NOTES_PER_MAIL:
                    break
        except ScheduleNotFound:
            create_note_schedule(note, config.SCHEDULE_DAYS)
        except ScheduleExhausted:
            continue

    mail_content = build_mail_content(scheduled_notes)
    send_mail(mail_content)
    update_schedule(scheduled_notes)


if __name__ == "__main__":
    import config

    main()
