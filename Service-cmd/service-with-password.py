#!/usr/bin/env python3
import sys
import getpass

def check_and_install_module(module_name):
    """
    Checks if the specified module is installed and installs it if not.
    """
    try:
        __import__(module_name)
        print(f"Module {module_name} is already installed.")
    except ImportError:
        print(f"Installing module {module_name}...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])

def create_ssh_client(server_ip, user, password, port=22):
    """
    Creates an SSH client to connect to the server on a specified port.
    """
    try:
        import paramiko
    except ImportError as e:
        print(f"Error importing Paramiko: {e}")
        sys.exit(1)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(server_ip, port=port, username=user, password=password)
        print(f"Successfully connected to {server_ip} on port {port}.")
    except paramiko.AuthenticationException:
        print("Authentication failed, please check your credentials")
        sys.exit(1)
    except paramiko.SSHException as sshException:
        print(f"Could not establish SSH connection: {sshException}")
        sys.exit(1)
    except Exception as e:
        print(f"Failed to connect to {server_ip}: {e}")
        sys.exit(1)
    return client

def manage_service(ssh_client, service_name, action):
    """
    Manages a specified service on the server based on the action.
    """
    valid_actions = ['start', 'stop', 'restart', 'status']
    if action not in valid_actions:
        print(f"Invalid action: {action}. Valid actions are: {', '.join(valid_actions)}")
        sys.exit(1)

    command = f'sudo systemctl {action} {service_name}'
    stdin, stdout, stderr = ssh_client.exec_command(command)
    output = stdout.read().decode()
    error = stderr.read().decode()
    if output:
        print(f"Service {action} output: {output}")
    if error:
        print(f"Error during service {action}: {error}")
        sys.exit(1)
    print(f"Service {service_name} {action}ed successfully.")

def main():
    """
    Main function controlling the script.
    """
    check_and_install_module('paramiko')

    if len(sys.argv) < 5:
        print("Usage: script.py <server_ip> <service_name> <username> <action> [ssh_port]")
        sys.exit(1)

    server_ip = sys.argv[1]
    service_name = sys.argv[2]
    username = sys.argv[3]
    action = sys.argv[4]
    ssh_port = int(sys.argv[5]) if len(sys.argv) == 6 else 22

    password = getpass.getpass(f'Password for {username}: ')

    ssh_client = create_ssh_client(server_ip, username, password, ssh_port)
    
    try:
        manage_service(ssh_client, service_name, action)
    except Exception as e:
        print(f'An error occurred: {e}')
    finally:
        ssh_client.close()

if __name__ == "__main__":
    main()
