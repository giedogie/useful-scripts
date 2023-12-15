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
log_name_time = current_time.strftime("%Y-%m-%d-%H-%M-%S")

# Define start and end separators with red color
start_separator = f"{RED}================== SCRIPT STARTED {formatted_time} ================================={RESET}"
end_separator = f"{RED}================== SCRIPT ENDED {formatted_time} ================================={RESET}"

# Function to print the start separator
def start():
    print(start_separator)

# Function to print the end separator
def end():
    print(end_separator)

# Function to list files in a directory based on different options
def list_files_in_dir(path, sort_option='size', reverse_sort=False, date_sort_reverse=False, extension=None, date_filter=None, phrase_filter=None, phrase_in_file_filter=None):
    if not os.path.exists(path):
        print(f"Path '{path}' does not exist.")
        return

    if os.path.isfile(path):
        if extension is None or path.endswith(extension):
            file_size = os.path.getsize(path)
            file_size_mb = file_size / (1024 * 1024)
            print(f"File: {path}, Size: {file_size_mb:.2f} MB")

    elif os.path.isdir(path):
        print(f"Directory: {path}")
        file_list = []

        for root, dirs, files in os.walk(path):
            for file in files:
                item_path = os.path.join(root, file)
                if extension is None or item_path.endswith(extension):
                    file_size = os.path.getsize(item_path)
                    file_size_mb = file_size / (1024 * 1024)
                    file_created_time = os.path.getctime(item_path)
                    file_created_time_formatted = datetime.datetime.fromtimestamp(file_created_time).strftime("%Y-%m-%d")
                    if phrase_in_file_filter:
                        try:
                            with open(item_path, 'r') as f:
                                if phrase_in_file_filter not in f.read():
                                    continue
                        except UnicodeDecodeError:
                            continue
                    file_list.append((item_path, file_size_mb, file_created_time_formatted))

        if date_filter:
            start_date, end_date = date_filter
            file_list = [file_info for file_info in file_list if start_date <= file_info[2] <= end_date]

        if phrase_filter:
            file_list = [file_info for file_info in file_list if phrase_filter.lower() in os.path.basename(file_info[0]).lower()]

        if sort_option == 'size':
            # Sort file list by size
            file_list.sort(key=lambda x: x[1], reverse=reverse_sort)
        elif sort_option == 'date':
            # Sort file list by creation date
            file_list.sort(key=lambda x: x[2], reverse=date_sort_reverse)
        elif sort_option == 'extension':
            # Sort file list by extension
            file_list.sort(key=lambda x: os.path.splitext(x[0])[-1])
        elif sort_option == 'alphabetical':
            # Sort file list alphabetically
            file_list.sort(key=lambda x: os.path.basename(x[0]), reverse=reverse_sort)

        # Print sorted list
        for file_info in file_list:
            file_path, file_size_mb, file_created_time_formatted = file_info
            print(f"File: {file_path}, Size: {file_size_mb:.2f} MB, Created: {file_created_time_formatted}")

        # Save results to .list file
        log_filename = f"result_{log_name_time}.list"
        with open(log_filename, 'w') as log_file:
            log_file.write(start_separator + '\n')
            for file_info in file_list:
                file_path, file_size_mb, file_created_time_formatted = file_info
                log_file.write(f"File: {file_path}, Size: {file_size_mb:.2f} MB, Created: {file_created_time_formatted}\n")
            log_file.write(end_separator + '\n')

# Function to get user input for date filtering
def get_date_filter_option():
    while True:
        date_filter_option = input(f"Filter by date {RED}R{RESET} for date range, {RED}D {RESET}for a specific day, or press {RED}Enter{RESET} to skip): \n").strip().lower()
        if date_filter_option in ('r', 'd', ''):
            return date_filter_option
        else:
            print(f"Invalid choice. Please enter {RED}'R'{RESET}, {RED}'D'{RESET}, or press {RED}Enter{RESET}.")

# Function to get date range from the user
def get_date_range():
    start_date = input(f"Enter start date in format {GREEN}'YYYY-MM-DD'{RESET}: \n")
    end_date = input(f"Enter end date in format {GREEN}'YYYY-MM-DD'{RESET}: \n")
    return start_date, end_date

# Function to get a specific day from the user
def get_specific_day():
    specific_date = input(f"Enter a specific date in format {GREEN}'YYYY-MM-DD'{RESET}: \n")
    return specific_date

OPTIONS = {
    '1': 'size',
    '2': 'date',
    '3': 'extension',
    '4': 'alphabetical',
    '5': 'phrase',
    '6': 'phrase_in_content',
    '7': 'actions_on_list',
    '8': 'exit'
}

while True:
    print(f"{GREEN}This script recursively searches directories and files in defined location and prints the sorted file list.{RESET}")
    print(f"{GREEN}MENU:{RESET}")
    print(f"{GREEN}(1){RESET} List files by size")
    print(f"{GREEN}(2){RESET} List files by date")
    print(f"{GREEN}(3){RESET} List files by extension")
    print(f"{GREEN}(4){RESET} List files by alphabetical order")
    print(f"{GREEN}(5){RESET} List files containing phrase in name")
    print(f"{GREEN}(6){RESET} List files containing phrase in content")
    print(f"{GREEN}(7){RESET} Actions on list")
    print(f"{GREEN}(8){RESET} Exit")
    
    choice = input(f"Enter your choice: \n")
    
    if choice in OPTIONS:
        if OPTIONS[choice] == 'exit':
            sys.exit() 
        elif OPTIONS[choice] == 'actions_on_list':
           subprocess.run([sys.executable, 'list-actions.py'])
           continue

        sort_option = OPTIONS[choice]
        dir_path = input(f"Type in the {GREEN}path{RESET} that you want to check: \n")
        if sort_option != 'phrase_in_content':
            reverse_sort = input(f"Sort order ({RED}S{RESET} for small-to-large / {RED}L{RESET} for large-to-small): \n").lower() == 'l'
        extension = input(f"Enter file extension {RED}(e.g., '.txt'){RESET} to filter by extension or leave blank to list all files: \n").lower()
        date_filter_option = get_date_filter_option()
        if date_filter_option == 'r':
            start_date, end_date = get_date_range()
            date_filter = (start_date, end_date)
        elif date_filter_option == 'd':
            specific_date = get_specific_day()
            date_filter = (specific_date, specific_date)
        else:
            date_filter = None
        phrase = input(f"Enter the phrase to search for: \n") if sort_option in ('phrase', 'phrase_in_content') else None
        start()
        if sort_option == 'phrase_in_content':
            phrase_in_file_filter = phrase
            list_files_in_dir(dir_path, sort_option, date_sort_reverse=False, extension=extension, date_filter=date_filter, phrase_in_file_filter=phrase_in_file_filter)
        else:
            list_files_in_dir(dir_path, sort_option, reverse_sort, date_sort_reverse=False, extension=extension, date_filter=date_filter, phrase_filter=phrase)
        end()
    else:
        print(f"{RED}Invalid choice.{RESET} Please enter a valid option {GREEN}(1){RESET}/{GREEN}(2){RESET}/{GREEN}(3){RESET}/{GREEN}(4){RESET}/{GREEN}(5){RESET}/{GREEN}(6){RESET}/{GREEN}(7){RESET}/{GREEN}(8){RESET}.")