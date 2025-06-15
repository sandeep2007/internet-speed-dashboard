#!/bin/bash

# Check if the script is running on Linux
if [[ "$(uname -s)" != "Linux" ]]; then
    echo "This script is intended to run on Linux systems."
    exit 1
fi

# Set the project directory
PROJECT_DIR="$(dirname $(realpath $0))"

# Run the speedtest.sh script once during installation
bash "$PROJECT_DIR/speedtest.sh"

# Add the cron job to crontab
CRON_JOB="*/5 * * * * $PROJECT_DIR/speedtest.sh"

# Check if the cron job already exists
if crontab -l 2>/dev/null | grep -Fxq "$CRON_JOB"; then
    echo "Cron job already exists. No changes made."
else
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "Cron job added successfully."
fi

# Install and enable the systemd service
SERVICE_FILE="$PROJECT_DIR/internet-speed-dashboard.service"
SYSTEMD_PATH="/etc/systemd/system/internet-speed-dashboard.service"

if [ -f "$SERVICE_FILE" ]; then
    sudo cp "$SERVICE_FILE" "$SYSTEMD_PATH"
    sudo systemctl daemon-reload
    sudo systemctl enable internet-speed-dashboard.service
    sudo systemctl start internet-speed-dashboard.service
    echo "Systemd service installed and enabled successfully."
else
    echo "Service file not found at $SERVICE_FILE. Skipping systemd setup."
fi


