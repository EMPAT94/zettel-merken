# USAGE: zettel-merken $ python -m pytest [ -q test/ ]

import json
import sqlite3 as db
from pathlib import Path
from datetime import date, timedelta

import zettel_merken as zm
from config_example import *


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

    note2 = Path("./sample_folder/note_folder_1/note-2.md").absolute()
    zm.create_note_schedule(note2, (0,))

    with db.connect(DB_PATH) as cx:
        cu = cx.cursor()

        schedule1 = cu.execute(
            f"select schedule from note_schedule where note = '{note}'"
        ).fetchone()

        assert len(json.loads(schedule1[0])) == len(SCHEDULE_DAYS)

        schedule2 = cu.execute(
            f"select schedule from note_schedule where note = '{note2}'"
        ).fetchone()

        assert str(date.toordinal(date.today())) in json.loads(schedule2[0])


def test_is_note_scheduled():
    # TODO Also test for ScheduleNotFound and ScheduleExhausted
    note = Path("./sample_folder/note_folder_1/note-1.md").absolute()
    assert zm.is_note_scheduled(note) == False

    note2 = Path("./sample_folder/note_folder_1/note-2.md").absolute()
    assert zm.is_note_scheduled(note2) == True


def test_cleanup():
    with db.connect(DB_PATH) as cx:
        cx.cursor().execute("delete from note_schedule")
        pass
