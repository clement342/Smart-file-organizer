import os
import shutil
from datetime import datetime

# Folder to organize
folder_path = r"C:\Users\Clement\Downloads"

# File categories
file_types = {
    "Images": [".jpg", ".jpeg", ".png"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Videos": [".mp4", ".mov"],
    "Music": [".mp3"],
    "Archives": [".zip", ".rar"],
}

# Track summary
summary = {
    "Images": 0,
    "Documents": 0,
    "Videos": 0,
    "Music": 0,
    "Archives": 0,
    "Others": 0,
    "Errors": 0,
}


def create_folder(path):
    """Create folder if it doesn't exist"""
    if not os.path.exists(path):
        os.makedirs(path)


def log_message(message):
    """Save logs to a file"""
    with open("organizer_log.txt", "a") as log:
        log.write(f"{datetime.now()} - {message}\n")


def move_file(file, folder_name):
    """Move file safely"""
    try:
        source = os.path.join(folder_path, file)
        destination_folder = os.path.join(folder_path, folder_name)
        destination = os.path.join(destination_folder, file)

        create_folder(destination_folder)
        shutil.move(source, destination)

        log_message(f"Moved {file} → {folder_name}")

        return True

    except Exception as e:
        log_message(f"ERROR moving {file}: {e}")
        summary["Errors"] += 1
        return False


def organize_files():
    """Main function to organize files"""

    for file in os.listdir(folder_path):

        file_path = os.path.join(folder_path, file)

        # Skip folders
        if os.path.isdir(file_path):
            continue

        _, extension = os.path.splitext(file)

        moved = False

        for folder_name, extensions in file_types.items():

            if extension.lower() in extensions:

                if move_file(file, folder_name):
                    summary[folder_name] += 1

                moved = True
                break

        # If file doesn't match any category
        if not moved:
            if move_file(file, "Others"):
                summary["Others"] += 1


def show_summary():
    """Display results"""

    print("\n===== ORGANIZATION SUMMARY =====")
    for key, value in summary.items():
        print(f"{key}: {value}")

    print("\nProcess completed successfully!")


# RUN PROGRAM
organize_files()
show_summary()
