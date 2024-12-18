import psutil
import time
from datetime import datetime
import os

# Function to get CPU usage
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

# Function to get RAM usage
def get_ram_usage():
    mem = psutil.virtual_memory()
    return mem.percent, mem.used, mem.total

# Function to get network activity for a specific IP address
def get_network_activity(target_ip):
    net_io = psutil.net_if_addrs()
    net_counters = psutil.net_io_counters(pernic=True)

    for interface, addresses in net_io.items():
        for addr in addresses:
            if addr.address == target_ip:
                if interface in net_counters:
                    stats = net_counters[interface]
                    return stats.bytes_sent, stats.bytes_recv

    return 0, 0  # Return 0 if the target IP is not found

# Function to log health metrics
def log_health_metrics(target_ip):
    # Create logs directory if it does not exist
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # Use the target IP as the filename
    log_file = os.path.join(log_dir, f"{target_ip}.log")

    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Get CPU usage
        cpu_usage = get_cpu_usage()

        # Get RAM usage
        ram_percent, ram_used, ram_total = get_ram_usage()

        # Get network activity for the target IP
        bytes_sent, bytes_recv = get_network_activity(target_ip)

        log_entry = (
            "=================================\n"
            f"Timestamp       : {timestamp}\n"
            f"CPU Usage       : {cpu_usage}%\n"
            f"RAM Usage       : {ram_percent}% ({ram_used / (1024**2):.2f} MB / {ram_total / (1024**2):.2f} MB)\n"
            f"Network Sent    : {bytes_sent / (1024**2):.2f} MB\n"
            f"Network Received: {bytes_recv / (1024**2):.2f} MB\n"
            "=================================\n"
        )

        # Write to file
        with open(log_file, "a") as file:
            file.write(log_entry)

        # Scan interval
        time.sleep(5)

if __name__ == "__main__":
    target_ip = input("Enter the target IP address: ")
    log_health_metrics(target_ip)
