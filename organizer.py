import os
import datetime
import shutil
import logging

# Set up logging
log_file = os.path.expanduser(
    "/home/nader/Coding/personal projects/automation scripts/Scripts/scripts.log"
)
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

downloads_folder = os.path.expanduser("~/Downloads")

categories = {
    "Documents": [
        os.path.join(downloads_folder, "Documents"),
        [".pdf", ".docx", ".odt"],
    ],
    "Presentations": [os.path.join(downloads_folder, "Presentations"), [".pptx"]],
    "TextFiles": [os.path.join(downloads_folder, "TextFiles"), [".txt"]],
    "Images": [
        os.path.join(downloads_folder, "Images"),
        [".jpg", ".png", ".gif", ".jpeg", ".webp", ".svg"],
    ],
    "Videos": [os.path.join(downloads_folder, "Videos"), [".mp4", ".avi"]],
    "Applications": [os.path.join(downloads_folder, "Applications"), [".sh", ".deb"]],
    "Archived": [os.path.join(downloads_folder, "Archived"), [".rar", ".zip", ".tar"]],
    "Packages": [os.path.join(downloads_folder, "Packages"), [".flatpakref"]],
    "OtherFolders": [os.path.join(downloads_folder, "OtherFolders"), []],
    "Coding": [
        os.path.join(downloads_folder, "Coding"),
        [".html", ".cpp", ".h", ".xml", ".fig"],
    ],
    "Sheets": [os.path.join(downloads_folder, "Sheets"), [".xlsx", "xls"]],
}


def get_current_date():
    return datetime.date.today().strftime("%Y-%m-%d")


def check_existing_folder(file_name):
    folder_path = os.path.join(downloads_folder, os.path.splitext(file_name)[0])
    return os.path.exists(folder_path)


def organize_file(file_path, extension):
    for folder_path, extensions in categories.values():
        if extension.lower() in extensions:
            os.makedirs(folder_path, exist_ok=True)
            destination = os.path.join(folder_path, os.path.basename(file_path))
            try:
                shutil.move(file_path, destination)
                logging.info(f"Moved file {file_path} to {destination}")
            except Exception as e:
                logging.error(
                    f"Error moving file {file_path} to {destination}: {str(e)}"
                )


def organize_archive_files():
    for filename in os.listdir(downloads_folder):
        file_path = os.path.join(downloads_folder, filename)
        if os.path.isfile(file_path):
            _, extension = os.path.splitext(filename)
            if extension.lower() in [".rar", ".zip"] and check_existing_folder(
                filename
            ):
                try:
                    os.remove(file_path)
                    logging.info(f"Removed archive file: {file_path}")
                except Exception as e:
                    logging.error(f"Error removing archive file {file_path}: {str(e)}")
            else:
                organize_file(file_path, extension)
    try:
        # Now, check the "Archived" folder for extracted files
        for filename in os.listdir(categories["Archived"][0]):
            file_path = os.path.join(categories["Archived"][0], filename)
            if os.path.isfile(file_path):
                _, extension = os.path.splitext(filename)
                if extension.lower() in [".rar", ".zip"] and check_existing_folder(
                    filename
                ):
                    shutil.rmtree(
                        file_path
                    )  # Use shutil.rmtree to delete folders and their contents
                    logging.info(f"Removed extracted archive files in {file_path}")
    except FileNotFoundError:
        logging.warning("No extracted archive files found")


def organize_downloads():
    for filename in os.listdir(downloads_folder):
        file_path = os.path.join(downloads_folder, filename)
        if os.path.isfile(file_path):
            _, extension = os.path.splitext(filename)
            organize_file(file_path, extension)
        elif os.path.isdir(file_path) and filename not in categories.keys():
            folder_path = categories["OtherFolders"][0]
            os.makedirs(folder_path, exist_ok=True)
            destination = os.path.join(folder_path, os.path.basename(file_path))
            try:
                shutil.move(file_path, destination)
                logging.info(f"Moved folder {file_path} to {destination}")
            except Exception as e:
                logging.error(
                    f"Error moving folder {file_path} to {destination}: {str(e)}"
                )


def delete_old_files():
    one_month_ago = datetime.datetime.now() - datetime.timedelta(days=30)
    for root, _, files in os.walk(downloads_folder):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path in [
                "./desktop.ini",
                "./organizer.py",
                "./downloads_watcher_starter.bat",
            ]:
                continue
            modification_time = datetime.datetime.fromtimestamp(
                os.path.getmtime(file_path)
            )
            if modification_time < one_month_ago:
                choice = input(f"Do you want to delete {file_path}? (yes/no): ").lower()
                if choice == "yes":
                    try:
                        os.remove(file_path)
                        logging.info(f"Deleted {file_path}")
                    except Exception as e:
                        logging.error(f"Error deleting file {file_path}: {str(e)}")


def delete_empty_folders(directory):
    for root, dirs, _ in os.walk(directory, topdown=False):
        for dir_name in dirs:
            folder_path = os.path.join(root, dir_name)
            if not os.listdir(folder_path):
                logging.info(f"Deleting empty folder: {folder_path}")
                try:
                    os.rmdir(folder_path)
                    logging.info(f"Deleted empty folder: {folder_path}")
                except Exception as e:
                    logging.error(
                        f"Error deleting empty folder {folder_path}: {str(e)}"
                    )


if __name__ == "__main__":
    try:
        logging.info("Starting organization and cleanup")
        logging.info("Organizing Archive files")
        organize_archive_files()
        logging.info("Organizing downloads...")
        organize_downloads()
        logging.info("Checking for old files...")
        delete_old_files()

        logging.info("Deleting empty folders...")
        delete_empty_folders(downloads_folder)

        logging.info("Organization and cleanup complete")
    except Exception as e:
        logging
