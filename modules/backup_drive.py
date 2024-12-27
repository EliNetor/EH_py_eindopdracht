import dropbox
import os

def read_access_token():
    token_file_path = 'token.txt'  
    try:
        with open(token_file_path, 'r') as f:
            access_token = f.read().strip()  
            return access_token
    except FileNotFoundError:
        print(f"File doenst exist")
        return None


def initialize_dropbox_client():
    access_token = read_access_token()
    if access_token is None:
        raise Exception("Token error")
    return dropbox.Dropbox(access_token)

def upload_to_dropbox(local_file_path, dropbox_dest_path):
    dbx = initialize_dropbox_client()
    with open(local_file_path, 'rb') as f:
        dbx.files_upload(f.read(), dropbox_dest_path, mute=True)
    print(f'Uploaded {local_file_path} to Dropbox as {dropbox_dest_path}')

def backup_directory(directory_path):
    for filename in os.listdir(directory_path):
        local_file_path = os.path.join(directory_path, filename)
        if os.path.isfile(local_file_path):
            dropbox_dest_path = f'/backup/{filename}'  # Change the folder name as needed
            upload_to_dropbox(local_file_path, dropbox_dest_path)

if __name__ == '__main__':
    directory_to_backup = r'C:\test\powershell' 
    backup_directory(directory_to_backup)
