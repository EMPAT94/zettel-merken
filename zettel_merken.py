import os
import json
from datetime import date, timedelta
import sqlite3 as db
from pathlib import Path

from config_example import DB_PATH, SCHEDULE_DAYS, NOTE_DIRS


def create_schema():
    """Create database schema for zettel-merken note schedules"""
    with db.connect(DB_PATH) as cx:
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


def is_note_scheduled(note: Path):
    """Check if a note is scheduled for this run"""
    with db.connect(DB_PATH) as cx:
        data = (
            cx.cursor()
            .execute(f"SELECT schedule FROM note_schedule WHERE note = '{note}'")
            .fetchone()
        )

        if not data:
            raise db.DataError("Note not found")

        schedule = json.loads(data[0])

        for ordinal in schedule:
            scheduled_day = date.fromordinal(int(ordinal))
            if not schedule[ordinal] and scheduled_day < date.today():
                return True
            if scheduled_day > date.today():
                return False
        else:
            return False


def create_note_schedule(note: Path, schedule_days: tuple):
    """Create a schedule for a given note"""
    os_stat = os.stat(note)
    stats = json.dumps({"size": os_stat.st_size, "mtime": os_stat.st_mtime})
    schedule = json.dumps(
        {date.toordinal(date.today() + timedelta(s)): None for s in schedule_days}
    )
    with db.connect(DB_PATH) as cx:
        cx.cursor().execute(
            "insert into note_schedule (note, stats, schedule) values (?, ?, ?)",
            [str(note), stats, schedule],
        )


def build_mail(notes: list[Path]):
    """Create a mail from a list of notes"""
    pass


def send_mail(mail: str):
    """Send an email containing notes scheduled for this run"""
    pass


def update_note_schedule(note: str):
    """If a note was mailed, update in database"""
    pass


def main():
    create_schema()

    for note in notes_list(NOTE_DIRS):
        try:
            if is_note_scheduled(note):
                pass
        except db.DataError:
            create_note_schedule(note, SCHEDULE_DAYS)


if __name__ == "__main__":
    main()
