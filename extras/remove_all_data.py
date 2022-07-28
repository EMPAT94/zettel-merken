"""This script cleans up zettel-merken data,\
    specifically systemd units and database file."""


import os
from pathlib import Path
from subprocess import run

HOME = Path("~").expanduser()
APP_PATH = HOME / ".config" / "zettel_merken"

if not APP_PATH.exists():
    APP_PATH = HOME / "zettel_merken"

if APP_PATH.exists():
    (APP_PATH / "zettel_merken.db").unlink(missing_ok=True)

if os.name == "posix":
    CONF_DIR = Path("~/.config/systemd/user").expanduser().resolve()
    run("systemctl --user disable --now zettel_merken.timer", shell=True)
    run("systemctl --user disable --now zettel_merken.service", shell=True)
    (CONF_DIR / "zettel_merken.timer").unlink(missing_ok=True)
    (CONF_DIR / "zettel_merken.service").unlink(missing_ok=True)
