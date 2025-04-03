#################################################################################

import os
import shutil

#################################################################################

def empty(file_path):
    with open(file_path, 'r') as file:
        return file.read(1) == ''
    
def list_load(file_path):
    with open(file_path, 'r') as file:
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
            if dir_name == '__pycache__':
                pycache_path = os.path.join(root, dir_name)
                shutil.rmtree(pycache_path)
                print(f"Removed: {pycache_path}")
                
def create(file_path):
    with open(file_path, 'w') as file:
        pass

def remove_lower(dir_path):
    for root, dirs, files in os.walk(dir, topdown=False):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            os.remove(file_path)
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            os.rmdir(dir_path)
#################################################################################