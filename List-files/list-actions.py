#!/usr/bin/env python3
import os
import datetime
import subprocess
import sys
import shutil
import re
import zipfile

# ANSI Colors
COLORS = {
    "RED": "\033[91m",
    "GREEN": "\033[92m",
    "BLUE": "\033[94m",
    "RESET": "\033[0m"
}

def current_formatted_time():
    """Get the current time and format it."""
    return datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

# Global Variables
loaded_list_file = None
log_file_name = f"log_{current_formatted_time()}.txt"

def create_script_separator(action, color="RED", total_length=100):
    """Create a script separator with given action, color, and length."""
    base_string = f" SCRIPT {action} {current_formatted_time()} "
    return f"{COLORS[color]}{base_string.center(total_length, '=')}{COLORS['RESET']}"

def initialize_log_file():
    with open(log_file_name, 'w') as log_file:
        log_file.write(create_script_separator("ACTIONS-LOG STARTED") + '\n')

def write_log(message):
    """Write a log message with a timestamp."""
    with open(log_file_name, 'a') as log_file:
        log_file.write(f"{current_formatted_time()} - {message}\n")

def start():
    """Print the start separator and write to the log."""
    print(create_script_separator("STARTED"))
    write_log("Script started")
def end():
    """Print the end separator and write to the log."""
    print(create_script_separator("ENDED"))
    write_log("Script ended")

def get_file_action_confirmation(action):
    """Get user confirmation for file actions."""
    user_input = input(f"Are you sure you want to {action} these files? (yes/no): ").lower()
    write_log(f"User was asked for confirmation to {action} files. User response: {user_input}")
    return user_input == 'yes'

def process_files_from_list(action, process_function):
    """General function to process files from the loaded list."""
    global loaded_list_file
    if not loaded_list_file:
        print(f"{COLORS['RED']}No list file loaded. Please load a list file first.{COLORS['RESET']}")
        return

    print(f"{action} files from the loaded list file: {loaded_list_file}")
    destination_folder = input("Enter the destination folder path: ")
    if not os.path.exists(destination_folder) or not os.path.isdir(destination_folder):
        print(f"{COLORS['RED']}Destination folder does not exist or is not a directory.{COLORS['RESET']}")
        return

    with open(loaded_list_file, 'r') as file:
        for line in file:
            match = re.search(r'File: (.*), Size:', line)
            if match:
                file_path = match.group(1).strip()
                process_function(file_path, destination_folder)

def copy_file(file_path, destination_folder):
    """Copy a file to the specified destination folder."""
    destination_file = os.path.join(destination_folder, os.path.basename(file_path))
    if not os.path.exists(destination_file):
        shutil.copy(file_path, destination_file)
        print(f"Copied {file_path} to {destination_folder}")
        write_log(f"Copied {file_path} to {destination_folder}")
    else:
        print(f"Skipped {file_path} because it already exists in the destination folder.")
        write_log(f"Skipped {file_path} because it already exists in the destination folder.")

def move_file(file_path, destination_folder):
    """Move a file to the specified destination folder."""
    destination_file = os.path.join(destination_folder, os.path.basename(file_path))
    if not os.path.exists(destination_file):
        shutil.move(file_path, destination_folder)
        print(f"Moved {file_path} to {destination_folder}")
        write_log(f"Moved {file_path} to {destination_folder}")
    else:
        print(f"Skipped {file_path} because it already exists in the destination folder.")
        write_log(f"Skipped {file_path} because it already exists in the destination folder.")


def add_to_archive():
    """Add files from the list to an archive."""
    if not loaded_list_file:
        print(f"{COLORS['RED']}No list file loaded. Please load a list file first.{COLORS['RESET']}")
        write_log("No list file loaded. Please load a list file first.")
        return

    archive_name = input("Enter the archive name (without extension): ")
    destination_folder = input("Enter the destination folder path for the archive: ")
    if not os.path.exists(destination_folder) or not os.path.isdir(destination_folder):
        print(f"{COLORS['RED']}Destination folder does not exist or is not a directory.{COLORS['RESET']}")
        write_log("Destination folder does not exist or is not a directory.")
        return

    archive_path = os.path.join(destination_folder, f"{archive_name}.zip")
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        with open(loaded_list_file, 'r') as file:
            for line in file:
                match = re.search(r'File: (.*), Size:', line)
                if match and os.path.exists(match.group(1).strip()):
                    zipf.write(match.group(1).strip(), os.path.basename(match.group(1).strip()))
            print(f"Created archive {archive_path}")
            write_log(f"Created archive {archive_path}")

def delete_files():
    """Delete files from the list."""
    if not loaded_list_file:
        print(f"{COLORS['RED']}No list file loaded. Please load a list file first.{COLORS['RESET']}")
        write_log("No list file loaded. Please load a list file first.")
        return

    # Rest of the code...

        print(f"{COLORS['RED']}No list file loaded. Please load a list file first.{COLORS['RESET']}")
        write_log("No list file loaded. Please load a list file first.")
        return

    if get_file_action_confirmation("delete"):
        with open(loaded_list_file, 'r') as file:
            for line in file:
                match = re.search(r'File: (.*), Size:', line)
                if match and os.path.exists(match.group(1).strip()):
                    os.remove(match.group(1).strip())
                    print(f"Deleted {match.group(1).strip()}")
                    write_log(f"Deleted {match.group(1).strip()}")
    else:
        print("Deletion canceled.")
        write_log("Deletion canceled.")

def load_list_file():
    """Load a list file."""
    global loaded_list_file
    list_file_path = input(f"Enter the path to the list file to load (or press Enter to go back): ")
    if list_file_path == "":
        return  # Return to the main menu if Enter is pressed
    elif os.path.exists(list_file_path):
        loaded_list_file = list_file_path
        print(f"Loaded list file: {list_file_path}")
        write_log(f"Loaded list file: {list_file_path}")
    else:
        print(f"{COLORS['RED']}File does not exist. Please enter a valid file path.{COLORS['RESET']}")
        write_log("File does not exist. Please enter a valid file path.")

def close_list_file():
    """Close the currently loaded list file."""
    global loaded_list_file
    loaded_list_file = None
    print("Closed the loaded list file.")
    write_log("Closed the loaded list file.")

def display_loaded_list_file():
    """Display the loaded list file information."""
    if loaded_list_file:
        print(f"Loaded list file: {COLORS['GREEN']}{loaded_list_file}{COLORS['RESET']}")
        write_log(f"Loaded list file: {loaded_list_file}")
    else:
        print(f"{COLORS['RED']}No list file loaded.{COLORS['RESET']}")
        write_log("No list file loaded.")

# Function to display the loaded list file
def display_loaded_list():
    if loaded_list_file:
        with open(loaded_list_file, 'r') as file:
            print(f"{COLORS['GREEN']}Loaded list file content:{COLORS['RESET']}")
            for line in file:
                print(line.strip())
    else:
        print(f"{COLORS['RED']}No list file loaded.{COLORS['RESET']}")  

def load_list_file_menu():
    """Display and handle the 'Load list file' menu."""
    menu_options = [
        "Choose list file",
        "Close list file",
        "Show available list files",
        "Back"
    ]
    while True:
        print(f"{COLORS['GREEN']}File list options:{COLORS['RESET']}")
        display_loaded_list_file()
        for i, option in enumerate(menu_options, 1):
            print(f"{COLORS['GREEN']}({i}){COLORS['RESET']} {option}")
        choice = input("Enter your choice: ")

        if choice == '1':
            load_list_file()
            write_log("Loaded list file menu: Choose list file")
        elif choice == '2':
            close_list_file()
            write_log("Loaded list file menu: Close list file")
        elif choice == '3':
            list_available_list_files()
            write_log("Loaded list file menu: Show available list files")
        elif choice == '4':
            break
        else:
            print(f"{COLORS['RED']}Invalid choice. Please enter a valid option.{COLORS['RESET']}")
            write_log("Loaded list file menu: Invalid choice")


def list_available_list_files():
    """List all available .list files in the current directory."""
    list_files = [f for f in os.listdir('.') if f.endswith('.list')]
    if list_files:
        print(f"{COLORS['GREEN']}Available list files:{COLORS['RESET']}")
        for file in list_files:
            print(file)
        write_log("Listed available list files")
    else:
        print(f"{COLORS['RED']}No list files available.{COLORS['RESET']}")
        write_log("No list files available")

def display_main_menu():
    """Display the main menu of the script."""
    menu_options = [
        "Open/Close list file",
        "Copy files from the list",
        "Move files from the list",
        "Add files from the list to archive",
        "Delete files from the list",
        "Display loaded list",
        "Go back to main menu",
        "Exit"
    ]
    print(f"{COLORS['GREEN']}MENU:{COLORS['RESET']}")
    for i, option in enumerate(menu_options, 1):
        print(f"{COLORS['GREEN']}({i}){COLORS['RESET']} {option}")
    display_loaded_list_file()  # Display loaded list file information
    write_log("Displayed main menu")

def handle_menu_choice(choice):
    """Handle the user's menu choice."""
    write_log(f"User selected menu choice: {choice}")
    if choice == '1':
        load_list_file_menu()
    elif choice == '2':
        process_files_from_list("Copying", copy_file)
    elif choice == '3':
        process_files_from_list("Moving", move_file)
    elif choice == '4':
        add_to_archive()
    elif choice == '5':
        delete_files()
    elif choice == '6':
        display_loaded_list()
    elif choice == '7':
        subprocess.run([sys.executable, 'list-files.py'])
        sys.exit()
    elif choice == '8':
        finalize_and_exit()
    else:
        write_log(f"Invalid choice: {choice}")
        print(f"{COLORS['RED']}Invalid choice. Please enter a valid option.{COLORS['RESET']}")
    

def finalize_and_exit():
    """Finalize the script and exit."""
    write_log("Finalizing the script and exiting")
    with open(log_file_name, 'a') as log_file:
        log_file.write(create_script_separator("ACTIONS-LOG ENDED") + '\n')
    sys.exit()

def main():
    """Main function of the script."""
    initialize_log_file()
    write_log("Script started")
    start()
    while True:
        display_main_menu()
        choice = input("Enter your choice: ")
        write_log(f"User entered choice: {choice}")
        handle_menu_choice(choice)

if __name__ == "__main__":
    initialize_log_file()
    write_log("Script started")
    start()
    while True:
        display_main_menu()
        choice = input("Enter your choice: ")
        write_log(f"User entered choice: {choice}")
        handle_menu_choice(choice)
