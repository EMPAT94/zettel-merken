# ---------------------------------------------------------------------------- #
# NOTE_DIRS:
# ---------------------------------------------------------------------------- #

NOTE_DIRS = ("./sample_folder/note_folder_1", "./sample_folder/note_folder_2")

# ---------------------------------------------------------------------------- #
#
# SCHEDULE_DAYS:
#
# Each value represents a day from which the note was created.
#
# So if a note is created on say, 21st August 2022, then the schedule
# for email would be -
#     1 = 22nd August
#     3 = 24th August
#     7 = 28th August and so on
#
# The default schedule is set considering a note (zettel) to be new
# knowledge without prior experience.
# ---------------------------------------------------------------------------- #
SCHEDULE_DAYS = (1, 3, 7, 14, 30, 60, 120)

# ---------------------------------------------------------------------------- #
# DB_PATH:
# ---------------------------------------------------------------------------- #
DB_PATH = "zettel_merken.test.db"


# ---------------------------------------------------------------------------- #
# EMAIL:
# https://support.google.com/accounts/answer/185833
# ---------------------------------------------------------------------------- #
EMAIL = {
    "USER": "sender@gmail.com",
    "PASS": "senderapppassword",
    "HOST": "smtp.gmail.com",
    "PORT": 465,
}

# ---------------------------------------------------------------------------- #
# RECEIVERS:
# ---------------------------------------------------------------------------- #
RECEIVERS = ("receiver1@gmail.com", "receiver2@gmail.com")

# ---------------------------------------------------------------------------- #
# MAX_NOTES_PER_MAIL:
# ---------------------------------------------------------------------------- #
MAX_NOTES_PER_MAIL = 10


# ---------------------------------------------------------------------------- #
# IGNORE_FILES:
# ---------------------------------------------------------------------------- #
IGNORE_FILES = ("index.md",)
