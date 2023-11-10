#!/usr/bin/env python3
import os
import shutil
import time

#counter=0


# Specify the directory to traverse
directory_to_traverse = input('TYPE A PATH TO SEARCH IN: ')

# Specify the target directory to copy the files
target_directory =os.getcwd() + "/COPIED-EBOOKS/"

#Check for result folder
if not os.path.exists(target_directory):
    os.makedirs(target_directory)
    print("Folder created.")
else:
    print("Folder already exists.")

def copy_file(file_path, target_dir):
    file_name = os.path.basename(file_path)
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


# Call the function to traverse the directory and copy the files
traverse_directory(directory_to_traverse, target_directory)




