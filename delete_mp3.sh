#!/bin/bash

# Directory containing the files
TARGET_DIR="/root/project/production/YTBOT/"

# Check if the directory exists
if [ -d "$TARGET_DIR" ]; then
    # Deleting .mp3 files in the target directory
    find "$TARGET_DIR" -type f -name "*.mp3" -exec rm {} \;
    echo "All .mp3 files in $TARGET_DIR have been deleted."
else
    echo "Directory $TARGET_DIR does not exist."
fi
