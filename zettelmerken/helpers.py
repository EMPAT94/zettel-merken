import os
import json
from contextlib import ExitStack
from pathlib import Path
from collections.abc import Iterator
from subprocess import run, call
from inspect import cleandoc
from sys import platform

from .config import Config


HOME = Path("~").expanduser()
if (HOME / ".config").exists():
    APP_PATH = HOME / ".config" / "zettel_merken"
else:
    APP_PATH = HOME / "zettel_merken"

if not APP_PATH.exists():
    os.mkdir(APP_PATH)


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
                    and file.casefold() not in config.IGNORE_FILES
                ):
                    yield Path(path + os.sep + file).resolve()


def get_app_path() -> Path:
    """Returns ~/.config/zettel_merken or ~/zettel_merken if .config not found"""
    return APP_PATH


def get_mail_content(notes: list[Path]) -> str:
    with ExitStack() as stack:
        files = [stack.enter_context(open(note)) for note in notes]
        return "\n\n".join(file.read() + "\n\n" for file in files)


def _add_systemd_units():
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


def _add_launchd_units():
    CONF_DIR = Path("~/Library/LaunchAgents").expanduser().resolve()
    TIMER_UNIT = CONF_DIR / "com.zettelmerken.dailyreview.plist"

    if not CONF_DIR.exists():
        os.mkdir(CONF_DIR)

    with open(TIMER_UNIT, "w") as timer:
        timer.write(
            """\
            <?xml version="1.0" encoding="UTF-8"?>
            <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
            <plist version="1.0">
              <dict>
                <key>Label</key>
                <string>com.zettelmerken.dailyreview</string>
                <key>ServiceDescription</key>
                <string>Zettelmerken Daily Review</string>
                <key>ProgramArguments</key>
                <array>
                  <string>/opt/homebrew/bin/python3</string>
                  <string>-m</string>
                  <string>zettelmerken</string>
                </array>
                <key>RunAtLoad</key>
                <true />
                <key>StartCalendarInterval</key>
                <dict>
                  <key>Hour</key>
                  <integer>0</integer>
                  <key>Minute</key>
                  <integer>10</integer>
                </dict>
                <!-- For Debugging
                <key>StandardErrorPath</key>
                <string>/tmp/com.zettelmerken.dailyreview.err</string>
                <key>StandardOutPath</key>
                <string>/tmp/com.zettelmerken.dailyreview.out</string>
                -->
              </dict>
            </plist>
            """
        )

    run(f"plutil {TIMER_UNIT}", shell=True)
    run(
        f"launchctl load {TIMER_UNIT}",
        shell=True,
    )
    run(f"launchctl enable {TIMER_UNIT}", shell=True)


def add_timer_units():
    if platform == "linux":
        _add_systemd_units()
    elif platform == "darwin":
        _add_launchd_units()
    else:
        print(
            "Unrecognized platform. Adding timer units only works on linux and macos!"
        )
        exit()


def create_config():
    if not (APP_PATH / "config.json").exists():
        with open(APP_PATH / "config.json", "wt") as config:
            dump = json.dumps(
                {
                    "NOTE_DIRS": ["/path/to/notes_folder"],
                    "EMAIL": {
                        "USER": "sender@gmail.com",
                        "PASS": "sampleapppassword",
                        "HOST": "smtp.gmail.com",
                        "PORT": 465,
                    },
                    "RECEIVERS": ["receiver@gmail.com"],
                    "MAX_NOTES_PER_MAIL": 10,
                    "IGNORE_FILES": ["ignore-file.md"],
                    "IGNORE_DIRS": ["ignore-folder"],
                    "INCLUDE_EXT": [".md", ".txt", ".org", ".norg"],
                    "SCHEDULE_DAYS": [1, 3, 7, 14, 30, 60, 120],
                },
            )

            config.write(dump)


def open_config():
    default_editor = "/usr/bin/vi"  # backup, if not defined in environment vars
    path = APP_PATH / "config.json"
    editor = os.environ.get("EDITOR", default_editor)
    call([editor, path])


def show_help():
    help_str = cleandoc(
        """
        USAGE: python -m zettelmerken [OPTION]

        OPTOINS:
            --help    Show this help
            --config  Create and open config.json
            --init    Init systemd units
            --remove  Remove database and systemd units
        """
    )
    print(help_str)


def remove_database():
    if APP_PATH.exists():
        (APP_PATH / "zettel_merken.db").unlink(missing_ok=True)


def remove_systemd_units():
    if os.name != "posix":
        print("This script for only systemd users!")
        exit()

    CONF_DIR = Path("~/.config/systemd/user").expanduser().resolve()
    run("systemctl --user disable --now zettel_merken.timer", shell=True)
    run("systemctl --user disable --now zettel_merken.service", shell=True)
    (CONF_DIR / "zettel_merken.timer").unlink(missing_ok=True)
    (CONF_DIR / "zettel_merken.service").unlink(missing_ok=True)
