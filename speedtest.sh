#!/bin/bash

# Set the project directory
PROJECT_DIR="$(dirname $(realpath $0))"

# Log file location
LOG_FILE="$PROJECT_DIR/internet_speed.log"

# Run speed test and append to log
echo "=== $(date) ===" >> "$LOG_FILE"
speedtest --share --simple >> "$LOG_FILE" 2>&1
echo "" >> "$LOG_FILE"
