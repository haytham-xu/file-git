
import os
import re
import json
import shutil
import hashlib
import time


# file/folder operation
# ---------------------------------------------------------------------------------------


# path operation
# ---------------------------------------------------------------------------------------
def get_middle_path_and_hash(virtual_file_path:str, virtual_local_root_path:str):
    middle_vpath = virtual_file_path.removeprefix(virtual_local_root_path)
    middle_vpath_hash = get_string_hash(middle_vpath)
    return middle_vpath, middle_vpath_hash

def get_string_hash(middle_vpath:str):
    return hashlib.md5(middle_vpath.encode()).hexdigest()

def convert_to_vpath(a_path:str):
    path_list = re.split(r'[\\/]', a_path)
    path_list = [p for p in path_list if p]
    res = "/" + "/".join(path_list)
    return res

def merge_convert_vpath(*path_segments):
    merged_path = merge_vpath(*path_segments)
    return convert_to_vpath(merged_path)

# real json/yaml operation
# ---------------------------------------------------------------------------------------
def real_read_json_file(file_vpath):
    real_file_path = convert_to_rpath(file_vpath)
    with open(real_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def real_write_json_file(file_vpath, data):
    real_file_path = convert_to_rpath(file_vpath)
    with open(real_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        
def real_write_file(virtual_file_path, data):
    real_file_path = convert_to_rpath(virtual_file_path)
    with open(real_file_path, 'w', encoding='utf-8') as f:
        f.write(data)
        
def real_write_file_byte(vpath:str, content):
    rpath = convert_to_rpath(vpath)
    with open(rpath, 'wb+') as f:
        f.write(content)
    f.close()
    
def real_append_file(vpath, content):
    real_path = convert_to_rpath(vpath)
    with open(real_path, 'a', encoding='utf-8') as log_file:
        log_file.write(content)
    
# virtual path operation
# ---------------------------------------------------------------------------------------
def get_current_vpath():
    real_current_path = os.getcwd()
    normalized_path = os.path.normpath(real_current_path)
    components = [component for component in normalized_path.split(os.sep) if component]
    virtual_current_path = "/" + "/".join(components)
    return virtual_current_path

def merge_vpath(*path_segments):
    path_list = []
    for segment in path_segments:
        parts = segment.split("/")
        path_list.extend(parts)
    path_list = [p for p in path_list if p]
    res = "/" + "/".join(path_list)
    return res

def vpath_convert(real_path):
    path_list = real_path.split(os.path.sep)
    res = "/" + "/".join(path_list)
    return res

def get_file_name_and_parent_vpath(vpath):
    vpath_part_list = vpath.split("/")
    vpath_part_list = [p for p in vpath_part_list if p]
    virtual_file_name = vpath_part_list[-1]
    file_parent_vpath = "/" + "/".join(vpath_part_list[:-1])
    return virtual_file_name, file_parent_vpath

# real path operation
# ---------------------------------------------------------------------------------------
def convert_to_rpath(vpath):
    path_list = vpath.split("/")
    a = os.path.sep.join(path_list)
    if a[0] == "/":
        return a
    if a[0] == "\\":
        return a[1:]
    return a

def merge_convert_rpath(*path_segments):
    merged_path = merge_vpath(*path_segments)
    return convert_to_rpath(merged_path)

def create_local_folder(rpath):
    # funny, there would have thread security issue.
    if not is_local_exist(rpath):
        real_path = convert_to_rpath(rpath)
        os.makedirs(real_path, exist_ok=True)
        time.sleep(5)

def real_check_and_create_parent_folder(vpath):
    real_path = convert_to_rpath(vpath)
    parent_path = os.path.split(real_path)[0]
    if not os.path.exists(parent_path):
        os.makedirs(parent_path)

def real_create_local_file(vpath):
    real_path = convert_to_rpath(vpath)
    parent_path = os.path.split(real_path)[0]
    create_local_folder(parent_path)
    open(real_path, 'w').close()

def real_copy_file_folder(virtual_source_path, virtual_target_path):
    real_source_path = convert_to_rpath(virtual_source_path)
    real_target_path = convert_to_rpath(virtual_target_path)
    if os.path.isdir(real_source_path):
        shutil.copytree(real_source_path, real_target_path)
    else:
        target_dir = os.path.dirname(real_target_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        shutil.copy(real_source_path, real_target_path)

def real_move_file_folder(source_vpath, target_vpath):
    real_source_path = convert_to_rpath(source_vpath)
    real_target_path = convert_to_rpath(target_vpath)
    parent_path = os.path.split(real_target_path)[0]
    create_local_folder(parent_path)
    shutil.move(real_source_path, real_target_path)
    
def real_is_dir(vpath):
    real_path = convert_to_rpath(vpath)
    return os.path.isdir(real_path)

def real_delete_local_path(vpath):
    real_path = convert_to_rpath(vpath)
    if is_local_exist(real_path):
        if os.path.isdir(real_path):
            shutil.rmtree(real_path)
        else:
            os.remove(real_path)
    
def is_local_exist(vpath:str):
    real_path = convert_to_rpath(vpath)
    return os.path.exists(real_path) 

def get_real_file_folder_local_name(vpath:str):
    real_path = convert_to_rpath(vpath)
    return os.path.split(real_path)[1]

def get_real_file_folder_parent_local_path(vpath:str):
    real_path = convert_to_rpath(vpath)
    return os.path.split(real_path)[0]

def real_listdir(vpath):
    real_path = convert_to_rpath(vpath)
    return os.listdir(real_path)

def is_folder_empty(vpath):
    real_path = convert_to_rpath(vpath)
    with os.scandir(real_path) as it:
        return not any(it)

def local_delete_empty_parent_folders(file_local_vpath):
    _, parent_folder_vpath = get_file_name_and_parent_vpath(file_local_vpath)
    while True:
        # if current folder is not empty, end
        if not is_folder_empty(parent_folder_vpath):
            break
        # if current folder is local buffer, end
        if parent_folder_vpath == merge_vpath(get_current_vpath(), ".fgit", "buffer"):
            break
        real_delete_local_path(parent_folder_vpath)
        _, parent_folder_vpath = get_file_name_and_parent_vpath(parent_folder_vpath)

# file meta operation
# ---------------------------------------------------------------------------------------

def get_file_size(vpath):
    real_path = convert_to_rpath(vpath)
    return os.path.getsize(real_path)
    
