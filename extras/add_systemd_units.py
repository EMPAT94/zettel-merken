#!/usr/bin/env python

# USAGE:
#
# zettel-merken $ python extras/add_systemd_timer.py
#
# DESCRIPTION:
#
# This nifty little script creates systemd user units
# for running zettel-merken once per day.

import os
from subprocess import run
from pathlib import Path

if os.name != "posix":
    print("This script for only systemd users!")
    exit()

MAIN_DIR = Path(__file__).parent.parent
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
        f"""\
            [Unit]
            Description=Zettel Merken Daily Review Service

            [Service]
            Type=simple
            ExecStart=/usr/bin/python {MAIN_DIR}

            [Install]
            WantedBy=default.target\
            """
    )

# Check if unit file was successfully created
# $ less ~/.config/systemd/user/zettel_merken.service

# Reload systemd units
run("systemctl --user daemon-reload", shell=True)

# Enable zettel-merken timer
run("systemctl --user enable --now zettel_merken.timer", shell=True)

# Ensure everything worked fine
run("systemctl --user status zettel_merken.timer", shell=True)

# Check your zettel-merken logs:
# $ journalctl --user -u zettel-merken
