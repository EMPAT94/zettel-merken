import os
from contextlib import ExitStack
from pathlib import Path
from collections.abc import Iterator
from subprocess import run

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


def add_systemd_units():
    if os.name != "posix":
        print("This script for only systemd users!")
        exit()

    CONF_DIR = Path("~/.config/systemd/user").expanduser().resolve()
    TIMER_UNIT = CONF_DIR / "zettel_merken.timer"
    SERVICE_UNIT = CONF_DIR / "zettel_merken.service"

    if not CONF_DIR.exists():
        os.mkdir(CONF_DIR)

    with open(TIMER_UNIT, "w") as timer:
        timer.write(
            """\
            [Unit]
            Description=Zettel Merken Daily Review Timer
            After=network-online.target

            [Timer]
            Persistent=true
            OnCalendar=Daily
            OnBootSec=300

            [Install]
            WantedBy=timers.target\
            """
        )

    with open(SERVICE_UNIT, "w") as service:
        service.write(
            """\
            [Unit]
            Description=Zettel Merken Daily Review Service

            [Service]
            Type=simple
            ExecStart=/usr/bin/python -m zettelmerken

            [Install]
            WantedBy=default.target\
            """
        )

    run("systemctl --user daemon-reload", shell=True)
    run("systemctl --user enable --now zettel_merken.timer", shell=True)
    run("systemctl --user status zettel_merken.timer", shell=True)


def remove_systemd_units():
    HOME = Path("~").expanduser()
    APP_PATH = HOME / ".config" / "zettel_merken"

    if not APP_PATH.exists():
        APP_PATH = HOME / "zettel_merken"

    if APP_PATH.exists():
        (APP_PATH / "zettel_merken.db").unlink(missing_ok=True)

    if os.name != "posix":
        print("This script for only systemd users!")
        exit()

    CONF_DIR = Path("~/.config/systemd/user").expanduser().resolve()
    run("systemctl --user disable --now zettel_merken.timer", shell=True)
    run("systemctl --user disable --now zettel_merken.service", shell=True)
    (CONF_DIR / "zettel_merken.timer").unlink(missing_ok=True)
    (CONF_DIR / "zettel_merken.service").unlink(missing_ok=True)
