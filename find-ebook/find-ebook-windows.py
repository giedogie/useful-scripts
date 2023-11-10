import os
import shutil

# Specify the directory to traverse
directory_to_traverse = input('TYPE A PATH TO SEARCH IN: ')

# Specify the target directory to copy the files
target_directory = os.path.join(os.getcwd(), "COPIED-EBOOKS")

# Check for result folder
if not os.path.exists(target_directory):
    os.makedirs(target_directory)
    print("Folder created.")
else:
    print("Folder already exist.")

def copy_file(file_path, target_dir):
    file_name = os.path.basename(file_path)
    
    # Delte special signs from file name.
    file_name = "".join([c for c in file_name if c.isalnum() or c in ['.', '_', '-']])
    
    try:
        shutil.copy2(file_path, os.path.join(target_dir, file_name))
        print(f"File '{file_name}' copied successfully.")
        
    except shutil.SameFileError:
        print(f"File '{file_name}' already exists in the target directory.")

def traverse_directory(directory, target_dir):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(('.pdf', '.epub', '.mobi')):
                copy_file(file_path, target_dir)

# Execute function traverse_directory
traverse_directory(directory_to_traverse, target_directory)