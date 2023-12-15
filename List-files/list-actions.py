#!/usr/bin/env python3
import os
import datetime
import subprocess
import sys

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
        # Implement logic to copy files from the loaded list file here
    else:
        print(f"{RED}No list file loaded. Please load a list file first.{RESET}")

# Function to move files from the list
def move_files():
    global loaded_list_file
    if loaded_list_file:
        print(f"Moving files from the loaded list file: {loaded_list_file}")
        # Implement logic to move files from the loaded list file here
    else:
        print(f"{RED}No list file loaded. Please load a list file first.{RESET}")

# Function to add files from the list to archive
def add_to_archive():
    global loaded_list_file
    if loaded_list_file:
        print(f"Adding files to archive from the loaded list file: {loaded_list_file}")
        # Implement logic to add files to an archive from the loaded list file here
    else:
        print(f"{RED}No list file loaded. Please load a list file first.{RESET}")

# Function to delete files from the list
def delete_files():
    global loaded_list_file
    if loaded_list_file:
        print(f"Deleting files from the loaded list file: {loaded_list_file}")
        # Implement logic to delete files from the loaded list file here
    else:
        print(f"{RED}No list file loaded. Please load a list file first.{RESET}")

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

