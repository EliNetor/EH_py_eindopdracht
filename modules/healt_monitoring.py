import psutil
import time
from datetime import datetime
import os

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

# Functie om logbestand te schrijven
def log_health_metrics():
    # Zorg ervoor dat de map 'logs' bestaat
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "health_metrics.log")
    
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Haal CPU-gebruik
        cpu_usage = get_cpu_usage()

        # Haal RAM-gebruik
        ram_percent, ram_used, ram_total = get_ram_usage()

        # Haal netwerkactiviteit
        bytes_sent, bytes_recv = get_network_activity()

        # Formatteer rapport
        log_entry = (
            "=================================\n"
            f"Timestamp       : {timestamp}\n"
            f"CPU Usage       : {cpu_usage}%\n"
            f"RAM Usage       : {ram_percent}% ({ram_used / (1024**2):.2f} MB / {ram_total / (1024**2):.2f} MB)\n"
            f"Network Sent    : {bytes_sent / (1024**2):.2f} MB\n"
            f"Network Received: {bytes_recv / (1024**2):.2f} MB\n"
            "=================================\n"
        )

        # Schrijf naar logbestand
        with open(log_file, "a") as file:
            file.write(log_entry)

        # Wacht 5 seconden voordat het opnieuw meet
        time.sleep(5)

if __name__ == "__main__":
    log_health_metrics()
