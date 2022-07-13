# USAGE: zettel-merken $ python -m pytest [ -q test/ ]

import json
import sqlite3 as db
from pathlib import Path

import zettel_merken as zm
from config_example import DB_PATH, NOTE_DIRS, SCHEDULE_DAYS


def test_create_schema():
    zm.create_schema()
    with db.connect(DB_PATH) as cx:
        cx.cursor().execute("select * from note_schedule")


def test_notes_list():
    notes = zm.notes_list(NOTE_DIRS)
    assert len(list(notes)) == 4


def test_create_note_schedule():
    note = Path("./sample_folder/note_folder_1/note-1.md").absolute()
    zm.create_note_schedule(note, SCHEDULE_DAYS)
    with db.connect(DB_PATH) as cx:
        note_schedule = (
            cx.cursor()
            .execute(f"select schedule from note_schedule where note = '{note}'")
            .fetchone()
        )
        assert len(json.loads(note_schedule[0])) == len(SCHEDULE_DAYS)


def test_is_note_scheduled():
    note = Path("./sample_folder/note_folder_1/note-1.md").absolute()
    assert zm.is_note_scheduled(note) == False
