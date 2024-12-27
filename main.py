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

def main():
    parser = argparse.ArgumentParser(description="Check resource usage on hosts")
    parser.add_argument(
        "-m", "--machine-user", 
        required=False, 
        help="Specify the SSH username for the hosts."
    )
    args = parser.parse_args()

    if args.machine_user:
        run_metrics_logger(args.machine_user)

if __name__ == "__main__":
    main()