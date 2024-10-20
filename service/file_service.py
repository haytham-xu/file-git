
from support.bdwp_support import bdwp_instance
from support import file_support

def list_cloud_file_recursion(remote_path):
    _, file_list = bdwp_instance.list_folder_file_recursion(remote_path)
    return file_list

def download_file(cloud_download_absolute_virtual_path, local_download_absolute_virtual_path):
    cloud_download_absolute_real_path = file_support.convert_to_unix_path(cloud_download_absolute_virtual_path)
    local_download_absolute_real_path = file_support.real_local_path_convert(local_download_absolute_virtual_path)
    bdwp_instance.download_file_with_path(cloud_download_absolute_real_path, local_download_absolute_real_path)

def upload_file(local_upload_absolute_virtual_path, cloud_upload_absolute_virtual_path):
    cloud_upload_absolute_real_path = file_support.convert_to_unix_path(cloud_upload_absolute_virtual_path)
    local_upload_absolute_real_path = file_support.real_local_path_convert(local_upload_absolute_virtual_path)
    bdwp_instance.upload_file(local_upload_absolute_real_path, cloud_upload_absolute_real_path)

def move_file_folder(cloud_source_file_virtual_path, cloud_target_folder_virtual_path):
    cloud_source_file_real_path = file_support.convert_to_unix_path(cloud_source_file_virtual_path)
    cloud_target_folder_real_path = file_support.convert_to_unix_path( cloud_target_folder_virtual_path)
    bdwp_instance.move_file_folder(cloud_source_file_real_path, cloud_target_folder_real_path)

def is_file_exist_in_cloud(cloud_file_virtual_path:str):
    cloud_file_name, cloud_file_parent_path = file_support.virtual_get_file_name_and_parent_path(cloud_file_virtual_path)
    res = bdwp_instance.search_file(cloud_file_name, cloud_file_parent_path)
    return len(res['list']) != 0
