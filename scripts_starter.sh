#!/bin/bash

# Escaping spaces in the log file path
LOGFILE="/home/nader/Coding/personal projects/automation scripts/Scripts/scripts.log"

# Log the start time
echo "$(date): Script started" >> "$LOGFILE"

# Run system cleanup in a new terminal window
gnome-terminal -- bash -c "./system_cleaner.sh; echo 'System cleaner finished'; exec bash"

# Run the Python organizer script in a new terminal window
gnome-terminal -- bash -c "python3 '/home/nader/Coding/personal projects/automation scripts/Scripts/organizer.py'; echo 'Organizer script finished'; exec bash"

# Log the end time
echo "$(date): Script finished" >> "$LOGFILE"
