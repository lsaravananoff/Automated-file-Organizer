import os
import shutil
from pathlib import Path

EXTENSION_MAP = {
    ".pdf": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".txt": "Documents",
    ".ppt": "Documents",
    ".pptx": "Documents",
    ".xls": "Documents",
    ".xlsx": "Documents",

    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".webp": "Images",

    ".mp4": "Videos",
    ".mkv": "Videos",
    ".mov": "Videos",
    ".avi": "Videos",

    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",

    ".py": "Code",
    ".js": "Code",
    ".html": "Code",
    ".css": "Code",
    ".java": "Code",
    ".cpp": "Code",
}

def get_unique_path(destination):
    """Avoid overwriting a file with the same name."""
    if not destination.exists():
        return destination

    counter = 1
    while True:
        new_name = (
            f"{destination.stem}_{counter}"
            f"{destination.suffix}"
        )
        new_path = destination.with_name(new_name)

        if not new_path.exists():
            return new_path

        counter += 1

def organize_files(folder_path):
    folder = Path(folder_path).expanduser().resolve()

    if not folder.is_dir():
        print("Error: The folder does not exist.")
        return

    moved_count = 0
    skipped_count = 0

    for item in folder.iterdir():
        if not item.is_file():
            continue

        category = EXTENSION_MAP.get(
            item.suffix.lower(), "Other"
        )

        destination_folder = folder / category

        try:
            destination_folder.mkdir(
                parents=True, exist_ok=True
            )

            destination = get_unique_path(
                destination_folder / item.name
            )

            shutil.move(str(item), str(destination))
            print(f"Moved: {item.name} -> {category}")
            moved_count += 1

        except (PermissionError, OSError, shutil.Error) as error:
            print(f"Skipped: {item.name} - {error}")
            skipped_count += 1

    print("\n========== ORGANIZATION SUMMARY ==========")
    print(f"Files moved: {moved_count}")
    print(f"Files skipped: {skipped_count}")
    print("Organization completed.")
    
if __name__ == "__main__":
    print("AUTOMATED FILE ORGANIZER")
    folder_path = input(
        "Enter the folder path to organize: "
    ).strip().strip('"')

    organize_files(folder_path)