

import os
import hashlib


from datetime import datetime

from support import file_support
from support import fgit_support

action_name = "duplicate"

def command_find_duplicate(virtual_source_path):
    
    current_action_folder_name = fgit_support.get_action_folder_name(action_name)
    current_action_folder_path = file_support.merge_vpath(constant_support.ACTION_FOLDER_VPATH, current_action_folder_name)
    file_support.create_local_folder(current_action_folder_path)

    index_file_path = file_support.merge_vpath(current_action_folder_path, "index.json")
    report_file_path = file_support.merge_vpath(current_action_folder_path, "report.json")
    
    
    all_file_index = {}
    duplicate_index = {}
    
    buffer = 1000
    index = 0
    
    real_local_root_path = file_support.convert_to_rpath(virtual_source_path)
    for real_parent_path, dirnames, filenames in os.walk(real_local_root_path):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        
        for filename in filenames:
            if filename.startswith('.'):
                continue
            virtual_parent_path = file_support.vpath_convert(real_parent_path)
            virtual_file_path = file_support.merge_vpath(virtual_parent_path, filename)
            file_name, file_size, file_md5 = get_filename_size_md5(virtual_file_path)
            file_code = "{}-{}-{}".format(file_name, file_size, file_md5)
            
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"{current_time}: {virtual_file_path}")
            
            if file_code not in all_file_index:
                all_file_index[file_code] = []
            all_file_index[file_code].append(virtual_file_path)
            index += 1
            
            if index >= buffer:
                file_support.real_write_json_file(index_file_path, all_file_index)
                index = 0
                
    if index != 0:
        file_support.real_write_json_file(index_file_path, all_file_index)
            
    for a_code in all_file_index:
        duplicate_list = all_file_index[a_code]
        if len(duplicate_list) >= 2:
            duplicate_index[a_code] = duplicate_list
    
    file_support.real_write_json_file(report_file_path, duplicate_index)    

def get_filename_size_md5(virtual_file_path):
    real_file_path = file_support.convert_to_rpath(virtual_file_path)
    file_name = os.path.basename(real_file_path)
    file_size = os.path.getsize(real_file_path)
    md5_hash = hashlib.md5()
    with open(real_file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    file_md5 = md5_hash.hexdigest()
    return file_name, file_size, file_md5
