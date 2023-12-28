#!/usr/bin/env python3
import subprocess
import os

# Informing the user about the service
print("Initializing a Containerized System Monitor.")
print("This service will be announced on port 5000.")

def check_docker_installed():
    try:
        subprocess.run(["docker", "--version"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    
# Install Docker instruction for Debian-based systems
def install_docker_instructions():
    print("\nDocker is not installed on your system.")
    print("To install Docker, run the following commands:")
    print("sudo apt update")
    print("sudo apt install docker.io")

# Build and run the docker container
def build_and_run_container():
    os.system("docker build -t g-monit .")
    os.system("docker run --name g-monit -it -d --restart unless-stopped -p 5000:5000 g-monit")
    print("\nDocker image named 'g-monit' has been built and is running.")
    print("The service is now accessible on localhost:5000.")

if __name__ == "__main__":
    if check_docker_installed():

        build_and_run_container()
    
    else:
        install_docker_instructions()