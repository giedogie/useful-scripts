#!/usr/bin/env python3
import subprocess

# Definiowanie czasów bezczynności (w sekundach)
LOGOUT_TIME = 10   # 5 minut
SUSPEND_TIME = 600  # 10 minut
HIBERNATE_TIME = 1200  # 20 minut

def run_swayidle():
    # Utworzenie polecenia swayidle
    command = f"""
    swayidle \\
        timeout {LOGOUT_TIME} 'swaylock' \\
        timeout {SUSPEND_TIME} 'systemctl suspend' \\
        timeout {HIBERNATE_TIME} 'systemctl hibernate' \\
        before-sleep 'systemctl hibernate'
    """

    # Uruchomienie swayidle
    subprocess.run(command, shell=True, check=True)

if __name__ == "__main__":
    run_swayidle()