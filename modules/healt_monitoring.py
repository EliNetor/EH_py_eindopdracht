import psutil
import time
from datetime import datetime

# Functie om CPU-gebruik te meten
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

# Functie om RAM-gebruik te meten
def get_ram_usage():
    mem = psutil.virtual_memory()
    return mem.percent, mem.used, mem.total

# Functie om netwerkactiviteit te meten
def get_network_activity():
    net_io = psutil.net_io_counters()
    return net_io.bytes_sent, net_io.bytes_recv

# Functie om het rapport te printen
def log_health_metrics():
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Haal CPU-gebruik
        cpu_usage = get_cpu_usage()

        # Haal RAM-gebruik
        ram_percent, ram_used, ram_total = get_ram_usage()

        # Haal netwerkactiviteit
        bytes_sent, bytes_recv = get_network_activity()

        # Print rapport
        print("=================================")
        print(f"Timestamp       : {timestamp}")
        print(f"CPU Usage       : {cpu_usage}%")
        print(f"RAM Usage       : {ram_percent}% ({ram_used / (1024**2):.2f} MB / {ram_total / (1024**2):.2f} MB)")
        print(f"Network Sent    : {bytes_sent / (1024**2):.2f} MB")
        print(f"Network Received: {bytes_recv / (1024**2):.2f} MB")
        print("=================================")

        # Wacht 5 seconden voordat het opnieuw meet
        time.sleep(5)

if __name__ == "__main__":
    log_health_metrics()
