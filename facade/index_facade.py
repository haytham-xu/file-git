
import os
import hashlib
from service import file_service
from support import file_support
from service import buffer_service

def get_local_index(local_root_path):
    local_dict = {}
    for dirpath, dirnames, filenames in os.walk(local_root_path):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        
        for filename in filenames:
            if filename.startswith('.'):
                continue
            file_path = os.path.join(dirpath, filename)
            file_size = os.path.getsize(file_path)
            middle_path, middle_path_hash = file_support.get_middle_path_and_hash(file_path, local_root_path)
            local_dict[middle_path_hash] = {
                'middle_path': middle_path,
                'size': file_size
            }
    return local_dict


def get_cloud_index(cloud_root_path):
    file_dict = file_service.list_cloud_file_recursion(cloud_root_path)
    remote_dict = {}
    for file_info in file_dict:
        file_path = file_info["path"]
        
        if any(part.startswith('.') for part in file_path.split(os.sep)):
            continue
        
        if file_info["server_filename"].startswith('.'):
            continue
        
        file_size = file_info["size"]
        source_middle_path = os.path.relpath(file_path, cloud_root_path)
        middle_path_for_hash = buffer_service.get_unencrypted_path(source_middle_path)
        file_hash = hashlib.md5(middle_path_for_hash.encode()).hexdigest()
        remote_dict[file_hash] = {
            'middle_path': source_middle_path,
            'size': file_size
        }
    return remote_dict
