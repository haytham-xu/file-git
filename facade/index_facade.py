
import os
import hashlib
from service import file_service
from support import file_support
from service import buffer_service
from model.logger import logger_instance

def get_local_index(local_vpath):
    local_dict = {}
    real_local_root_path = file_support.real_local_path_convert(local_vpath)
    for real_parent_path, dirnames, filenames in os.walk(real_local_root_path):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        for filename in filenames:
            # ignore hidden files
            if filename.startswith('.'):
                continue
            virtual_parent_path = file_support.vpath_convert(real_parent_path)
            virtual_file_path = file_support.merge_vpath(virtual_parent_path, filename)
            file_size = file_support.get_file_size(virtual_file_path)
            middle_vpath, middle_vpath_hash = file_support.get_middle_path_and_hash(virtual_file_path, local_vpath)
            local_dict[middle_vpath_hash] = {
                'middle_path': middle_vpath,
                'size': file_size
            }
    return local_dict

def get_cloud_index(cloud_root_vpath):
    logger_instance.log_debug("get_cloud_index", cloud_root_vpath)
    cloud_root_real_unix_path = file_support.convert_to_vpath(cloud_root_vpath)
    logger_instance.log_debug("get_cloud_index", cloud_root_real_unix_path)
    file_dict = file_service.list_cloud_file_recursion(cloud_root_real_unix_path)
    logger_instance.log_debug("get_cloud_index", str(file_dict))
    remote_dict = {}
    for file_info in file_dict:
        file_unix_rpath = file_info["path"]
        # if any(part.startswith('.') for part in real_unix_file_path.split("/")):
        #     continue
        if file_info["server_filename"].startswith('.'):
            continue
        file_size = file_info["size"]
        real_unix_middle_path = file_unix_rpath.removeprefix(cloud_root_real_unix_path)
        middle_path_for_hash = buffer_service.get_unencrypted_path(real_unix_middle_path)
        file_hash = hashlib.md5(middle_path_for_hash.encode()).hexdigest()
        remote_dict[file_hash] = {
            'middle_path': real_unix_middle_path,
            'size': file_size
        }
    return remote_dict

def get_only_in_local(local_index_json, cloud_index_json):
    only_in_local_json = {key: value for key, value in local_index_json.items() if key not in cloud_index_json}
    return only_in_local_json

def get_only_in_remote(local_index_json, cloud_index_json):
    only_in_remote_json = {key: value for key, value in cloud_index_json.items() if key not in local_index_json}
    return only_in_remote_json

def get_local_remote_diff(local_index_json, cloud_index_json):
    diff = {}
    return diff
