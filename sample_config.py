# ---------------------------------------------------------------------------- #
# NOTE_DIRS:
#
# List of paths (preferably absolute) of directories containing note files.
# Note that currently, recursive searching inside directories in not present.
# ---------------------------------------------------------------------------- #

NOTE_DIRS = ("./sample_folder/note_folder_1", "./sample_folder/note_folder_2")


# ---------------------------------------------------------------------------- #
# EMAIL:
#
# Sender's email details.
# See https://support.google.com/accounts/answer/185833 for gmail app-passwords.
# ---------------------------------------------------------------------------- #

EMAIL = {
    "USER": "sender@gmail.com",
    "PASS": "senderapppassword",
    "HOST": "smtp.gmail.com",
    "PORT": 465,
}


# ---------------------------------------------------------------------------- #
# RECEIVERS:
#
# List of recepients' email ids.
# ---------------------------------------------------------------------------- #

RECEIVERS = ("receiver1@gmail.com", "receiver2@gmail.com")


# ---------------------------------------------------------------------------- #
# DB_PATH:
#
# Path of sqlite3 database used by zettel_merken.
# Note that folders are *NOT* automatically created!
# ---------------------------------------------------------------------------- #

DB_PATH = "/tmp/zettel_merken.test.db"


# ---------------------------------------------------------------------------- #
# SCHEDULE_DAYS:
#
# Each value represents a day from which the note was created.
# So if a note is created on say, 21st August, then the schedule
# for email would be -
#     1 = 22nd August
#     3 = 24th August
#     7 = 28th August and so on
# ---------------------------------------------------------------------------- #

SCHEDULE_DAYS = (1, 3, 7, 14, 30, 60, 120)


# ---------------------------------------------------------------------------- #
# MAX_NOTES_PER_MAIL:
#
# Maximum count of notes to be sent in one email.
# ---------------------------------------------------------------------------- #

MAX_NOTES_PER_MAIL = 10


# ---------------------------------------------------------------------------- #
# IGNORE_FILES:
#
# List of files (names, not paths) to be excluded from note list.
# ---------------------------------------------------------------------------- #

IGNORE_FILES = ("ignore-file.md",)


# ---------------------------------------------------------------------------- #
# INCLUDE_EXT:
#
# List of file extentions to determine if a file should be considered a note.
# Note the period in extension prefix, it is required
# ---------------------------------------------------------------------------- #

INCLUDE_EXT = (".md", ".txt", ".org", ".norg")
