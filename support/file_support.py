
import os
import re
import json
import shutil
import hashlib

# file/folder operation
# ---------------------------------------------------------------------------------------


# path operation
# ---------------------------------------------------------------------------------------
def get_middle_path_and_hash(virtual_file_path:str, virtual_local_root_path:str):
    virtual_middle_path = virtual_file_path.removeprefix(virtual_local_root_path)
    virtual_middle_path_hash = get_string_hash(virtual_middle_path)
    return virtual_middle_path, virtual_middle_path_hash

def get_string_hash(virtual_middle_path:str):
    return hashlib.md5(virtual_middle_path.encode()).hexdigest()

def convert_to_unix_path(a_path:str):
    path_list = re.split(r'[\\/]', a_path)
    path_list = [p for p in path_list if p]
    res = "/" + "/".join(path_list)
    return res

# real json/yaml operation
# ---------------------------------------------------------------------------------------
def real_read_json_file(virtual_file_path):
    real_file_path = real_local_path_convert(virtual_file_path)
    with open(real_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def real_write_json_file(virtual_file_path, data):
    real_file_path = real_local_path_convert(virtual_file_path)
    with open(real_file_path, 'w') as file:
        json.dump(data, file, indent=4)
        
def real_write_file(virtual_file_path, data):
    real_file_path = real_local_path_convert(virtual_file_path)
    with open(real_file_path, 'w') as f:
        f.write(data)
        
def real_create_png(output_virtual_path, image, size_in_bytes):
    real_file_path = real_local_path_convert(output_virtual_path)
    with open(real_file_path, 'wb') as f:
        image.save(f, format='PNG')
        current_size = f.tell()
        if current_size < size_in_bytes:
            f.write(b'\0' * (size_in_bytes - current_size))

def real_write_file_byte(virtual_path:str, content):
    real_path = real_local_path_convert(virtual_path)
    with open(real_path, 'wb+') as f:
        f.write(content)
    f.close()
    
def real_append_file(virtual_path, content):
    real_path = real_local_path_convert(virtual_path)
    with open(real_path, 'a') as log_file:
        log_file.write(content)
    
# virtual path operation
# ---------------------------------------------------------------------------------------
def virtual_get_current_path():
    real_current_path = os.getcwd()
    normalized_path = os.path.normpath(real_current_path)
    components = normalized_path.split(os.sep)
    virtual_current_path = "/" + "/".join(components)
    return virtual_current_path

def virtual_merge_path(*path_segments):
    path_list = []
    for segment in path_segments:
        parts = segment.split("/")
        path_list.extend(parts)
    path_list = [p for p in path_list if p]
    res = "/" + "/".join(path_list)
    return res

def virtual_path_convert(real_path):
    path_list = real_path.split(os.path.sep)
    res = "/" + "/".join(path_list)
    return res

def virtual_get_file_name_and_parent_path(virtual_path):
    virtual_path_part_list = virtual_path.split("/")
    virtual_path_part_list = [p for p in virtual_path_part_list if p]
    virtual_file_name = virtual_path_part_list[-1]
    virtual_file_parent_path = "/" + "/".join(virtual_path_part_list[:-1])
    return virtual_file_name, virtual_file_parent_path

# real path operation
# ---------------------------------------------------------------------------------------
def real_local_path_convert(virtual_path):
    path_list = virtual_path.split("/")
    a = os.path.sep.join(path_list)
    if a[0] == "/":
        return a
    if a[0] == "\\":
        return a[1:]
    return a
    
def real_create_local_folder(virtual_path):
    if not real_is_local_exist(virtual_path):
        real_path = real_local_path_convert(virtual_path)
        os.makedirs(real_path)

def real_create_local_file(virtual_path):
    real_path = real_local_path_convert(virtual_path)
    parent_path = os.path.split(real_path)[0]
    real_create_local_folder(parent_path)
    open(real_path, 'w').close()

def real_copy_file_folder(virtual_source_path, virtual_target_path):
    real_source_path = real_local_path_convert(virtual_source_path)
    real_target_path = real_local_path_convert(virtual_target_path)
    if os.path.isdir(real_source_path):
        shutil.copytree(real_source_path, real_target_path)
    else:
        target_dir = os.path.dirname(real_target_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        shutil.copy(real_source_path, real_target_path)

def real_move_file_folder(virtual_source_path, virtual_target_path):
    real_source_path = real_local_path_convert(virtual_source_path)
    real_target_path = real_local_path_convert(virtual_target_path)
    parent_path = os.path.split(real_target_path)[0]
    real_create_local_folder(parent_path)
    shutil.move(real_source_path, real_target_path)
    
def real_is_dir(virtual_path):
    real_path = real_local_path_convert(virtual_path)
    return os.path.isdir(real_path)

def real_delete_local_path(virtual_path):
    real_path = real_local_path_convert(virtual_path)
    if real_is_local_exist(real_path):
        if os.path.isdir(real_path):
            shutil.rmtree(real_path)
        else:
            os.remove(real_path)
    
def real_is_local_exist(virtual_path:str):
    real_path = real_local_path_convert(virtual_path)
    return os.path.exists(real_path) 

def get_real_file_folder_local_name(virtual_path:str):
    real_path = real_local_path_convert(virtual_path)
    return os.path.split(real_path)[1]

def get_real_file_folder_parent_local_path(virtual_path:str):
    real_path = real_local_path_convert(virtual_path)
    return os.path.split(real_path)[0]

def real_listdir(virtual_path):
    real_path = real_local_path_convert(virtual_path)
    return os.listdir(real_path)

# file meta operation
# ---------------------------------------------------------------------------------------

def get_file_size(virtual_path):
    real_path = real_local_path_convert(virtual_path)
    return os.path.getsize(real_path)
    
