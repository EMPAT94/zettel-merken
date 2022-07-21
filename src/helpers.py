import os

from pathlib import Path
from collections.abc import Iterator

from config import Config


def notes_list(config: Config) -> Iterator[Path]:
    """Get a list of notes from a list of directories"""

    for dir in config.NOTE_DIRS:
        for path, dirs, files in os.walk(dir, topdown=True):
            dirs[:] = (
                d for d in dirs if d not in config.IGNORE_DIRS and not d.startswith(".")
            )
            for file in files:
                if (
                    Path(file).suffix in config.INCLUDE_EXT
                    and file not in config.IGNORE_FILES
                ):
                    yield Path(path + os.sep + file).resolve()
