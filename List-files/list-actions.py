#!/usr/bin/env python3
import os
import datetime
import subprocess
import sys
import shutil
import re
import zipfile

# ANSI Colors
RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"

# Get the current time and format it
current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d-%H:%M:%S")

# Define global list file
loaded_list_file = None

# Define start and end separators with red color
start_separator = f"{RED}================== SCRIPT STARTED {formatted_time} ================================={RESET}"
end_separator = f"{RED}================== SCRIPT ENDED {formatted_time} ================================={RESET}"

# Function to print the start separator
def start():
    print(start_separator)

# Function to print the end separator
def end():
    print(end_separator)

def display_main_menu():
    global loaded_list_file  # Make loaded_list_file global to access it here
    print(f"{GREEN}MENU:{RESET}")
    print(f"{GREEN}(1){RESET} Open/Close list file")
    print(f"{GREEN}(2){RESET} Copy files from the list")
    print(f"{GREEN}(3){RESET} Move files from the list")
    print(f"{GREEN}(4){RESET} Add files from the list to archive")
    print(f"{GREEN}(5){RESET} Delete files from the list")
    print(f"{GREEN}(6){RESET} Display loaded list")
    print(f"{GREEN}(7){RESET} Go back to main menu")
    print(f"{GREEN}(8){RESET} Exit")
    
    display_loaded_list_file()  # Display loaded list file information


# Function to display the loaded list file information
def display_loaded_list_file():
    if loaded_list_file:
        print(f"Loaded list file: {GREEN}{loaded_list_file}{RESET}")
    else:
        print(f"{RED}No list file loaded.{RESET}")

# Function to display the "Load list file" sub-menu
def load_list_file_menu():
    while True:
        print(f"{GREEN}File list options:{RESET}")
        display_loaded_list_file()
        print(f"{GREEN}(1){RESET} Choose list file")
        print(f"{GREEN}(2){RESET} Close list file")
        print(f"{GREEN}(3){RESET} Show available list files")
        print(f"{GREEN}(4){RESET} Back")
        choice = input(f"Enter your choice {GREEN}(1){RESET}/{GREEN}(2){RESET}/{GREEN}(3){RESET}/{GREEN}(4){RESET}: ")
        
        if choice == '1':
            load_list_file()
        elif choice == '2':
            close_list_file()  # Close the loaded list file
        elif choice == '3':
            list_available_list_files()  # Wywołanie funkcji do listowania dostępnych plików list
        elif choice == '4':
            break
        else:
            print(f"{RED}Invalid choice. Please enter a valid option.{RESET}")


# Function to load a list file
def load_list_file():
    global loaded_list_file
    list_file_path = input(f"Enter the path to the list file to load (or press Enter to go back to the main menu): ")
    if list_file_path == "":
        return  # Return to the main menu if Enter is pressed
    elif os.path.exists(list_file_path):
        loaded_list_file = list_file_path
    else:
        print(f"{RED}File does not exist. Please enter a valid file path or press Enter to go back to the main menu.{RESET}")

def close_list_file():
    global loaded_list_file
    loaded_list_file = None
    print("Closed the loaded list file.")            

# Function to copy files from the list
def copy_files():
    global loaded_list_file
    if loaded_list_file:
        print(f"Copying files from the loaded list file: {loaded_list_file}")
        destination_folder = input("Enter the destination folder path: ")
        if os.path.exists(destination_folder) and os.path.isdir(destination_folder):
            with open(loaded_list_file, 'r') as file:
                copied_files = []  # List to store copied files
                for line in file:
                    match = re.search(r'File: (.*), Size:', line)
                    if match:
                        file_to_copy = match.group(1).strip()
                        if os.path.exists(file_to_copy) and os.path.isfile(file_to_copy):
                            destination_file = os.path.join(destination_folder, os.path.basename(file_to_copy))
                            if not os.path.exists(destination_file):
                                shutil.copy(file_to_copy, destination_file)
                                copied_files.append(file_to_copy)
                                print(f"Copied {file_to_copy} to {destination_folder}")
                            else:
                                print(f"Skipped {file_to_copy} because it already exists in the destination folder.")
                if not copied_files:
                    print(f"No files were copied.")
        else:
            print(f"Destination folder does not exist or is not a directory.")
    else:
        print(f"No list file loaded. Please load a list file first.")

# Function to move files from the list
def move_files():
    global loaded_list_file
    if loaded_list_file:
        print(f"Moving files from the loaded list file: {loaded_list_file}")
        destination_folder = input("Enter the destination folder path: ")
        if os.path.exists(destination_folder) and os.path.isdir(destination_folder):
            with open(loaded_list_file, 'r') as file:
                moved_files = []  # List to store moved files
                for line in file:
                    match = re.search(r'File: (.*), Size:', line)
                    if match:
                        file_to_move = match.group(1).strip()
                        if os.path.exists(file_to_move) and os.path.isfile(file_to_move):
                            destination_file = os.path.join(destination_folder, os.path.basename(file_to_move))
                            if not os.path.exists(destination_file):
                                shutil.move(file_to_move, destination_file)
                                moved_files.append(file_to_move)
                                print(f"Moved {file_to_move} to {destination_folder}")
                            else:
                                print(f"Skipped {file_to_move} because it already exists in the destination folder.")
                if not moved_files:
                    print(f"No files were moved.")
        else:
            print(f"Destination folder does not exist or is not a directory.")
    else:
        print(f"No list file loaded. Please load a list file first.")

# Function to add files from the list to archive
def add_to_archive():
    global loaded_list_file
    if loaded_list_file:
        print(f"Creating and moving archive from the loaded list file: {loaded_list_file}")
        destination_folder = input("Enter the destination folder path for the archive: ")
        archive_name = input("Enter the archive name (without extension): ")
        if os.path.exists(destination_folder) and os.path.isdir(destination_folder):
            with open(loaded_list_file, 'r') as file:
                files_to_archive = []  # List to store files to be archived
                for line in file:
                    match = re.search(r'File: (.*), Size:', line)
                    if match:
                        file_to_archive = match.group(1).strip()
                        if os.path.exists(file_to_archive) and os.path.isfile(file_to_archive):
                            files_to_archive.append(file_to_archive)
                        else:
                            print(f"Skipped {file_to_archive} because it does not exist.")
                
                if files_to_archive:
                    archive_path = os.path.join(destination_folder, f"{archive_name}.zip")
                    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        for file_to_archive in files_to_archive:
                            zipf.write(file_to_archive, os.path.basename(file_to_archive))
                    
                    print(f"Created archive {archive_path}")
                else:
                    print(f"No files to archive.")
        else:
            print(f"Destination folder does not exist or is not a directory.")
    else:
        print(f"No list file loaded. Please load a list file first.")

# Function to delete files from the list
def delete_files():
    global loaded_list_file
    if loaded_list_file:
        print(f"Deleting files from the loaded list file: {loaded_list_file}")
        confirm = input("Are you sure you want to delete these files? (yes/no): ")
        if confirm.lower() == 'yes':
            with open(loaded_list_file, 'r') as file:
                deleted_files = []  # List to store deleted files
                for line in file:
                    match = re.search(r'File: (.*), Size:', line)
                    if match:
                        file_to_delete = match.group(1).strip()
                        if os.path.exists(file_to_delete) and os.path.isfile(file_to_delete):
                            os.remove(file_to_delete)
                            deleted_files.append(file_to_delete)
                            print(f"Deleted {file_to_delete}")
                        else:
                            print(f"Skipped {file_to_delete} because it does not exist.")
                if not deleted_files:
                    print(f"No files were deleted.")
        else:
            print("Deletion canceled.")
    else:
        print(f"No list file loaded. Please load a list file first.")

# Function to display the loaded list file
def display_loaded_list():
    if loaded_list_file:
        with open(loaded_list_file, 'r') as file:
            print(f"{GREEN}Loaded list file content:{RESET}")
            for line in file:
                print(line.strip())
    else:
        print(f"{RED}No list file loaded.{RESET}")        

def list_available_list_files():
    list_files = [f for f in os.listdir('.') if f.endswith('.list')]
    if list_files:
        print(f"{GREEN}Available list files:{RESET}")
        for file in list_files:
            print(file)
    else:
        print(f"{RED}No list files available.{RESET}")

# Main loop for the program
while True:
    display_main_menu()
    choice = input(f"Enter your choice: \n" )
    
    if choice == '1':
        load_list_file_menu()  # Go to the "Load list file" sub-menu
    elif choice == '2':
        copy_files()
    elif choice == '3':
        move_files()
    elif choice == '4':
        add_to_archive()
    elif choice == '5':
        delete_files()
    elif choice == '6':
        display_loaded_list()  # Display the loaded list
    elif choice == '7':
        subprocess.run([sys.executable, 'list-files.py'])
        continue
    elif choice == '8':
        sys.exit()    
    else:
        print(f"{RED}Invalid choice. Please enter a valid option.{RESET}")

