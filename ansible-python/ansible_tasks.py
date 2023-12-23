#!/usr/bin/env python3
import logging
import subprocess
import platform
import distro
import configparser
import os

def setup_logging(config):
    """ Sets up the logging based on the configuration file. """
    if config.getboolean('logging', 'enabled', fallback=True):
        level = getattr(logging, config.get('logging', 'level', fallback='INFO'))
        log_file = config.get('logging', 'file', fallback=None)
        logging.basicConfig(filename=log_file, level=level, 
                            format='%(asctime)s - %(levelname)s - %(message)s', 
                            datefmt='%Y-%m-%d %H:%M:%S')
    else:
        logging.disable(logging.CRITICAL)

def get_linux_distribution():
    """ Detects the Linux distribution running on the machine. """
    try:
        return distro.id()
    except:
        return platform.system()

class LinuxSystemManager:
    def __init__(self, config):
        self.config = config
        self.distro = get_linux_distribution()

    def update_system(self):
        """ Updates the system based on the Linux distribution. """
        logging.info("Starting system update...")
        env = os.environ.copy()
        env["DEBIAN_FRONTEND"] = "noninteractive"
        try:
            if self.distro in ["ubuntu", "debian"]:
                subprocess.run(["sudo", "apt-get", "update"], check=True, env=env)
                subprocess.run(["sudo", "apt-get", "upgrade", "-y", "-o", "Dpkg::Options::=--force-confnew"], check=True, env=env)
            elif self.distro in ["almalinux", "centos", "fedora"]:
                subprocess.run(["sudo", "dnf", "update", "-y"], check=True)  # DNF does not need the env variable
            logging.info("System update completed successfully.")
        except Exception as e:
            logging.error(f"Error updating system: {e}")

    def install_tools(self):
        """ Installs tools based on the Linux distribution. """
        if self.distro in ["ubuntu", "debian"]:
            packages = self.config.get('packages', 'ubuntu').split(',')
        elif self.distro in ["almalinux", "centos", "fedora"]:
            packages = self.config.get('packages', 'rhel').split(',')
        logging.info(f"Installing tools: {packages}")
        try:
            for tool in packages:
                if tool.strip():  # Ensure the line is not empty
                    subprocess.run(["sudo", "apt-get" if self.distro in ["ubuntu", "debian"] else "dnf", "install", "-y", tool.strip()], check=True)
            logging.info("Tools installed successfully.")
        except Exception as e:
            logging.error(f"Error installing tools: {e}")

    def set_timezone(self):
        """ Sets the system timezone from the configuration file. """
        timezone = self.config.get('timezone', 'zone')
        logging.info(f"Setting timezone to {timezone}")
        try:
            subprocess.run(["sudo", "timedatectl", "set-timezone", timezone], check=True)
            logging.info("Timezone set successfully.")
        except Exception as e:
            logging.error(f"Error setting timezone: {e}")

    def update_ssh_config(self):
        """ Updates the SSH configuration file with the differences from the template. """
        template_path = self.config.get('ssh', 'template_path')
        ssh_config_path = '/etc/ssh/sshd_config'
        logging.info("Updating SSH configuration")
        try:
            with open(ssh_config_path, 'r') as file:
                current_config = file.read()

            with open(template_path, 'r') as file:
                template_config = file.read()

            updated_config = self.merge_configs(current_config, template_config)

            with open(ssh_config_path, 'w') as file:
                file.write(updated_config)
            logging.info("SSH configuration updated successfully.")
        except Exception as e:
            logging.error(f"Error updating SSH configuration: {e}")

    def merge_configs(self, current_config, template_config):
        """ Merges the current config with the template, updating only differing parts. """
        current_lines = current_config.splitlines()
        template_lines = template_config.splitlines()

        merged_config = []
        for line in template_lines:
            if line.strip() and not line.startswith("#"):
                key = line.split()[0]
                matching_lines = [l for l in current_lines if l.startswith(key)]
                if matching_lines:
                    merged_config.append(matching_lines[0])
                else:
                    merged_config.append(line)
            else:
                merged_config.append(line)

        return "\n".join(merged_config)

    def restart_ssh_service(self):
        """ Restarts the SSH service. """
        logging.info("Restarting SSH service")
        try:
            service_name = "ssh" if self.distro in ["ubuntu", "debian"] else "sshd"
            subprocess.run(["sudo", "systemctl", "restart", service_name], check=True)
            logging.info(f"SSH service ({service_name}) restarted successfully.")
        except Exception as e:
            logging.error(f"Error restarting SSH service ({service_name}): {e}")


    def configure_firewall(self):
        """ Configures and enables the firewall based on the Linux distribution. """
        if self.distro in ["ubuntu", "debian"]:
            self.configure_ufw()
            self.enable_ufw()
        elif self.distro in ["almalinux", "centos", "fedora"]:
            self.enable_firewalld()
            self.configure_firewalld()
            

    def configure_ufw(self):
        """ Configures UFW firewall rules from the configuration file. """
        ufw_rules = self.config.get('ufw', 'rules').splitlines()
        logging.info("Configuring UFW firewall")
        try:
            for rule in ufw_rules:
                if rule.strip():  # Ensure the line is not empty
                    subprocess.run(["sudo", "ufw"] + rule.strip().split(), check=True)
            logging.info("UFW firewall configured successfully.")
        except Exception as e:
            logging.error(f"Error configuring UFW: {e}")

    def enable_ufw(self):
        """ Enables UFW firewall without interaction. """
        logging.info("Enabling UFW firewall")
        try:
            subprocess.run(["sudo", "ufw", "--force", "enable"], check=True)
            subprocess.run(["sudo", "ufw", "reload"], check=True)
            logging.info("UFW firewall enabled and reloaded successfully.")
        except Exception as e:
            logging.error(f"Error enabling or reloading UFW: {e}")

    def enable_firewalld(self):
        """ Enables Firewalld service without interaction. """
        logging.info("Enabling Firewalld service")
        try:
            subprocess.run(["sudo", "systemctl", "start", "firewalld"], check=True)
            subprocess.run(["sudo", "systemctl", "enable", "firewalld"], check=True)
            logging.info("Firewalld service enabled successfully.")
        except Exception as e:
            logging.error(f"Error enabling Firewalld service: {e}")

    def disable_selinux(self):
        """ Temporarily disables SELinux on systems where it is installed. """
        if self.distro not in ["ubuntu", "debian"]:
            logging.info("Disabling SELinux")
            try:
                subprocess.run(["sudo", "setenforce", "0"], check=True)
                logging.info("SELinux has been disabled.")
            except Exception as e:
                logging.error(f"Error disabling SELinux: {e}")
        else:
            logging.info("SELinux disablement skipped, not required for this distribution.")

    
    """def configure_firewalld(self):
         Configures Firewalld firewall rules from the configuration file. 
        firewalld_rules = self.config.get('firewalld', 'rules').splitlines()
        logging.info("Configuring Firewalld firewall")
        try:
            for rule in firewalld_rules:
                if rule.strip():
                    command = ["sudo", "firewall-cmd"] + rule.strip().split()
                    logging.info(f"Executing command: {' '.join(command)}")
                    subprocess.run(command, check=True)
            subprocess.run(["sudo", "firewall-cmd", "--reload"], check=True)
            logging.info("Firewalld configured and reloaded successfully.")
        except Exception as e:
            logging.error(f"Error configuring Firewalld: {e}")
    """
    def configure_firewalld(self):
        """ Testowy konfigurator Firewalld. """
        logging.info("Testing Firewalld configuration")
        try:
            subprocess.run(["sudo", "firewall-cmd", "--permanent", "--add-port=3033/tcp"], check=True)
            subprocess.run(["sudo", "firewall-cmd", "--reload"], check=True)
            logging.info("Testowy Firewalld configured and reloaded successfully.")
        except Exception as e:
            logging.error(f"Error in test configuration of Firewalld: {e}")


    def reboot_system(self):
        """ Reboots the system, ensuring all logs are written before rebooting. """
        logging.info("Rebooting the system")
        try:
            logging.shutdown()  # Flush and close all log handlers
            subprocess.run(["sudo", "reboot"], check=True)
        except Exception as e:
            logging.error(f"Error rebooting the system: {e}")

def main():
    # Wczytywanie pliku konfiguracyjnego
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Ustawienie logowania
    setup_logging(config)

    # Inicjalizacja menedżera systemu z konfiguracją
    system_manager = LinuxSystemManager(config)

    # Tymczasowe wyłączenie SELinux
    system_manager.disable_selinux()

    # Wywołanie metod menedżera systemu
    system_manager.update_system()
    system_manager.install_tools()
    system_manager.set_timezone()
    system_manager.update_ssh_config()
    system_manager.configure_firewall()
    system_manager.restart_ssh_service()
    #system_manager.reboot_system()

if __name__ == "__main__":
    main()

