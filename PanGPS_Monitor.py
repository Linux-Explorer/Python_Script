import time
import subprocess
from datetime import datetime

SERVICE_NAME = "PanGPS"
CHECK_INTERVAL = 60  # seconds

def write_log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def is_service_running():
    try:
        result = subprocess.run(
            ["sc", "query", SERVICE_NAME],
            capture_output=True,
            text=True
        )

        return "RUNNING" in result.stdout

    except Exception as e:
        write_log(f"Error checking service: {e}")
        return False

def start_service():
    try:
        write_log(f"Starting {SERVICE_NAME} service...")
        subprocess.run(
            ["sc", "start", SERVICE_NAME],
            capture_output=True,
            text=True
        )

        time.sleep(5)

        if is_service_running():
            write_log(f"{SERVICE_NAME} started successfully.")
        else:
            write_log(f"Failed to start {SERVICE_NAME}.")

    except Exception as e:
        write_log(f"Error starting service: {e}")

write_log("PanGPS Monitoring Started")

while True:
    try:
        if not is_service_running():
            write_log(f"{SERVICE_NAME} is STOPPED")
            start_service()
        else:
            write_log(f"{SERVICE_NAME} is RUNNING")

    except Exception as e:
        write_log(f"Unexpected Error: {e}")

    time.sleep(CHECK_INTERVAL)