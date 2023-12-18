#!/usr/bin/env python3
import os
import datetime
import subprocess
import sys


# ANSI Colors
COLORS = {
    "RED": "\033[91m",
    "GREEN": "\033[92m",
    "BLUE": "\033[94m",
    "RESET": "\033[0m"
}

def current_formatted_time():
    """Get the current time and format it."""
    return datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

# Global Variables
loaded_list_file = None
log_file_name = f"log_{current_formatted_time()}.log"
global_directory_path = None


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

def finalize_and_exit():
    """Finalize the script and exit."""
    write_log("Finalizing the script and exiting")
    with open(log_file_name, 'a') as log_file:
        log_file.write(create_script_separator("ACTIONS-LOG ENDED") + '\n')
    sys.exit()

def list_files_recursive(directory, file_list):
    """Rekursywnie listuje pliki w podanym katalogu."""
    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_file():
                file_list.append((entry.path, os.path.getsize(entry.path)))
            elif entry.is_dir():
                list_files_recursive(entry.path, file_list)

def save_results_to_file(files):
    """Save the sorted and filtered files to a file with a generated name."""
    result_file_name = f"result_{current_formatted_time()}.list"
    with open(result_file_name, 'w') as result_file:
        for file_path, size in files:
            size_mb = get_file_size_in_mb(size)
            creation_time = get_file_creation_time(file_path)
            result_file.write(f"{file_path} - {size_mb:.2f} MB - Created: {creation_time}\n")
    

def get_time_frame():
    """Get the time frame for file sorting with a modular menu."""
    print(f"Enter the time frame for sorting (leave {COLORS['RED']}empty{COLORS['RESET']} for anytime):")
    start_date_str = input(f"Enter the start date {COLORS['RED']}YYYY-MM-DD{COLORS['RESET']} or leave {COLORS['RED']}empty{COLORS['RESET']}: ").strip()
    end_date_str = input(f"Enter the end date {COLORS['RED']}YYYY-MM-DD{COLORS['RESET']} or leave {COLORS['RED']}empty{COLORS['RESET']}: ").strip()

    start_date, end_date = None, None
    if start_date_str:
        try:
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
        except ValueError:
            print(f"Invalid start date format. Please use {COLORS['RED']}YYYY-MM-DD{COLORS['RESET']}.")
            return None, None, False

    if end_date_str:
        try:
            end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")
        except ValueError:
            print(f"Invalid end date format. Please use {COLORS['RED']}YYYY-MM-DD{COLORS['RESET']}.")
            return None, None, False

    return start_date, end_date, False


def get_file_creation_time(file_path):
    """Pobierz czas utworzenia pliku."""
    timestamp = os.path.getctime(file_path)
    return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

def get_file_size_in_mb(size_in_bytes):
    """Konwertuje rozmiar pliku na megabajty."""
    return size_in_bytes / (1024 * 1024)

def get_user_sort_choice():
    """Pobiera od użytkownika wybór sposobu sortowania plików."""
    while True:
        print("Choose the file sorting method:")
        print(f"{COLORS['GREEN']}(1){COLORS['RESET']} ASCENDING")
        print(f"{COLORS['GREEN']}(2){COLORS['RESET']} DESCENDING")
        print(f"{COLORS['GREEN']}(3){COLORS['RESET']} Back")
        choice = input("Choice (1/2/3): ").strip()

        if choice == '1':
            return True  # sort_ascending = True
        elif choice == '2':
            return False  # sort_ascending = False
        elif choice == '3':
            return None  # sort_ascending = False
        else:
            print(f"{COLORS['RED']}Invalid choice. Please try again.{COLORS['RESET']}")

def get_file_modification_time(file_path):
    """Pobierz czas ostatniej modyfikacji pliku."""
    timestamp = os.path.getmtime(file_path)
    return datetime.datetime.fromtimestamp(timestamp)

def get_directory_path():
    """Pobiera od użytkownika ścieżkę do katalogu i weryfikuje jej poprawność."""
    while True:
        directory = input("Enter the directory path: ").strip()
        if os.path.isdir(directory):
            return directory
        else:
            print(f"{COLORS['RED']}Invalid path. Please try again.{COLORS['RESET']}")

def get_extension():
    """Get the file extension for sorting."""
    extension = input(f"Enter the file extension to filter {COLORS['RED']}(e.g., '.txt') or leave blank {COLORS['RESET']}: ").strip()
    return extension if extension else None

def get_size_filter():
    """Get the user's input for filtering files by size."""
    size_filter_input = input(f"Enter file size filter {COLORS['RED']}(e.g., '> 50', '< 100', or leave blank){COLORS['RESET']}: ").strip()
    if size_filter_input:
        try:
            operator, size_limit = size_filter_input.split()
            size_limit = float(size_limit)
            return operator, size_limit
        except ValueError:
            print(f"Invalid format. Use '{COLORS['RED']}> MB'{COLORS['RESET']} or '{COLORS['RED']}< MB{COLORS['RESET']}'.")
            return None, None
    return None, None

def filter_files_by_date(files, start_date, end_date):
    """Filtruj pliki według daty modyfikacji."""
    if not start_date and not end_date:
        return files
    filtered_files = []
    for file in files:
        mod_time = get_file_modification_time(file[0])
        if (start_date and mod_time < start_date) or (end_date and mod_time > end_date):
            continue
        filtered_files.append(file)
    return filtered_files

def filter_files_by_extension(files, extension):
    """Filtruj pliki według rozszerzenia."""
    if not extension:
        return files
    return [file for file in files if file[0].endswith(extension)]


def list_by_size(directory):
    """List files in the directory sorted by size, display size in MB, and creation time."""
    
    if global_directory_path is None:
        print(f"{COLORS['RED']}No directory path set. Please set the path first.{COLORS['RESET']}")
        return
    
    sort_choice = get_user_sort_choice()
    if sort_choice is None or sort_choice == 'back':
        return  # Return to menu if the user chose to go back

    sort_ascending = sort_choice
    start_date, end_date, back_flag = get_time_frame()
    if back_flag:
        return  # Return to menu if the user chose to go back

    extension_filter = get_extension()
    if extension_filter == 'back':
        return  # Return to menu if the user chose to go back

    size_operator, size_limit = get_size_filter()
    if size_operator == 'back':
        return  # Return to menu if the user chose to go back

    files = []
    list_files_recursive(directory, files)

    # Filtering files based on time frame, extension, and size
    if start_date and end_date:
        files = [file for file in files if start_date <= get_file_modification_time(file[0]) <= end_date]
    if extension_filter:
        files = [file for file in files if file[0].endswith(extension_filter)]
    if size_operator and size_limit:
        if size_operator == '>':
            files = [file for file in files if get_file_size_in_mb(file[1]) > size_limit]
        elif size_operator == '<':
            files = [file for file in files if get_file_size_in_mb(file[1]) < size_limit]

    # Sort the files by size
    files.sort(key=lambda x: x[1], reverse=not sort_ascending)

    # Display the sorted and filtered files
    for file_path, size in files:
        size_mb = get_file_size_in_mb(size)
        creation_time = get_file_creation_time(file_path)
        print(f"{file_path} - {COLORS['GREEN']}{size_mb:.2f} MB {COLORS['RESET']} - Created: {COLORS['GREEN']}{creation_time}{COLORS['RESET']}")
        save_results_to_file(files)

def list_by_date(directory):
    
    if global_directory_path is None:
        print(f"{COLORS['RED']}No directory path set. Please set the path first.{COLORS['RESET']}")
        return
    
    
    sort_choice = get_user_sort_choice()
    if sort_choice is None or sort_choice == 'back':
        return  # Return to menu if the user chose to go back

    sort_ascending = sort_choice
    start_date, end_date, back_flag = get_time_frame()
    if back_flag:
        return  # Return to menu if the user chose to go back

    extension_filter = get_extension()
    if extension_filter == 'back':
        return  # Return to menu if the user chose to go back

    size_operator, size_limit = get_size_filter()
    if size_operator == 'back':
        return  # Return to menu if the user chose to go back

    files = []
    list_files_recursive(directory, files)

    # Filtering files based on time frame, extension, and size
    if start_date and end_date:
        files = [file for file in files if start_date <= get_file_modification_time(file[0]) <= end_date]
    if extension_filter:
        files = [file for file in files if file[0].endswith(extension_filter)]
    if size_operator and size_limit:
        if size_operator == '>':
            files = [file for file in files if get_file_size_in_mb(file[1]) > size_limit]
        elif size_operator == '<':
            files = [file for file in files if get_file_size_in_mb(file[1]) < size_limit]

    # Sort the files by date
    files.sort(key=lambda x: get_file_modification_time(x[0]), reverse=not sort_ascending)

    # Display the sorted and filtered files
    for file_path, size in files:
        size_mb = get_file_size_in_mb(size)
        creation_time = get_file_creation_time(file_path)
        print(f"{file_path} - {COLORS['GREEN']}{size_mb:.2f} MB {COLORS['RESET']} - Created: {COLORS['GREEN']}{creation_time}{COLORS['RESET']}")
        save_results_to_file(files)

def list_by_extension(directory):
    if global_directory_path is None:
        print(f"{COLORS['RED']}No directory path set. Please set the path first.{COLORS['RESET']}")
        return
    
    sort_choice = get_user_sort_choice()
    if sort_choice is None or sort_choice == 'back':
        return  # Return to menu if the user chose to go back

    sort_ascending = sort_choice
    start_date, end_date, back_flag = get_time_frame()
    if back_flag:
        return  # Return to menu if the user chose to go back

    extension_filter = get_extension()
    if extension_filter == 'back':
        return  # Return to menu if the user chose to go back

    size_operator, size_limit = get_size_filter()
    if size_operator == 'back':
        return  # Return to menu if the user chose to go back

    files = []
    list_files_recursive(directory, files)

    # Filtering files based on time frame, extension, and size
    if start_date and end_date:
        files = [file for file in files if start_date <= get_file_modification_time(file[0]) <= end_date]
    if extension_filter:
        files = [file for file in files if file[0].endswith(extension_filter)]
    if size_operator and size_limit:
        if size_operator == '>':
            files = [file for file in files if get_file_size_in_mb(file[1]) > size_limit]
        elif size_operator == '<':
            files = [file for file in files if get_file_size_in_mb(file[1]) < size_limit]

    # Sort the files by extension
    files.sort(key=lambda x: x[0].split('.')[-1], reverse=not sort_ascending)

    # Display the sorted and filtered files
    for file_path, size in files:
        size_mb = get_file_size_in_mb(size)
        creation_time = get_file_creation_time(file_path)
        print(f"{file_path} - {COLORS['GREEN']}{size_mb:.2f} MB {COLORS['RESET']} - Created: {COLORS['GREEN']}{creation_time}{COLORS['RESET']}")
        save_results_to_file(files)


import os

def list_by_alphabetical(directory, size_operator=None, size_limit=None):
    """
    Lists files in the specified directory alphabetically.
    Optionally filters files by size and modification date.
    """

    # Check if global directory path is set
    if global_directory_path is None:
        print(f"{COLORS['RED']}No directory path set. Please set the path first.{COLORS['RESET']}")
        return

    # Get user's choice for sorting order
    sort_choice = get_user_sort_choice()
    if sort_choice is None or sort_choice == 'back':
        return  # Return to menu if the user chose to go back

    sort_ascending = sort_choice

    # Get time frame for filtering files
    start_date, end_date, back_flag = get_time_frame()
    if back_flag:
        return  # Return to menu if the user chose to go back

    # Get file extension filter
    extension_filter = get_extension()
    if extension_filter == 'back':
        return  # Return to menu if the user chose to go back

    # Get size filter
    size_operator, size_limit = get_size_filter()
    if size_operator == 'back':
        return  # Return to menu if the user chose to go back

    files = []
    list_files_recursive(directory, files)

    # Filtering files based on time frame, extension, and size
    if start_date and end_date:
        files = [file for file in files if start_date <= get_file_modification_time(file[0]) <= end_date]
    if extension_filter:
        files = [file for file in files if file[0].endswith(extension_filter)]
    if size_operator and size_limit:
        if size_operator == '>':
            files = [file for file in files if get_file_size_in_mb(file[1]) > size_limit]
        elif size_operator == '<':
            files = [file for file in files if get_file_size_in_mb(file[1]) < size_limit]

    # Sort the files alphabetically
    files.sort(key=lambda x: os.path.basename(x[0]), reverse=not sort_ascending)

    # Display the sorted and filtered files
    for file_path, size in files:
        size_mb = get_file_size_in_mb(size)
        creation_time = get_file_creation_time(file_path)
        print(f"{file_path} - {COLORS['GREEN']}{size_mb:.2f} MB {COLORS['RESET']} - Created: {COLORS['GREEN']}{creation_time}{COLORS['RESET']}")
        save_results_to_file(files)


def list_by_phrase_in_name(directory):
    """
    Lists files containing a specified phrase in their name.
    """

    # Check if global directory path is set
    if global_directory_path is None:
        print(f"{COLORS['RED']}No directory path set. Please set the path first.{COLORS['RESET']}")
        return

    # Get phrase to search in file names
    phrase = input(f"Enter the {COLORS['RED']}phrase{COLORS['RESET']} to search in file names: ").strip().lower()

    files = []
    list_files_recursive(directory, files)

    # Filter files containing the phrase in their name
    filtered_files = [file for file in files if phrase in os.path.basename(file[0]).lower()]

    # Get user's choice for sorting order
    sort_choice = get_user_sort_choice()
    if sort_choice is None or sort_choice == 'back':
        return  # Return to menu if the user chose to go back

    sort_ascending = sort_choice 
   # Sort the filtered files alphabetically
    filtered_files.sort(key=lambda x: os.path.basename(x[0]), reverse=not sort_ascending)

    # Display the sorted and filtered files
    for file_path, size in filtered_files:
        size_mb = get_file_size_in_mb(size)
        creation_time = get_file_creation_time(file_path)
        print(f"{file_path} - {COLORS['GREEN']}{size_mb:.2f} MB {COLORS['RESET']} - Created: {COLORS['GREEN']}{creation_time}{COLORS['RESET']}")


def list_by_phrase_in_content(directory):
    
    if global_directory_path is None:
        print(f"{COLORS['RED']}No directory path set. Please set the path first.{COLORS['RESET']}")
        return    

    """List files containing a specified phrase in their content."""
    phrase = input(f"Enter the {COLORS['RED']}phrase{COLORS['RESET']} to search in file content: ").strip().lower()
    files = []
    list_files_recursive(directory, files)

    sort_choice = get_user_sort_choice()
    if sort_choice is None or sort_choice == 'back':
        return  # Return to menu if the user chose to go back

    sort_ascending = sort_choice
    start_date, end_date, back_flag = get_time_frame()
    if back_flag:
        return  # Return to menu if the user chose to go back

    extension_filter = get_extension()
    if extension_filter == 'back':
        return  # Return to menu if the user chose to go back

    size_operator, size_limit = get_size_filter()
    if size_operator == 'back':
        return  # Return to menu if the user chose to go back

    files = []
    list_files_recursive(directory, files)

    # Filtering files based on time frame, extension, and size
    if start_date and end_date:
        files = [file for file in files if start_date <= get_file_modification_time(file[0]) <= end_date]
    if extension_filter:
        files = [file for file in files if file[0].endswith(extension_filter)]
    if size_operator and size_limit:
        if size_operator == '>':
            files = [file for file in files if get_file_size_in_mb(file[1]) > size_limit]
        elif size_operator == '<':
            files = [file for file in files if get_file_size_in_mb(file[1]) < size_limit]

    # Filter files containing the phrase in their content
    filtered_files = []
    for file_path, size in files:
        try:
            with open(file_path, 'r') as file:
                try:
                    if phrase in file.read().lower():
                        filtered_files.append((file_path, size))
                except UnicodeDecodeError:
                    continue  # Skip files that cannot be decoded
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    # Display and save the filtered files
    for file_path, size in filtered_files:
        size_mb = get_file_size_in_mb(size)
        creation_time = get_file_creation_time(file_path)
        print(f"{file_path} - {size_mb:.2f} MB - Created: {creation_time}")
    save_results_to_file(filtered_files)

def path_to_dir_menu():
    
    """Display and manage submenu 'Path to dir'."""
    
    global global_directory_path
    while True:
        print(f"PATH MOUNTED: {COLORS['GREEN']}{global_directory_path}{COLORS['RESET']}")
        print(f"{COLORS['GREEN']}(1){COLORS['RESET']} Enter path")
        print(f"{COLORS['GREEN']}(2){COLORS['RESET']} Unmount path")
        print(f"{COLORS['GREEN']}(3){COLORS['RESET']} Back")
        choice = input("Wybór (1/2/3): ").strip()

        if choice == '1':
            global_directory_path = get_directory_path()
            print(f"Selected path: {global_directory_path}")
        elif choice == '2':
            global_directory_path = None
            print(f"{COLORS['RED']}Path unmounted{COLORS['RESET']}")
        elif choice == '3':
            return
        else:
            print(f"{COLORS['RED']}Invalid choice. Please try again.{COLORS['RESET']}")

def display_sort_menu():
    
    """Shows sorting menu and handles users choices."""
    
    while True:
        print(f"PATH MOUNTED: {COLORS['GREEN']}{global_directory_path}{COLORS['RESET']}")
        print(f"Choose the file sorting method:")
        print(f"{COLORS['GREEN']}(1){COLORS['RESET']} From smallest to largest")
        print(f"{COLORS['GREEN']}(2){COLORS['RESET']} From largest to smallest")
        print(f"{COLORS['GREEN']}(3){COLORS['RESET']} Return to the previous menu")
        choice = input("Wybór (1/2/3): ").strip()

        if choice == '1':
            return True  # sort_ascending = True
        elif choice == '2':
            return False  # sort_ascending = False
        elif choice == '3':
            return  None # Oznaczenie powrotu do menu
        else:
            print(f"{COLORS['GREEN']}Invalid choice. Please try again.{COLORS['RESET']}")

def display_main_menu():
    """Display the main menu of the script."""
    menu_options = [
        "Path to dir",
        "List files by size",
        "List files by date",
        "List files by alphabetical order",
        "List files containing phrase in name",
        "List files containing phrase in content",
        "Actions on list",
        "Exit"
    ]
    print(f"{COLORS['GREEN']}This script recursively searches directories and files in defined location and prints the sorted file list. \n You can also perform actions on listed files{COLORS['RESET']}")
    print(f"PATH MOUNTED: {COLORS['GREEN']}{global_directory_path}{COLORS['RESET']}")
    print(f"{COLORS['GREEN']}MENU:{COLORS['RESET']}")
    for i, option in enumerate(menu_options, 1):
        print(f"{COLORS['GREEN']}({i}){COLORS['RESET']} {option}")
    write_log("Displayed main menu")

def handle_menu_choice(choice):
    """Handle the user's menu choice."""
    write_log(f"User selected menu choice: {choice}")
    directory = global_directory_path
    if choice == '1':
        path_to_dir_menu()
    elif choice == '2':       
        list_by_size(directory)
    elif choice == '3':
        list_by_date(directory)
    elif choice == '4':
        list_by_alphabetical(directory)
    elif choice == '5':
        list_by_phrase_in_name(directory)
    elif choice == '6':
        list_by_phrase_in_content(directory)
    elif choice == '7':
        subprocess.run([sys.executable, 'list-actions.py'])
        sys.exit()
    elif choice == '8':
        finalize_and_exit()
    else:
        write_log(f"Invalid choice: {choice}")
        print(f"{COLORS['RED']}Invalid choice. Please enter a valid option.{COLORS['RESET']}")
            
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
