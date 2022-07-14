import os, json, smtplib, ssl, sqlite3

from pathlib import Path
from datetime import date, timedelta
from config import *


def create_schema():
    """Create database schema for zettel-merken note schedules"""
    with sqlite3.connect(DB_PATH) as cx:
        cu = cx.cursor()
        cu.execute(
            """CREATE TABLE IF NOT EXISTS note_schedule (
                id INTEGER PRIMARY KEY ASC,
                note TEXT NOT NULL UNIQUE,
                stats JSON NOT NULL,
                schedule JSON NOT NULL
            )"""
        )


def notes_list(dirs):
    """Get a list of notes from a list of directories"""
    for dir in dirs:
        for note in os.listdir(dir):
            # if Path(note).is_file() and note.endswith(("md", "txt", "org")):
            yield Path(note).absolute()


class ScheduleNotFound(Exception):
    """When a note schedule is not found in database"""


class ScheduleExhausted(Exception):
    """When the note has beeen sent on all the scheduled days"""


def is_note_scheduled(note: Path):
    """Check if a note is scheduled for this run"""

    with sqlite3.connect(DB_PATH) as cx:
        data = (
            cx.cursor()
            .execute(f"SELECT schedule FROM note_schedule WHERE note = '{note}'")
            .fetchone()
        )

        if not data:
            raise ScheduleNotFound

        schedule = json.loads(data[0])
        for scheduled_day, sent_day in schedule.items():
            scheduled_date = date.fromordinal(int(scheduled_day))
            if scheduled_date > date.today():
                return False
            if not sent_day:
                return True

        else:
            raise ScheduleExhausted


def create_note_schedule(note: Path, schedule_days: tuple):
    """Create a schedule for a given note"""

    os_stat = os.stat(note)
    stats = json.dumps({"size": os_stat.st_size, "mtime": os_stat.st_mtime})
    schedule = json.dumps(
        {date.toordinal(date.today() + timedelta(s)): None for s in schedule_days}
    )
    with sqlite3.connect(DB_PATH) as cx:
        cx.cursor().execute(
            "insert into note_schedule (note, stats, schedule) values (?, ?, ?)",
            (str(note), stats, schedule),
        )


def build_mail(notes: Path):
    """Create a mail from a list of notes"""


def send_mail(mail_list):
    """Send an email containing contents of notes list scheduled for this run"""

    with smtplib.SMTP_SSL(
        EMAIL["HOST"], EMAIL["PORT"], context=ssl.create_default_context()
    ) as server:
        server.login(EMAIL["USER"], EMAIL["PASS"])
        for r in RECEIVERS:
            server.sendmail(EMAIL["USER"], r, mail_list)


def update_schedule(mail_list):
    """If a note was mailed, update in database"""


def main():
    create_schema()

    mail_list = []

    for note in notes_list(NOTE_DIRS):
        try:
            # Add max notes limit here
            if is_note_scheduled(note):
                mail_list.append(note)
        except ScheduleNotFound:
            create_note_schedule(note, SCHEDULE_DAYS)
        except ScheduleExhausted:
            # Check if end with schedule or send every last scheduled day
            pass

    # send_mail(mail_list)

    update_schedule(mail_list)


if __name__ == "__main__":
    main()
