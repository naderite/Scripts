#!/bin/bash
LOGFILE="/home/nader/Coding/personal projects/automation scripts/Scripts/scripts.log"

sudo apt-get clean
sudo apt-get autoremove -y

sudo rm -rf /tmp/*
sudo rm -rf ~/.cache/*

sudo find /var/log -type f -name "*.log" -exec rm -f {} \;

rm -rf ~/.local/share/Trash/*

echo "System cleanup completed!" >> "$LOGFILE"
