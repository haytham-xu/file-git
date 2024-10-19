
import os
import re
import json
import shutil
import hashlib

# file/folder operation
# ---------------------------------------------------------------------------------------
def create_folder(folder_path):
    if not is_exist(folder_path):
        os.makedirs(folder_path)

def create_file(file_path):
    parent_path = os.path.split(file_path)[0]
    create_folder(parent_path)
    open(file_path, 'w').close()

def copy_file_folder(source_path, target_path):
    if os.path.isdir(source_path):
        shutil.copytree(source_path, target_path)
    else:
        target_dir = os.path.dirname(target_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        shutil.copy(source_path, target_path)

def move_file_folder(source_path, target_path):
    parent_path = os.path.split(target_path)[0]
    create_folder(parent_path)
    shutil.move(source_path, target_path)

def delete_path(path):
    if is_exist(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

def write_file_byte(file_path:str, content):
    with open(file_path, 'wb+') as f:
        f.write(content)
    f.close()

# path operation
# ---------------------------------------------------------------------------------------
def get_middle_path_and_hash(file_path:str, root_path:str):
    middle_path = os.path.relpath(file_path, root_path)
    middle_path_hash = get_string_hash(middle_path)
    return middle_path, middle_path_hash

def get_string_hash(source_string:str):
    return hashlib.md5(source_string.encode()).hexdigest()

def is_exist(file_folder_path):
    return os.path.exists(file_folder_path) 

def get_file_folder_name(file_folder_path:str):
    return os.path.split(file_folder_path)[1]

def get_file_folder_parent_path(file_folder_path:str):
    return os.path.split(file_folder_path)[0]

def merge_path(*path_segments):
    path_list = []
    for segment in path_segments:
        parts = re.split(r'[\\/]', segment)
        path_list.extend(parts)
    path_list = [p for p in path_list if p]
    return os.path.sep + os.path.join(*path_list)

def convert_to_unix_path(a_path:str):
    normalized_path = os.path.normpath(a_path)
    components = normalized_path.split(os.sep)
    return "/".join(components)

# json/yaml operation
# ---------------------------------------------------------------------------------------
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def write_json_file(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
