import os
from contextlib import ExitStack
from pathlib import Path
from collections.abc import Iterator

from .config import Config


def get_notes_list(config: Config) -> Iterator[Path]:
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
    home = Path.home()

    if (home / ".config").exists():
        app_path = home / ".config" / "zettel_merken"
    else:
        app_path = home / "zettel_merken"

    if not app_path.exists():
        os.mkdir(app_path)

    return app_path


def get_mail_content(notes: list[Path]) -> str:
    with ExitStack() as stack:
        files = [stack.enter_context(open(note)) for note in notes]
        return "\n\n".join(file.read() + "\n\n" for file in files)
