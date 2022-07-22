import os

from pathlib import Path
from collections.abc import Iterator

from . import config as cfg


def notes_list(config: cfg.Config) -> Iterator[Path]:
    """Get a list of notes from a list of directories"""

    for dir in config.NOTE_DIRS:
        for path, dirs, files in os.walk(dir, topdown=True):

            # Exclude hidden and user ignored directories
            dirs[:] = (
                d for d in dirs if d not in config.IGNORE_DIRS and not d.startswith(".")
            )

            for file in files:
                if (
                    Path(path, file).suffix in config.INCLUDE_EXT
                    and file not in config.IGNORE_FILES
                ):
                    yield Path(path + os.sep + file).resolve()


def get_app_path() -> Path:
    """Returns ~/.config/zettel_merken or ~/zettel_merken if .config not found"""
    home = Path("~").expanduser()

    if (home / ".config").exists():
        app_path = home / ".config" / "zettel_merken"
    else:
        app_path = home / "zettel_merken"

    if not app_path.exists():
        os.mkdir(app_path)

    return app_path
