
from support.bdwp_support import bdwp_instance

def list_cloud_file_recursion(remote_path):
    _, file_list = bdwp_instance.list_folder_file_recursion(remote_path)
    return file_list

def download_file(cloud_download_absolute_path, local_download_absolute_path):
    bdwp_instance.download_file_with_path(cloud_download_absolute_path, local_download_absolute_path)

def upload_file(local_upload_absolute_path, cloud_upload_absolute_path):
    bdwp_instance.upload_file(local_upload_absolute_path, cloud_upload_absolute_path)

def move_file_folder(cloud_source_file_path, cloud_target_folder_path):
    bdwp_instance.move_file_folder(cloud_source_file_path, cloud_target_folder_path)

