import os
import datetime
import shutil

downloads_folder = "C:\\Users\\2003n\\Downloads"

categories = {
    "Documents": ["C:\\Users\\2003n\\Downloads\\Documents", [".pdf", ".docx", ".odt"]],
    "Presentations": ["C:\\Users\\2003n\\Downloads\\Presentations", [".pptx"]],
    "TextFiles": ["C:\\Users\\2003n\\Downloads\\TextFiles", [".txt"]],
    "Images": [
        "C:\\Users\\2003n\\Downloads\\Images",
        [".jpg", ".png", ".gif", ".jpeg", ".webp", ".svg"],
    ],
    "Videos": ["C:\\Users\\2003n\\Downloads\\Videos", [".mp4", ".avi"]],
    "Applications": ["C:\\Users\\2003n\\Downloads\\Applications", [".exe"]],
    "Archived": ["C:\\Users\\2003n\\Downloads\\Archived", [".rar", ".zip"]],
    "OtherFolders": ["C:\\Users\\2003n\\Downloads\\OtherFolders", []],
    "Coding": [
        "C:\\Users\\2003n\\Downloads\\Coding",
        [".html", ".cpp", ".h", ".xml", ".fig"],
    ],
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
            except Exception as e:
                print(f"Error moving file: {str(e)}")


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
                    print(f"Removed archive file: {file_path}")
                except Exception as e:
                    print(f"Error removing file: {str(e)}")
            else:
                organize_file(file_path, extension)
    try:
        # Now, check the "Archived" folder for extracted files
        for filename in os.listdir(f"{downloads_folder}/Archived"):
            file_path = os.path.join(f"{downloads_folder}/Archived", filename)
            if os.path.isfile(file_path):
                _, extension = os.path.splitext(filename)
                if extension.lower() in [".rar", ".zip"] and check_existing_folder(
                    filename
                ):
                    shutil.rmtree(
                        file_path
                    )  # Use shutil.rmtree to delete folders and their contents
                    print(f"Removed extracted archive files in {file_path}")
    except FileNotFoundError:
        pass


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
            except Exception as e:
                print(f"Error moving folder: {str(e)}")


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
                        print(f"Deleted {file_path}")
                    except Exception as e:
                        print(f"Error deleting file: {str(e)}")


def delete_empty_folders(directory):
    for root, dirs, _ in os.walk(directory, topdown=False):
        for dir_name in dirs:
            folder_path = os.path.join(root, dir_name)
            if not os.listdir(folder_path):
                print(f"Deleting empty folder: {folder_path}")
                try:
                    os.rmdir(folder_path)
                    print(f"Deleted {folder_path}")
                except Exception as e:
                    print(f"Error deleting folder: {str(e)}")


if __name__ == "__main__":
    print("Organizing Archive files")
    organize_archive_files()
    print("Organizing downloads...")
    organize_downloads()
    print("Checking for old files...")
    delete_old_files()

    print("Deleting empty folders...")
    delete_empty_folders(downloads_folder)

    print("Organization and cleanup complete.")
