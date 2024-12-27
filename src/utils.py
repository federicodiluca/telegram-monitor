import requests
import logging
import os
import shutil
import psutil
import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def fetch_public_ip():
    """Fetch the public IP address from ipinfo.io."""
    url = "https://ipinfo.io/json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        data.pop("readme", None)  # Remove the "readme" field if it exists
        return data
    except requests.RequestException as e:
        logging.error(f"Error fetching IP: {e}")
        return None

def ensure_log_directory(log_dir):
    """Ensure the log directory exists."""
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

def get_log_file_path(log_dir):
    """Get the log file path for the current day."""
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    return os.path.join(log_dir, f"log_{date_str}.txt")

def clean_old_logs(log_dir, retention_days):
    """Remove log files older than the retention period."""
    now = datetime.datetime.now()
    for filename in os.listdir(log_dir):
        file_path = os.path.join(log_dir, filename)
        if os.path.isfile(file_path):
            file_date_str = filename.split("_")[1].split(".")[0]
            file_date = datetime.datetime.strptime(file_date_str, "%Y-%m-%d")
            if (now - file_date).days > retention_days:
                os.remove(file_path)

def log_ip_check(ip_info, log_dir="log"):
    """Log the IP check to a specified log directory."""
    ensure_log_directory(log_dir)
    log_file = get_log_file_path(log_dir)
    ip = ip_info.get("ip")
    city = ip_info.get("city")
    time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"IP Check: {ip} - {city}"
    logging.info(log_message)
    with open(log_file, "a") as f:
        f.write(f"[{time_str}] {log_message}\n")

def log_ip_change(old_ip_info, new_ip_info, log_dir="log", retention_days=7):
    """Log the IP change to a specified log directory."""
    ensure_log_directory(log_dir)
    clean_old_logs(log_dir, retention_days)
    log_file = get_log_file_path(log_dir)
    old_ip = old_ip_info.get("ip")
    old_city = old_ip_info.get("city")
    new_ip = new_ip_info.get("ip")
    new_city = new_ip_info.get("city")
    time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{time_str}] IP CAMBIATO DA {old_ip} - {old_city} A {new_ip} - {new_city}"
    logging.info(log_message)
    with open(log_file, "a") as f:
        f.write(f"{log_message}\n")

def get_system_metrics():
    """Get system metrics such as CPU, RAM, and internet usage."""
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    net_io = psutil.net_io_counters()
    metrics = (
        f"CPU Usage: {cpu_usage}%\n"
        f"RAM Usage: {ram_usage}%\n"
        f"Bytes Sent: {net_io.bytes_sent}\n"
        f"Bytes Received: {net_io.bytes_recv}"
    )
    return metrics