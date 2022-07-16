# USAGE: zettel-merken $ python -m pytest

import json, sqlite3, pytest
from pathlib import Path
from datetime import date, timedelta

import zettel_merken as zm
from sample_config import *


note1 = Path("./sample_folder/note_folder_1/note-1.md").absolute()
note2 = Path("./sample_folder/note_folder_1/note-2.txt").absolute()
note3 = Path("./sample_folder/note_folder_2/note-3.org").absolute()
note4 = Path("./sample_folder/note_folder_2/note-4.norg").absolute()
notes = [note1, note2, note3, note4]


def test_create_schema():
    zm.create_schema()
    with sqlite3.connect(DB_PATH) as cx:
        cx.cursor().execute("SELECT * FROM note_schedule")


def test_notes_list():
    assert len(list(zm.notes_list(NOTE_DIRS))) == len(notes)


def test_create_note_schedule():
    zm.create_note_schedule(note1, SCHEDULE_DAYS)
    zm.create_note_schedule(note2, (0,))

    with sqlite3.connect(DB_PATH) as cx:
        cu = cx.cursor()

        schedule1 = cu.execute(
            f"SELECT schedule FROM note_schedule WHERE note = '{note1}'"
        ).fetchone()

        assert len(json.loads(schedule1[0])) == len(SCHEDULE_DAYS)

        schedule2 = cu.execute(
            f"SELECT schedule FROM note_schedule WHERE note = '{note2}'"
        ).fetchone()

        assert date.toordinal(date.today()) in json.loads(schedule2[0])


def test_is_note_scheduled():
    assert zm.is_note_scheduled(note1) == False
    assert zm.is_note_scheduled(note2) == True
    with pytest.raises(zm.ScheduleNotFound):
        zm.is_note_scheduled(note3)


def test_build_mail():
    mail_content = zm.build_mail_content(notes)
    expected_content = "\n\n".join(open(note).read() for note in notes)
    assert mail_content == expected_content


# Uncomment to run,
# Must manually check if the mail was received
# def test_send_mail():
#     mail_content = zm.build_mail_content(notes)
#     zm.send_mail(mail_content)


def test_update_schedule():
    zm.update_schedule([note2])
    with pytest.raises(zm.ScheduleExhausted):
        zm.is_note_scheduled(note2)


def test_cleanup():
    with sqlite3.connect(DB_PATH) as cx:
        cu = cx.cursor()
        cu.execute("drop table if exists note_schedule")
        cu.execute("drop index if exists idx_note")
