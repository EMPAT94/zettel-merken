import os, json, sqlite3

from datetime import date, timedelta
from pathlib import Path

from config import Config


def create_schema(config: Config) -> None:
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


class ScheduleNotFound(BaseException):
    pass


class ScheduleExhausted(BaseException):
    pass


def create_note_schedule(note: Path, config: Config) -> None:
    """Create a schedule for a given note"""

    stats = {"mtime": os.stat(note).st_mtime}
    schedule = sorted(
        date.toordinal(date.today() + timedelta(s)) for s in config.SCHEDULE_DAYS
    )
    sent = []

    with sqlite3.connect(config.DB_PATH) as cx:
        cx.cursor().execute(
            "INSERT INTO note_schedule (note, stats, schedule, sent) VALUES (?, ?, ?, ?)",
            (str(note), json.dumps(stats), json.dumps(schedule), json.dumps(sent)),
        )


def is_note_scheduled(note: Path, config: Config):
    """Check if a note is scheduled for this run"""

    with sqlite3.connect(config.DB_PATH) as cx:
        data = (
            cx.cursor()
            .execute(
                "SELECT schedule FROM note_schedule WHERE note = (?)", (str(note),)
            )
            .fetchone()
        )

        if not data:
            raise ScheduleNotFound("Note data not found.")

        schedule = json.loads(data[0])

        if not schedule:
            raise ScheduleExhausted("Note schedule is empty.")

        today = date.toordinal(date.today())
        for day in schedule:
            if day <= today:
                return True

        return False


def update_note_schedule(notes: list[Path], config: Config) -> None:
    """If a note was mailed, update in database"""

    notes_list = [str(note) for note in notes]

    with sqlite3.connect(config.DB_PATH) as cx:
        cu = cx.cursor()

        notes_to_update = cu.execute(
            "SELECT id, schedule, sent FROM note_schedule WHERE note IN"
            f" ({', '.join('?' * len(notes_list))})",
            notes_list,
        )

        today = date.toordinal(date.today())

        for id, schedule, sent in notes_to_update:
            schedule = json.loads(schedule)
            schedule = schedule[1:]  # Remove first element
            sent = json.loads(sent)
            sent.append(today)  # Append today's date
            cu.execute(
                "UPDATE note_schedule SET schedule=(?), sent=(?) WHERE id=(?)",
                (json.dumps(schedule), json.dumps(sent), id),
            )
