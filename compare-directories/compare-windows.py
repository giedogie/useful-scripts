#!/usr/bin/env python3
import os
import shutil
import datetime
import time

current_time = datetime.datetime.now()
counter=0
counter1=0

def start():
    
    start_separator=f"================== SKRYPT URUCHOMIONY {current_time} ================================="
    
    print(start_separator)  

def end():
    
    end_separator=f"================== SKRYPT ZAKOŃCZONY {current_time} ================================="
    print(end_separator)

start()


source_dir1 = input('Podaj ścieżkę do pierwszego folderu: ')
source_dir2 = input('Podaj ścieżkę do drugiego folderu: ')
target_dir=os.getcwd() + "/result1"

def copy_file(source_path, target_path):
    global counter
    if not os.path.exists(target_path):
        shutil.copy2(source_path, target_path)
        counter += 1
        print(f'Skopiowano plik: {counter}\r', end='')
        time.sleep(0.0001)
    else:
        source_stat = os.stat(source_path)
        target_stat = os.stat(target_path)

        if source_stat.st_mtime > target_stat.st_mtime or source_stat.st_size > target_stat.st_size:
            shutil.copy2(source_path, target_path)
            counter += 1
            print(f'Skopiowano plik: {counter}\r', end='')
            time.sleep(0.0001)

def compare_directories(source_dir1, source_dir2, target_dir):
    for root, dirs, files in os.walk(source_dir1):
        relative_path = os.path.relpath(root, source_dir1)
        target_path = os.path.join(target_dir, relative_path)

        if not os.path.exists(target_path):
            os.makedirs(target_path)

        for file in files:
            source_path1 = os.path.join(root, file)
            source_path2 = os.path.join(source_dir2, relative_path, file)
            target_path = os.path.join(target_dir, relative_path, file)

            copy_file(source_path1, target_path)
            if os.path.exists(source_path2):
                copy_file(source_path2, target_path)

    for root, dirs, files in os.walk(source_dir2):
        relative_path = os.path.relpath(root, source_dir2)
        target_path = os.path.join(target_dir, relative_path)

        if not os.path.exists(target_path):
            os.makedirs(target_path)

        for file in files:
            source_path2 = os.path.join(root, file)
            source_path1 = os.path.join(source_dir1, relative_path, file)
            target_path = os.path.join(target_dir, relative_path, file)

            copy_file(source_path2, target_path)
            if os.path.exists(source_path1):
                copy_file(source_path1, target_path)



compare_directories(source_dir1, source_dir2, target_dir)

end()