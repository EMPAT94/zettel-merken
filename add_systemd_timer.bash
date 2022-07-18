#!/usr/bin/env bash
#
# USAGE:
#
# zettel-merken $ ./add_systemd_timer.bash
#
# DESCRIPTION:
#
# This nifty little script creates systemd user units
# for running zettel-merken once per day.


set -euo pipefail
IFS=$'\n\t'

# Directory where systemd user units reside
CONF_DIR=$HOME/.config/systemd/user

# Create the directory if it does not already exists
mkdir -p $CONF_DIR

# Create zettel-merken.timer unit
echo "\
[Unit]
Description=Zettel Merken Daily Review Timer

[Timer]
Persistent=true
OnCalendar=Daily
OnBootSec=120

[Install]
WantedBy=timers.target\
" > $CONF_DIR/zettel-merken.timer

# Create zettel-merken.service unit
echo "\
[Unit]
Description=Zettel Merken Daily Review Service

[Service]
Type=simple
ExecStart=$PWD/zettel_merken.py

[Install]
WantedBy=default.target\
" > $CONF_DIR/zettel-merken.service

# Reload systemd units
systemctl --user daemon-reload

# Enable zettel-merken timer
systemctl --user enable --now zettel-merken.timer

# Ensure everything worked fine
systemctl --user status zettel-merken.timer

# Check your zettel-merken logs like so:
# $ journalctl --user -u zettel-merken
