import shutil
# Provides high level file operations including moving, copying, and deletion.

from pathlib import Path
# Offers an object oriented approach to filesystem paths.


# Mapping of category names to relevant file extensions, determining final destination folders for each type.
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".heic"],
    "Documents": [
        ".pdf", ".doc", ".docx", ".txt", ".rtf",
        ".ppt", ".pptx", ".xls", ".xlsx", ".csv", ".md"
    ],
    "Videos": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [
        ".py", ".js", ".ts", ".html", ".css", ".json", ".yml", ".yaml",
        ".java", ".c", ".cpp", ".cs", ".go", ".rs", ".rb", ".php"
    ],
    "Installers": [".exe", ".msi", ".dmg", ".pkg", ".deb"],
}


def get_category(file_path: Path) -> str:
    # Determine the appropriate category directory for a given file based on extension.

    ext = file_path.suffix.lower()
    # Extracts the suffix (extension) from the file name and normalizes to lowercase.


    for category, extensions in FILE_CATEGORIES.items():
        # Iterates through all configured categories and their associated extensions.

        if ext in extensions:
            # Checks whether the extracted extension belongs to this category.
            return category
            # Returns the category name once found.


    return "Other"
    # Falls back to a generic category if no match is detected.


def clean_folder(folder: Path) -> None:
    # Reorganizes files inside the specified folder into categorized subdirectories.

    print(f"Organizing downloads folder: {folder}")
    # Outputs the target folder being processed.


    if not folder.exists() or not folder.is_dir():
        # Confirms the provided folder exists and is a directory.

        print("Specified folder is invalid or unavailable.")
        # Informs the user that the folder path was not valid.
        return
        # Prevents further execution in the absence of a valid folder.


    for item in folder.iterdir():
        # Iterates over filesystem entries located directly inside the folder.


        if item.is_dir():
            # Identifies and excludes subdirectories from processing.
            continue
            # Continues with next entry, skipping directories.


        category = get_category(item)
        # Invokes classification logic to determine destination category directory.


        destination_dir = folder / category
        # Constructs a new Path object representing the destination subfolder.


        destination_dir.mkdir(exist_ok=True)
        # Creates destination directory when absent, without raising if it already exists.


        destination_path = destination_dir / item.name
        # Combines destination directory with the original file name to construct final path.


        counter = 1
        # Counter to help resolve filename conflicts.


        while destination_path.exists():
            # Continues until a non conflicting filename is available.

            new_name = f"{item.stem}_{counter}{item.suffix}"
            # Constructs a modified filename by appending numeric suffixes.

            destination_path = destination_dir / new_name
            # Updates destination path using modified filename.

            counter += 1
            # Increments suffix counter for each conflict detected.


        print(f"Moving {item.name} to {category}/")
        # Outputs the relocation operation being executed.


        shutil.move(str(item), str(destination_path))
        # Moves file to target path using high level filesystem operation.


    print("Completed. Files have been organized by category.")
    # Final status message confirming completion of the reorganization.


if __name__ == "__main__":
    # Ensures the following logic runs only when this script is executed directly.

    downloads_folder = Path.home() / "Downloads"
    # Defines default target path by combining user's home directory and Downloads folder.

    clean_folder(downloads_folder)
    # Executes folder reorganization using the configured Downloads path.
