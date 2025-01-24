import os
from dotenv import load_dotenv
import paramiko

load_dotenv()

# Server details
sftp_host = os.getenv('SFTP_HOST')
sftp_port = os.getenv('SFTP_PORT')
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

remote_file = os.getenv('REMOTE_FILE')


def ftp_upload_file(file):
    remote_file_name = remote_file.format(FILENAME=file)
    # Create an SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the server
    ssh.connect(hostname=sftp_host, port=sftp_port, username=username, password=password)
    sftp = ssh.open_sftp()

    # Upload the file
    sftp.put(file, remote_file_name)
    print(f"File uploaded successfully to {remote_file_name}")

    # Close the connection
    sftp.close()
    ssh.close()

 


def ftp_download_file(file: str):
    server_file_name = f"{file.split('.')[0]}.png"    
 
    # Create an SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the server
    print(f"Connecting to {sftp_host}...")
    ssh.connect(hostname=sftp_host, port=sftp_port, username=username, password=password)
    print("Connected successfully.")

    # Open an SFTP session
    sftp = ssh.open_sftp()

    # Download the file
    print(f"Downloading {server_file_name, file} to ./ ...")
    sftp.get(remote_file.format(FILENAME=server_file_name), f'downloaded_{file}')
    print("File downloaded successfully.")

    # Close the connection
    sftp.close()
    ssh.close()

    return f'downloaded_{file}'

