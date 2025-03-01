
from support.bdwp_support import bdwp_instance
from support import file_support

def download_file(cloud_download_abs_vpath, local_download_abs_vpath):
    cloud_download_abs_rpath = file_support.convert_to_vpath(cloud_download_abs_vpath)
    local_download_abs_rpath = file_support.real_local_path_convert(local_download_abs_vpath)
    file_support.real_check_and_create_parent_folder(local_download_abs_rpath)
    bdwp_instance.download_file_with_path(cloud_download_abs_rpath, local_download_abs_rpath)

def upload_file(local_upload_abs_vpath, cloud_upload_abs_vpath):
    cloud_upload_abs_rpath = file_support.convert_to_vpath(cloud_upload_abs_vpath)
    local_upload_abs_rpath = file_support.real_local_path_convert(local_upload_abs_vpath)
    bdwp_instance.upload_file(local_upload_abs_rpath, cloud_upload_abs_rpath)

def cloud_move_file_folder(source_file_vpath, target_folder_vpath):
    cloud_source_file_rpath = file_support.convert_to_vpath(source_file_vpath)
    cloud_target_folder_rpath = file_support.convert_to_vpath( target_folder_vpath)
    bdwp_instance.move_file_folder(cloud_source_file_rpath, cloud_target_folder_rpath)

def cloud_is_file_exist(vpath:str):
    cloud_file_name, cloud_file_parent_path = file_support.get_file_name_and_parent_vpath(vpath)
    return bdwp_instance.check_file_exists(cloud_file_name, cloud_file_parent_path)

def list_cloud_file_recursion(cloud_vpath):
    cloud_rpath = file_support.convert_to_vpath(cloud_vpath)
    return bdwp_instance.list_file_recursion(cloud_rpath)

def cloud_delete_folder(cloud_folder_vpath):
    cloud_rpath = file_support.convert_to_vpath(cloud_folder_vpath)
    return bdwp_instance.delete_file_folder(cloud_rpath)
