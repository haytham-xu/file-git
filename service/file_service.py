
from support.bdwp_support import bdwp_instance
from support import file_support

def list_cloud_file_recursion(remote_path):
    _, file_list = bdwp_instance.list_folder_file_recursion(remote_path)
    return file_list

def download_file(cloud_download_absolute_path, local_download_absolute_path):
    bdwp_instance.download_file_with_path(cloud_download_absolute_path, local_download_absolute_path)

def upload_file(local_upload_absolute_path, cloud_upload_absolute_path):
    bdwp_instance.upload_file(local_upload_absolute_path, cloud_upload_absolute_path)

def move_file_folder(cloud_source_file_path, cloud_target_folder_path):
    bdwp_instance.move_file_folder(cloud_source_file_path, cloud_target_folder_path)

def is_file_exist_in_cloud(cloud_file_path:str):
    search_key = file_support.get_file_folder_name(cloud_file_path)
    parent_path = file_support.get_file_folder_parent_path(cloud_file_path)
    res = bdwp_instance.search_file(search_key, parent_path)
    return len(res['list']) != 0
