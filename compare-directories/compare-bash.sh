#!/bin/bash

logfile=/var/log/directory_diff.log
errorlog=/var/log/directory_diff_errors.log

start() {
    start_separator="\e[34m==================\e[32mSKRYPT URUCHOMIONY $(/usr/bin/date)\e[34m=================================\e[0m"
    end_separator="\e[34m==================\e[32mSKRYPT ZAKOŃCZONY $(/usr/bin/date)\e[34m=================================\e[0m"
    target_dir="$PWD/result"
    counter=0

    echo -e "$start_separator" >> $logfile && >>$errorlog
    echo -e "$start_separator" 
    read -p "Podaj ścieżkę do pierwszego folderu: " source_dir1
    read -p "Podaj ścieżkę do drugiego folderu: " source_dir2
    
}

# Function to copy file
copy_file() {
    local source_file="$1"
    local target_file="$2"

    # Compare size and modification dates of the files
    if [[ -f "$target_file" ]]; then
        source_size=$(stat -c %s "$source_file")
        target_size=$(stat -c %s "$target_file")
        source_date=$(stat -c %Y "$source_file")
        target_date=$(stat -c %Y "$target_file")

        if [[ $source_size -gt $target_size || $source_date -gt $target_date ]]; then
            cp "$source_file" "$target_file" 1>> $logfile 2>> $errorlog 
            echo "Copied: $source_file -> $target_file" >> $logfile
        fi
    else
        cp "$source_file" "$target_file" 1>> $logfile 2>> $errorlog 
        echo "Copied: $source_file -> $target_file" >> $logfile
    fi
}

# Recursive function to traverse directories
traverse_directories() {
    local source_dir="$1"
    local target_dir="$2"

    # Create target directory if it doesn't exist
    if [[ ! -d "$target_dir" ]]; then
        mkdir -p "$target_dir"
    fi

    # Traverse files and directories in source directory
    for file in "$source_dir"/*; do
        counter=$(( $counter +1 ))
        echo -ne "\e[0mKopiuje plik: \e[32m$counter"'\r'
        if [[ -f "$file" ]]; then
            # Copy file to target directory
            relative_path="${file#$source_dir}"
            target_file="$target_dir$relative_path"
            copy_file "$file" "$target_file"
        elif [[ -d "$file" ]]; then
            # Recursively traverse subdirectories
            relative_path="${file#$source_dir}"
            target_subdir="$target_dir$relative_path"
            traverse_directories "$file" "$target_subdir"
        fi
    done
}

end_f() {
    echo -e "Skopiowano: $counter plików"
    echo -e "$end_separator" && >> $logfile && >>$errorlog
}
# Start traversing directories

start
traverse_directories "$source_dir1" "$target_dir"
traverse_directories "$source_dir2" "$target_dir"
end_f

