#!/usr/bin/env python3
import sys
import os

def check_module_installed():
    """
    Checks if the 'paramiko' module is installed. If not, provides instructions to install it.
    """
    try:
        __import__('paramiko')
    except ImportError:
        print("Module 'paramiko' is not installed. Please install it using the following command:")
        print("pip install paramiko")
        sys.exit(1)

def create_ssh_client(server_ip, user, key_file, port=22):
    """
    Creates an SSH client to connect to the server using an SSH key.
    """
    import paramiko

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.load_system_host_keys()
        client.connect(server_ip, port=port, username=user, key_filename=key_file)
        print(f"Successfully connected to {server_ip} on port {port}.")
    except paramiko.AuthenticationException:
        print("Authentication failed, please check your SSH key")
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
    check_module_installed()

    if len(sys.argv) < 5:
        print("Usage: script.py <server_ip> <service_name> <username> <action> <ssh_key_file> [ssh_port]")
        sys.exit(1)

    server_ip = sys.argv[1]
    service_name = sys.argv[2]
    username = sys.argv[3]
    action = sys.argv[4]
    ssh_key_file = sys.argv[5]
    ssh_port = int(sys.argv[6]) if len(sys.argv) == 7 else 22

    if not os.path.exists(ssh_key_file):
        print(f"SSH key file {ssh_key_file} not found")
        sys.exit(1)

    ssh_client = create_ssh_client(server_ip, username, ssh_key_file, ssh_port)
    
    try:
        manage_service(ssh_client, service_name, action)
    except Exception as e:
        print(f'An error occurred: {e}')
    finally:
        ssh_client.close()

if __name__ == "__main__":
    main()
