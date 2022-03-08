#!/usr/bin/env bash

conf_dir=$HOME/.config/systemd/user

echo Creating directoy for systemd in .config
mkdir -p $conf_dir
echo

echo Creating zettel-merken.timer
echo "\
[Unit]
Description=Zettel Merken Email Timer

[Timer]
Persistent=true
OnCalendar=Daily

[Install]
WantedBy=timers.target\
" > $conf_dir/zettel-merken.timer
echo

echo Creating zettel-merken.service
echo "\
[Unit]
Description=Zettel Merken Email Service

[Service]
Type=simple
ExecStart=${PWD}/src/server.js

[Install]
WantedBy=default.target\
" > $conf_dir/zettel-merken.service
echo

echo Reloading systemd daemon
systemctl --user daemon-reload
echo

echo Starting timer, autostarts on boot
systemctl --user enable --now zettel-merken.timer
echo

echo Ensuring timer is active
systemctl --user status zettel-merken.timer
echo
