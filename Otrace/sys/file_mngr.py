#################################################################################

import os
import shutil

#################################################################################


def empty(file_path):
    with open(file_path, "r") as file:
        return file.read(1) == ""


def list_load(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    return lines


def restore(file_path):
    lines = list_load(file_path)
    return lines


def check(file_path):
    if os.path.exists(file_path):
        return True
    else:
        # File doesn't exist
        return False


def remove_pycache(directory):
    for root, dirs, _ in os.walk(directory):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                pycache_path = os.path.join(root, dir_name)
                shutil.rmtree(pycache_path)
                print(f"Removed: {pycache_path}")


def create(file_path):
    with open(file_path, "w") as file:
        pass


def folder_create(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"Created directory: {dir_path}")
    else:
        print(f"Directory already exists: {dir_path}")


def remove_lower(dir_path):
    for root, dirs, files in os.walk(dir_path, topdown=False):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                os.remove(file_path)
                print(f"Removed file: {file_path}")
            except OSError as e:
                print(f"Error removing file {file_path}: {e}")

        for dir_name in dirs:
            dir_path_full = os.path.join(root, dir_name)
            try:
                os.rmdir(dir_path_full)
                print(f"Removed directory: {dir_path_full}")
            except OSError as e:
                print(f"Error removing directory {dir_path_full}: {e}")


def zip_folder(folder_path, zip_path):
    shutil.make_archive(zip_path, "zip", folder_path)
    print(f"Zipped folder {folder_path} to {zip_path}.zip")


def unzip_file(zip_path, extract_to):
    if not zip_path.endswith(".zip"):
        print("Error: Provided file is not a zip file.")
        return
    with shutil.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_to)
        print(f"Extracted {zip_path} to {extract_to}")


def copy_file(src_path, dest_path):
    try:
        shutil.copy(src_path, dest_path)
        print(f"Copied file from {src_path} to {dest_path}")
    except OSError as e:
        print(f"Error copying file: {e}")


def move_file(src_path, dest_path):
    try:
        shutil.move(src_path, dest_path)
        print(f"Moved file from {src_path} to {dest_path}")
    except OSError as e:
        print(f"Error moving file: {e}")


def rename_file(file_path, new_name):
    dir_path = os.path.dirname(file_path)
    new_path = os.path.join(dir_path, new_name)
    try:
        os.rename(file_path, new_path)
        print(f"Renamed file {file_path} to {new_path}")
    except OSError as e:
        print(f"Error renaming file: {e}")


def get_file_size(file_path):
    try:
        size = os.path.getsize(file_path)
        print(f"Size of {file_path}: {size} bytes")
        return size
    except OSError as e:
        print(f"Error getting size of file: {e}")
        return None


def list_files_in_directory(dir_path):
    try:
        files = [
            f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))
        ]
        print(f"Files in {dir_path}: {files}")
        return files
    except OSError as e:
        print(f"Error listing files in directory: {e}")
        return []


def list_directories_in_directory(dir_path):
    try:
        directories = [
            d for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))
        ]
        print(f"Directories in {dir_path}: {directories}")
        return directories
    except OSError as e:
        print(f"Error listing directories in directory: {e}")
        return []


def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f"Deleted file: {file_path}")
    except OSError as e:
        print(f"Error deleting file: {e}")


def copy_folder(src_path, dest_path):
    try:
        shutil.copytree(src_path, dest_path)
        print(f"Copied folder from {src_path} to {dest_path}")
    except OSError as e:
        print(f"Error copying folder: {e}")


def move_folder(src_path, dest_path):
    try:
        shutil.move(src_path, dest_path)
        print(f"Moved folder from {src_path} to {dest_path}")
    except OSError as e:
        print(f"Error moving folder: {e}")


#################################################################################
