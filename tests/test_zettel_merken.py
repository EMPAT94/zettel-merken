import unittest
import sqlite3
import json
from datetime import date
from pathlib import Path

from zettelmerken.db import Db, ScheduleExhausted, ScheduleNotFound
from zettelmerken.config import Config, ConfigNotFound
import zettelmerken.helpers as hlp


config_file = Path("extras", "config.test.json").resolve()

note1 = Path("extras", "test_folder", "note_folder_1", "note-1.md").resolve()
note2 = Path("extras", "test_folder", "note_folder_1", "note-2.txt").resolve()
note3 = Path("extras", "test_folder", "note_folder_2", "note-3.org").resolve()
note4 = Path("extras", "test_folder", "note_folder_2", "note-4.norg").resolve()
notes = [note1, note2, note3, note4]

db_path = Path("/tmp", "zettel_merken.test.db")


class TestConfig(unittest.TestCase):
    def test_get_config(self):
        config = Config.load_from_file(config_file)
        self.assertEqual(config.MAX_NOTES_PER_MAIL, 10)
        self.assertRaises(
            ConfigNotFound,
            Config.load_from_file,
            Path("extras/not_present.json"),
        )


class TestHelpers(unittest.TestCase):
    def test_get_app_path(self):
        home_dir = Path.home()
        config_dir = home_dir / ".config"
        app_dirs = [config_dir / "zettel_merken", home_dir / "zettel_merken"]
        self.assertIn(hlp.get_app_path(), app_dirs)

    def test_get_notes_list(self):
        config = Config.load_from_file(config_file)
        for note in notes:
            self.assertIn(note, list(hlp.get_notes_list(config)))


class TestDb(unittest.TestCase):
    def test_create_schema(self):
        db = Db(db_path, Config.load_from_file(config_file))
        db.create_schema()
        with sqlite3.connect(db.DB_PATH) as cx:
            cx.cursor().execute("SELECT * FROM note_schedule")

    def test_create_note_schedule(self):

        db = Db(db_path, Config.load_from_file(config_file))
        db.create_schema()
        db.create_note_schedule(note1, [1, 3, 6])
        db.create_note_schedule(note2, [0])
        db.create_note_schedule(note3, [0, 1, 2])

        with sqlite3.connect(db.DB_PATH) as cx:
            cu = cx.cursor()

            schedule1 = cu.execute(
                f"SELECT schedule FROM note_schedule WHERE note = '{note1}'"
            ).fetchone()

            assert len(json.loads(schedule1[0])) == 3

            schedule2 = cu.execute(
                f"SELECT schedule FROM note_schedule WHERE note = '{note2}'"
            ).fetchone()

            assert date.toordinal(date.today()) in json.loads(schedule2[0])

            schedule3 = cu.execute(
                f"SELECT schedule FROM note_schedule WHERE note = '{note3}'"
            ).fetchone()

            assert date.toordinal(date.today()) in json.loads(schedule3[0])

    def test_is_note_scheduled(self):
        db = Db(db_path, Config.load_from_file(config_file))
        self.assertFalse(db.is_note_scheduled(note1))
        self.assertTrue(db.is_note_scheduled(note2))
        self.assertTrue(db.is_note_scheduled(note3))
        self.assertRaises(ScheduleNotFound, db.is_note_scheduled, note4)

    def test_update_schedule(self):
        db = Db(db_path, Config.load_from_file(config_file))

        db.update_note_schedule([note2])
        self.assertRaises(ScheduleExhausted, db.is_note_scheduled, note2)

        db.update_note_schedule([note3])

        with sqlite3.connect(db.DB_PATH) as cx:
            cu = cx.cursor()

            schedule3 = cu.execute(
                f"SELECT schedule FROM note_schedule WHERE note = '{note3}'"
            ).fetchone()

            self.assertNotIn(date.toordinal(date.today()), json.loads(schedule3[0]))

    def tearDownClass():
        db = Db(db_path, Config.load_from_file(config_file))

        with sqlite3.connect(db.DB_PATH) as cx:
            cu = cx.cursor()
            cu.execute("DROP TABLE IF EXISTS note_schedule")
            cu.execute("DROP INDEX IF EXISTS idx_note")


if __name__ == "__main__":
    unittest.main()
