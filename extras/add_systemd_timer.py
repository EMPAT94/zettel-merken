#!/usr/bin/env python

# USAGE:
#
# zettel-merken $ python extras/add_systemd_timer.py
#
# DESCRIPTION:
#
# This nifty little script creates systemd user units
# for running zettel-merken once per day.

from subprocess import run
from pathlib import Path
import os

ZETTEL_DIR = Path(__file__).parent.parent

if os.name != "posix":
    print("This script for only systemd users!")
    exit()

CONF_DIR = Path("~/.config/systemd/user").expanduser().resolve()
if not CONF_DIR.exists():
    os.mkdir(CONF_DIR)

timer_file = CONF_DIR / "zettel_merken.timer"
with open(timer_file, "wt") as timer:
    timer.write(
        """\
            [Unit]
            Description=Zettel Merken Daily Review Timer
            After=network-online.target

            [Timer]
            Persistent=true
            OnCalendar=Daily
            OnBootSec=120

            [Install]
            WantedBy=timers.target\
            """
    )

unit_file = CONF_DIR / "zettel_merken.service"
with open(unit_file, "wt") as unit:
    unit.write(
        f"""\
            [Unit]
            Description=Zettel Merken Daily Review Service

            [Service]
            Type=simple
            ExecStart=/usr/bin/python {ZETTEL_DIR}/src/zettel_merken.py

            [Install]
            WantedBy=default.target\
            """
    )

# Reload systemd units
run("systemctl --user daemon-reload", shell=True, check=True)

# Enable zettel-merken timer
run("systemctl --user enable --now zettel_merken.timer", shell=True)

# Ensure everything worked fine
run("systemctl --user status zettel_merken.timer", shell=True)

# Check your zettel-merken logs:
# $ journalctl --user -u zettel-merken
