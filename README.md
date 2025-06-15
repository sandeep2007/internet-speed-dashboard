# Internet Speed Dashboard

## Overview

This project provides an Internet Speed Statistics Dashboard that visualizes internet speed data collected by a Raspberry Pi. The dashboard is built using Flask and ApexCharts, and it includes features like filtering data by time ranges (1 day, 1 week, 1 month, 3 months, all).

## Features

- Logs internet speed data using `speedtest-cli`.
- Visualizes data with interactive charts.
- Provides filtering options for various time ranges.
- Automates data collection and dashboard startup using cron jobs and systemd services.

## Prerequisites

1. Python installed on your system.
2. `speedtest-cli` installed for internet speed tests:
   ```bash
   pip install speedtest-cli
   ```
3. Bash installed (Linux systems typically have it pre-installed).

## Setup Instructions

### 1. Clone or Copy the Project

Copy the project files to your desired location. Ensure the following files are included:

- `dashboard.py`
- `install.sh`
- `requirements.txt`
- `internet-speed-dashboard.service`
- `speedtest.sh`

### 2. Create a Virtual Environment

Run the following command to create a virtual environment:

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

Activate the virtual environment:

- On Linux/macOS:
  ```bash
  source venv/bin/activate
  ```
- On Windows:
  ```bash
  venv\Scripts\activate
  ```

### 4. Install Dependencies

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

### 5. Set Up Cron Jobs and Systemd Service

Run the `install.sh` script to set up the cron jobs and systemd service:

```bash
bash install.sh
```

This will:

- Schedule the `speedtest.sh` script to run every 5 minutes.
- Install and enable the `internet-speed-dashboard.service`.

### 6. Start the Dashboard

To manually start the dashboard, run:

```bash
python dashboard.py
```

### 7. Access the Dashboard

Open your browser and navigate to:

```
http://<your-local-ip>:5000
```

### 8. Verify Cron Jobs

Check if the cron jobs are correctly set up:

```bash
crontab -l
```

You should see entries for:

- `*/5 * * * * ~/speedtest.sh`

### 9. Update the Service File

Ensure the `HOME` environment variable is correctly set in the `internet-speed-dashboard.service` file:

```plaintext
Environment="HOME=/home/pi"
```

## Notes

- Ensure the `speedtest.sh` and `dashboard.py` scripts have executable permissions:
  ```bash
  chmod +x speedtest.sh
  chmod +x dashboard.py
  ```
- The `internet_speed.log` file will store the internet speed test results.
- The dashboard will visualize the data from the log file.

## License

This project is licensed under the MIT License.
