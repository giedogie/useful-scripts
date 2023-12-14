#!/usr/bin/env python3
import os
import datetime

# ANSI Colors
RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"

# Get the current time and format it
current_time = datetime.datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d-%H:%M:%S")

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
def list_files_in_dir(path, sort_option='size', reverse_sort=False, date_sort_reverse=False, extension=None, date_filter=None, min_size=None, max_size=None):
    if not os.path.exists(path):
        print(f"Path '{path}' does not exist.")
        return

    if os.path.isfile(path):
        if extension is None or path.endswith(extension):
            file_size = os.path.getsize(path)
            file_size_mb = file_size / (1024 * 1024)
            if (min_size is None or file_size_mb >= min_size) and (max_size is None or file_size_mb <= max_size):
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
                    if (min_size is None or file_size_mb >= min_size) and (max_size is None or file_size_mb <= max_size):
                        file_created_time = os.path.getctime(item_path)
                        file_created_time_formatted = datetime.datetime.fromtimestamp(file_created_time).strftime("%Y-%m-%d")
                        file_list.append((item_path, file_size_mb, file_created_time_formatted))

        if date_filter:
            start_date, end_date = date_filter
            file_list = [file_info for file_info in file_list if start_date <= file_info[2] <= end_date]

        if sort_option == 'size':
            # Sort file list by size
            file_list.sort(key=lambda x: x[1], reverse=reverse_sort)
        elif sort_option == 'date':
            # Sort file list by creation date
            file_list.sort(key=lambda x: x[2], reverse=date_sort_reverse)
        elif sort_option == 'extension':
            # Sort file list by extension
            file_list.sort(key=lambda x: os.path.splitext(x[0])[-1])

        # Print sorted list
        for file_info in file_list:
            file_path, file_size_mb, file_created_time_formatted = file_info
            print(f"File: {file_path}, Size: {file_size_mb:.2f} MB, Created: {file_created_time_formatted}")

        # Save results to .log file
        log_filename = f"result_{formatted_time}.log"
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

# Function to get user input for minimum and maximum file size
def get_file_size_range():
    min_size = input(f"Enter minimum file size in MB (or press {RED}Enter{RESET} to skip): ")
    max_size = input(f"Enter maximum file size in MB (or press {RED}Enter{RESET} to skip): ")
    try:
        min_size = float(min_size) if min_size else None
        max_size = float(max_size) if max_size else None
        return min_size, max_size
    except ValueError:
        print(f"{RED}Invalid input. Please enter a valid number or press {RESET}{RED}Enter{RESET} to skip.")
        return get_file_size_range()

# Main loop for user interaction
while True:
    print(f"{GREEN}This script recursively searches directories and files in defined location and prints the sorted file list.{RESET}")
    print(f"{GREEN}MENU:{RESET}")
    print(f"{GREEN}(1){RESET} List files by size")
    print(f"{GREEN}(2){RESET} List files by date")
    print(f"{GREEN}(3){RESET} List files by extension")
    print(f"{GREEN}(4){RESET} Exit")
    
    choice = input(f"Enter your choice {GREEN}(1){RESET}/{GREEN}(2){RESET}/{GREEN}(3){RESET}/{GREEN}(4){RESET}: ")
    
    if choice == '1':
        sort_option = 'size'
        dir_path = input(f"Type in the {GREEN}path{RESET} that you want to check: \n")
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
        min_size, max_size = get_file_size_range()
        start()
        list_files_in_dir(dir_path, sort_option, reverse_sort, date_sort_reverse=False, extension=extension, date_filter=date_filter, min_size=min_size, max_size=max_size)
        end()
    elif choice == '2':
        sort_option = 'date'
        dir_path = input(f"Type in the {GREEN}path{RESET} that you want to check: \n")
        date_sort_reverse = input(f"Sort by date order (enter {RED}O{RESET} for oldest-to-newest or {RED}N{RESET} for newest-to-oldest): \n").lower() == 'n'     
        date_filter_option = get_date_filter_option()
        if date_filter_option == 'r':
            start_date, end_date = get_date_range()
            date_filter = (start_date, end_date)
        elif date_filter_option == 'd':
            specific_date = get_specific_day()
            date_filter = (specific_date, specific_date)
        else:
            date_filter = None
        extension = None  # Removed the extension prompt in this option
        min_size, max_size = get_file_size_range()
        start()
        list_files_in_dir(dir_path, sort_option, reverse_sort=False, date_sort_reverse=date_sort_reverse, extension=extension, date_filter=date_filter, min_size=min_size, max_size=max_size)
        end()
    elif choice == '3':
        sort_option = 'extension'
        dir_path = input(f"Type in the {GREEN}path{RESET} that you want to check: \n")
        extension = input(f"Enter file extension {GREEN}(e.g., '.txt'){RESET} to filter by extension or leave blank to list all files: \n").lower()
        date_filter_option = get_date_filter_option()
        if date_filter_option == 'r':
            start_date, end_date = get_date_range()
            date_filter = (start_date, end_date)
        elif date_filter_option == 'd':
            specific_date = get_specific_day()
            date_filter = (specific_date, specific_date)
        else:
            date_filter = None
        min_size, max_size = get_file_size_range()
        start()
        list_files_in_dir(dir_path, sort_option, reverse_sort=False, date_sort_reverse=False, extension=extension, date_filter=date_filter, min_size=min_size, max_size=max_size)
        end()
    elif choice == '4':
        break
    else:
        print(f"{RED}Invalid choice.{RESET} Please enter a valid option {GREEN}(1){RESET}/{GREEN}(2){RESET}/{GREEN}(3){RESET}/{GREEN}(4){RESET}.")
