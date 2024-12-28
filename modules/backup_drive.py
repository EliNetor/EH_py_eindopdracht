import dropbox
import paramiko
from io import BytesIO
from datetime import datetime
import argparse

def read_access_token():
    token_file_path = 'token.txt'
    try:
        with open(token_file_path, 'r') as f:
            access_token = f.read().strip()  
            return access_token
    except FileNotFoundError:
        print(f"File doesn't exist")
        return None


def initialize_dropbox_client():
    access_token = read_access_token()
    if access_token is None:
        raise Exception("Token error")
    return dropbox.Dropbox(access_token)


def upload_to_dropbox(file_content, dropbox_dest_path):
    dbx = initialize_dropbox_client()
    dbx.files_upload(file_content, dropbox_dest_path, mute=True)
    print(f'File uploaded to dropbox: {dropbox_dest_path}')


def execute_ssh_command(ssh_client, command):
    stdin, stdout, stderr = ssh_client.exec_command(command)
    return stdout.read().decode().strip(), stderr.read().decode().strip()


def download_files_from_remote(remote_ip, remote_directory, ssh_username):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.load_system_host_keys()
        ssh_client.connect(hostname=remote_ip, username=ssh_username)

        
        sftp = ssh_client.open_sftp()

        
        remote_files = sftp.listdir(remote_directory)
        print(f"files on host: {remote_files}")  

        
        for filename in remote_files:
            remote_file_path = remote_directory + '/' + filename  
            print(f"accessing: {remote_file_path}")  
            
            
            with sftp.open(remote_file_path, 'rb') as remote_file:
                file_content = remote_file.read()  

                
                dropbox_dest_path = f'/{remote_ip}/{filename}' 
                upload_to_dropbox(file_content, dropbox_dest_path)

        
        sftp.close()
        ssh_client.close()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Backup files from a remote host to Dropbox")
    
    parser.add_argument('-i', '--ip', required=True, help="ip address of host")
    parser.add_argument('-u', '--username', required=True, help="username of the host")
    
    args = parser.parse_args()
    
  
    remote_ip = args.ip 
    remote_directory = '/home/ubuntu/test'  
    ssh_username = args.username 

    
    download_files_from_remote(remote_ip, remote_directory, ssh_username)
