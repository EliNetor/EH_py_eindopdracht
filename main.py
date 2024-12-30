import argparse
import subprocess
import sys
import os
from datetime import date

def run_metrics_logger(username):
    try:
        subprocess.run(
            [sys.executable, "./modules/healt_monitoring.py", username],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(e)

def run_backup(ip, username, directory):
    try:
        subprocess.run(
            [sys.executable, "./modules/backup_drive.py", "-i", ip, "-u", username, "-d", directory],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(e)

def run_commands(username):
    try:
        subprocess.run(
            [sys.executable, "./modules/commandos.py", "-u", username],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(e)

def git_operations(repo_path, commit_message):
    try:
        os.chdir(repo_path)
        
        subprocess.run(["git", "add", "."], check=True)
        
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        
        subprocess.run(["git", "push"], check=True)
        
        print(f"pushed from {repo_path}")
    except Exception as e:
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
    parser.add_argument(
        "-d", "--directory",
        help="Select directory to backup"
    )
    parser.add_argument(
        "-c", "--commands",
        action="store_true",
        help="run commands on hosts from github file"
    )

    args = parser.parse_args()

    try:
        if args.machine_user:
            run_metrics_logger(args.username)
        if args.backup and args.directory:
            run_backup(args.backup, args.username, args.directory)
        if args.commands:
            run_commands(args.username)
    except KeyboardInterrupt:
        git_path = "./git_repo/ethical_hacking_python/"
        git_message = f"Logs from {date.today()}"
        git_operations(git_path, git_message)

if __name__ == "__main__":
    main()
