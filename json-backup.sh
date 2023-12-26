#!/bin/bash

# Name of the file to move
source_file="domoticz-log.json"

# Destination directory
destination_dir="json-log"

# Check if the source file exists
if [ -e "$source_file" ]; then
    # Check if the destination directory exists, otherwise create it
    if [ ! -d "$destination_dir" ]; then
        mkdir -p "$destination_dir"
    fi

    # Move the file to the destination directory
    mv "$source_file" "$destination_dir/"

    # Create a new empty file with the same name in the original location
    touch "$source_file"

    echo "The file '$source_file' has been moved to '$destination_dir', and a new empty file has been created in the original location."
else
    echo "The file '$source_file' does not exist in the current directory."
fi

