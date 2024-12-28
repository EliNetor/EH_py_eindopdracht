import argparse
import subprocess
import sys

def run_metrics_logger(username):
    try:
        subprocess.run(
            [sys.executable, "./modules/healt_monitoring.py", username],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(e)

def run_backup(ip, username):
    try:
        subprocess.run(
            [sys.executable, "./modules/backup_drive.py", "-i", ip, "-u", username],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(e)

def main():
    parser = argparse.ArgumentParser(description="Check resource usage on hosts")

    parser.add_argument(
        "-u", "--username",
        required=True,
        help="Specify the SSH username for the hosts."
    )
    parser.add_argument(
        "-m", "--machine-user",
        action="store_true",
        help="Run metrics logger for the specified user."
    )
    parser.add_argument(
        "-b", "--backup",
        help="Backup for set host. Specify the IP address."
    )

    args = parser.parse_args()

    if args.machine_user:
        run_metrics_logger(args.username)
    if args.backup:
        run_backup(args.backup, args.username)

if __name__ == "__main__":
    main()
