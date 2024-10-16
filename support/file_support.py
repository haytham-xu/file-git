
import os
import re
import json
import shutil

# file/folder operation
# ---------------------------------------------------------------------------------------
def create_folder(folder_path):
    if not is_exist(folder_path):
        os.makedirs(folder_path)

def create_file(file_path):
    open(file_path, 'w').close()

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

# json/yaml operation
# ---------------------------------------------------------------------------------------
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data
