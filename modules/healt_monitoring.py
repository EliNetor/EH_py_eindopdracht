import paramiko
import time
from datetime import datetime
import os
import argparse

def execute_ssh_command(ssh_client, command):
    stdin, stdout, stderr = ssh_client.exec_command(command)
    return stdout.read().decode().strip(), stderr.read().decode().strip()

def log_health_metrics(target_ip, ssh_client):
    log_dir = "./git_repo/ethical_hacking_python/logs"
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, f"{target_ip}.log")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cpu_usage_cmd = "top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\([0-9.]*\)%* id.*/\1/' | awk '{print 100 - $1}'"
    cpu_usage, _ = execute_ssh_command(ssh_client, cpu_usage_cmd)

    ram_usage_cmd = (
        "free -m | awk 'NR==2{printf \"%s %s %s\", $3, $2, $3*100/$2 }'"
    )
    ram_data, _ = execute_ssh_command(ssh_client, ram_usage_cmd)
    ram_used, ram_total, ram_percent = ram_data.split()

    network_activity_cmd = (
        "cat /proc/net/dev | tail -n +3 | awk '{print $1, $2, $10}'"
    )
    network_data, _ = execute_ssh_command(ssh_client, network_activity_cmd)
    bytes_sent = 0
    bytes_recv = 0
    for line in network_data.splitlines():
        parts = line.split()
        if len(parts) >= 3:
            bytes_recv += int(parts[1])
            bytes_sent += int(parts[2])

    log_entry = (
        "=================================\n"
        f"Timestamp       : {timestamp}\n"
        f"CPU Usage       : {cpu_usage}%\n"
        f"RAM Usage       : {ram_percent}% ({int(ram_used)} MB / {int(ram_total)} MB)\n"
        f"Network Sent    : {bytes_sent / (1024**2):.2f} MB\n"
        f"Network Received: {bytes_recv / (1024**2):.2f} MB\n"
        "=================================\n"
    )

    with open(log_file, "a") as file:
        file.write(log_entry)

    print(f"Metrics for IP {target_ip}:")
    print(log_entry)

def main():
    parser = argparse.ArgumentParser(description="SSH Host Metrics Logger")
    parser.add_argument(
        "username", 
        help="Specify the SSH username for the machines."
    )
    args = parser.parse_args()

    input_file = "ip_addresses.txt"
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    with open(input_file, "r") as file:
        ip_addresses = [line.strip() for line in file if line.strip()]

    if not ip_addresses:
        print("No IP addresses found in the file.")
        return

    ssh_username = args.username  

    while True:
        for ip in ip_addresses:
            try:
                print(f"Connecting to {ip}...")
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=ip, username=ssh_username)

                print(f"Starting metrics logging for IP: {ip}")
                log_health_metrics(ip, ssh_client)
                print(f"Finished metrics logging for IP: {ip}")

                ssh_client.close()

            except Exception as e:
                print(f"Error connecting to {ip}: {e}")

            time.sleep(60)  

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Script terminated by user.")
