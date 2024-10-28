
import os
import hashlib
from service import file_service
from support import file_support
from service import buffer_service

def get_local_index(virtual_local_root_path):
    local_dict = {}
    real_local_root_path = file_support.real_local_path_convert(virtual_local_root_path)
    for real_parent_path, dirnames, filenames in os.walk(real_local_root_path):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        
        for filename in filenames:
            if filename.startswith('.'):
                continue
            virtual_parent_path = file_support.virtual_path_convert(real_parent_path)
            virtual_file_path = file_support.virtual_merge_path(virtual_parent_path, filename)
            file_size = file_support.get_file_size(virtual_file_path)
            virtual_middle_path, virtual_middle_path_hash = file_support.get_middle_path_and_hash(virtual_file_path, virtual_local_root_path)
            local_dict[virtual_middle_path_hash] = {
                'middle_path': virtual_middle_path,
                'size': file_size
            }
    return local_dict


def get_cloud_index(cloud_root_virtual_path):
    cloud_root_real_unix_path = file_support.convert_to_unix_path(cloud_root_virtual_path)
    file_dict = file_service.list_cloud_file_recursion(cloud_root_real_unix_path)
    remote_dict = {}
    for file_info in file_dict:
        real_unix_file_path = file_info["path"]
        
        # if any(part.startswith('.') for part in real_unix_file_path.split("/")):
        #     continue
        if file_info["server_filename"].startswith('.'):
            continue
        file_size = file_info["size"]
        real_unix_middle_path = real_unix_file_path.removeprefix(cloud_root_real_unix_path)
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
    # for key, local_value in local_index_json.items():
    #     if key in cloud_index_json:
    #         cloud_value = cloud_index_json[key]
    #         if local_value['size'] != cloud_value['size']:
    #             diff[key] = {
    #                 'local': local_value,
    #                 'remote': cloud_value
    #             }
    return diff
