import os
import yaml
import paramiko
import requests
import argparse

def fetch_commands_from_github(repo_url, branch="main", file_path="commands.yml", token=None):
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    api_url = f"https://raw.githubusercontent.com/{repo_url}/{branch}/{file_path}"
    
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return yaml.safe_load(response.text)
    else:
        raise Exception(f"Failed to fetch commands: {response.status_code} - {response.text}")

def read_hosts_from_file(filename="hosts.txt"):
    try:
        with open(filename, "r") as file:
            hosts = [line.strip() for line in file if line.strip()]
        return hosts
    except FileNotFoundError:
        raise Exception(f"Host file '{filename}' not found.")

def execute_command_on_host(host, username, command):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        ssh.connect(hostname=host, username=username)
        
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()
        ssh.close()
        
        if error:
            return f"Error on {host}: {error}"
        return f"Output from {host}:\n{output}"
    except Exception as e:
        return f"Failed to execute command on {host}: {e}"

def main():

    parser = argparse.ArgumentParser(description="get username")
    parser.add_argument('-u', '--username', required=True, help="username of the host")
    args = parser.parse_args()

    repo_url = "EliNetor/ethical_hacking_python"  
    token = os.getenv("GITHUB_TOKEN")  
    hosts_file = "ip_addresses.txt"  
    username = args.username
    
    try:
        hosts = read_hosts_from_file(hosts_file)
        
        config = fetch_commands_from_github(repo_url, file_path="commands.yml", token=token)
        commands = config.get("commands", [])
        
        if not commands:
            print("0 commands in file")
            return

        for host in hosts:
            print(f"\n--- Executing on host: {host} ---")
            for command in commands:
                print(f"Running command: {command}")
                output = execute_command_on_host(host, username, command) 
                print(output)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
