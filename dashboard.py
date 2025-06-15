import os
import pandas as pd
from flask import Flask, render_template_string, request
from datetime import datetime, timedelta

# Define constants for column names
DOWNLOAD_SPEED = 'Download Speed (Mbps)'
UPLOAD_SPEED = 'Upload Speed (Mbps)'

# Load and parse the log file
def load_data(log_file):
    data = []
    with open(log_file, 'r') as file:
        block = []
        for line in file:
            line = line.strip()
            if line.startswith("==="):
                # Start of a new block
                if block:
                    # Process the previous block
                    try:
                        timestamp_line = block[0]
                        download_line = block[2]
                        upload_line = block[3]

                        timestamp = timestamp_line.split("===")[1].strip()
                        timestamp = pd.to_datetime(timestamp.replace("IST", ""), errors='coerce')
                        download_speed = download_line.split(":")[1].strip().split(" ")[0]
                        upload_speed = upload_line.split(":")[1].strip().split(" ")[0]

                        data.append({
                            'Timestamp': timestamp,
                            DOWNLOAD_SPEED: float(download_speed),
                            UPLOAD_SPEED: float(upload_speed)
                        })
                    except (IndexError, ValueError, TypeError):
                        # Set default values for missing or invalid data
                        data.append({
                            'Timestamp': pd.NaT,
                            DOWNLOAD_SPEED: 0.0,
                            UPLOAD_SPEED: 0.0
                        })
                block = []
            block.append(line)

        # Process the last block
        if block:
            try:
                timestamp_line = block[0]
                download_line = block[2]
                upload_line = block[3]

                timestamp = timestamp_line.split("===")[1].strip()
                timestamp = pd.to_datetime(timestamp.replace("IST", ""), errors='coerce')
                download_speed = download_line.split(":")[1].strip().split(" ")[0]
                upload_speed = upload_line.split(":")[1].strip().split(" ")[0]

                data.append({
                    'Timestamp': timestamp,
                    DOWNLOAD_SPEED: float(download_speed),
                    UPLOAD_SPEED: float(upload_speed)
                })
            except (IndexError, ValueError, TypeError):
                data.append({
                    'Timestamp': pd.NaT,
                    DOWNLOAD_SPEED: 0.0,
                    UPLOAD_SPEED: 0.0
                })

    # Convert to DataFrame
    df = pd.DataFrame(data)
    # Check if DataFrame is empty or missing required columns
    if df.empty or 'Timestamp' not in df.columns:
        print("The log file is empty or improperly formatted.")
        exit()
    # Filter out rows with invalid timestamps
    return df.dropna(subset=['Timestamp'])

# File path to the log file
log_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'internet_speed.log')
data = load_data(log_file)

# Flask app setup
app = Flask(__name__)

# Add filtering options for 1 day, 1 week, 1 month, 3 months, and all data
@app.route('/')
def dashboard():
    data = load_data(log_file)  # Reload the log file dynamically
    filter_option = request.args.get('filter', '1day')

    if filter_option == '1day':
        filtered_data = data[data['Timestamp'] >= (datetime.now() - timedelta(days=1))]
    elif filter_option == '1week':
        filtered_data = data[data['Timestamp'] >= (datetime.now() - timedelta(days=7))]
    elif filter_option == '1month':
        filtered_data = data[data['Timestamp'] >= (datetime.now() - timedelta(days=30))]
    elif filter_option == '3months':
        filtered_data = data[data['Timestamp'] >= (datetime.now() - timedelta(days=90))]
    else:
        filtered_data = data

    return render_template_string(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/apexcharts"></script>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                margin: 0;
                padding: 0;
            }}
            h1 {{
                text-align: center;
                color: #333;
                margin-top: 20px;
            }}
            .chart-container {{
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 20px;
            }}
            #download_chart, #upload_chart {{
                width: 90%;
                max-width: 90vw;
                margin: auto;
            }}
        </style>
    </head>
    <body>
        <h1>Internet Speed Dashboard</h1>
        <div class="chart-container">
            <div id="download_chart"></div>
        </div>
        <div class="chart-container">
            <div id="upload_chart"></div>
        </div>

        <script>
        var downloadOptions = {{
            chart: {{ type: 'line', height: 350, toolbar: {{ show: true, tools: {{ pan: true, zoom: true, zoomin: true, zoomout: true, reset: true }}, autoSelected: 'pan' }} }},
            colors: ['#1E90FF'],
            series: [{{
                name: 'Download Speed',
                data: {filtered_data[DOWNLOAD_SPEED].tolist()}
            }}],
            xaxis: {{
                categories: {filtered_data['Timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist()},
                labels: {{ show: false }},
                tooltip: {{ enabled: true }}
            }},
            title: {{ text: 'Download Speed Over Time', align: 'center', style: {{ fontSize: '16px', color: '#333' }} }}
        }};

        var uploadOptions = {{
            chart: {{ type: 'line', height: 350, toolbar: {{ show: true, tools: {{ pan: true, zoom: true, zoomin: true, zoomout: true, reset: true }}, autoSelected: 'pan' }} }},
            colors: ['#FF6347'],
            series: [{{
                name: 'Upload Speed',
                data: {filtered_data[UPLOAD_SPEED].tolist()}
            }}],
            xaxis: {{
                categories: {filtered_data['Timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist()},
                labels: {{ show: false }},
                tooltip: {{ enabled: true }}
            }},
            title: {{ text: 'Upload Speed Over Time', align: 'center', style: {{ fontSize: '16px', color: '#333' }} }}
        }};

        var downloadChart = new ApexCharts(document.querySelector("#download_chart"), downloadOptions);
        var uploadChart = new ApexCharts(document.querySelector("#upload_chart"), uploadOptions);

        downloadChart.render();
        uploadChart.render();
        </script>
    </body>
    </html>
    """)

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
