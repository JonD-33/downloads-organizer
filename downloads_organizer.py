import shutil
from pathlib import Path

# -------------------------------------------------------
# File categories mapped to corresponding file extensions.
# Each key represents a target directory name that will be
# created under the Downloads folder. The associated list
# defines which file extensions belong in that directory.
# -------------------------------------------------------
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
    """
    Determine the appropriate category directory for the given file based on its extension.

    Parameters
    ----------
    file_path : Path
        The file path to evaluate.

    Returns
    -------
    str
        The name of the category directory, or 'Other' if the extension is unrecognized.
    """
    ext = file_path.suffix.lower()

    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category

    return "Other"


def clean_folder(folder: Path) -> None:
    """
    Move each non directory file in the specified folder into a category specific subdirectory.
    Categories are determined by file extension and defined in FILE_CATEGORIES.
    """
    print(f"Organizing downloads folder: {folder}")

    if not folder.exists() or not folder.is_dir():
        print("Specified folder is invalid or unavailable.")
        return

    for item in folder.iterdir():
        # Skip directories, only process files located directly under Downloads
        if item.is_dir():
            continue

        category = get_category(item)
        destination_dir = folder / category
        destination_dir.mkdir(exist_ok=True)

        destination_path = destination_dir / item.name

        # Resolve potential naming conflicts by incrementing a numerical suffix
        counter = 1
        while destination_path.exists():
            new_name = f"{item.stem}_{counter}{item.suffix}"
            destination_path = destination_dir / new_name
            counter += 1

        print(f"Moving {item.name} to {category}/")
        shutil.move(str(item), str(destination_path))

    print("Completed. Files have been organized by category.")


if __name__ == "__main__":
    # Default target directory is the current user's Downloads folder
    downloads_folder = Path.home() / "Downloads"
    clean_folder(downloads_folder)
