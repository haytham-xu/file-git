
from datetime import datetime

from support.config_support import config_instance
from support.constant_support import constant_instance

from support import file_support
from service import file_service

def local_move_to_trash(local_virtual_path):
    now = datetime.now()
    formatted_date = now.strftime("%Y%m%d")
    today_trash_virtual_path = file_support.virtual_merge_path(constant_instance.get_virtual_trash_folder_path(), formatted_date)
    file_middle_virtual_path = local_virtual_path.removeprefix(config_instance.get_virtual_local_path())
    target_path_in_virtual_trash = file_support.virtual_merge_path(today_trash_virtual_path, file_middle_virtual_path)
    file_support.real_move_file_folder(local_virtual_path, target_path_in_virtual_trash)

def remote_move_to_trash(cloud_virtual_path):
    now = datetime.now()
    formatted_date = now.strftime("%Y%m%d")
    today_trash_virtual_path = file_support.virtual_merge_path(config_instance.get_virtual_remote_path(), ".trash", formatted_date)
    file_middle_virtual_path = cloud_virtual_path.removeprefix(config_instance.get_virtual_remote_path())
    
    _, file_parent_middle_virtual_path = file_support.virtual_get_file_name_and_parent_path(file_middle_virtual_path)
    target_path_in_trash = file_support.virtual_merge_path(today_trash_virtual_path, file_parent_middle_virtual_path)
    file_service.move_file_folder(cloud_virtual_path, target_path_in_trash)

