
from datetime import datetime

from support.config_support import config_instance
from support.constant_support import constant_instance

from support import file_support
from service import file_service

def local_move_to_trash(local_path):
    now = datetime.now()
    formatted_date = now.strftime("%Y%m%d")
    today_trash_path = file_support.merge_path(constant_instance.get_trash_folder_path(), formatted_date)
    file_middle_path = local_path.removeprefix(config_instance.get_local_path())
    target_path_in_trash = file_support.merge_path(today_trash_path, file_middle_path)
    file_support.move_file_folder(local_path, target_path_in_trash)

def remote_move_to_trash(cloud_path):
    now = datetime.now()
    formatted_date = now.strftime("%Y%m%d")
    today_trash_path = file_support.merge_path(config_instance.get_remote_path(), ".trash", formatted_date)
    file_middle_path = cloud_path.removeprefix(config_instance.get_remote_path())
    file_name = file_support.get_file_folder_name(cloud_path)
    file_middle_path = file_middle_path.removesuffix(file_name)
    target_path_in_trash = file_support.merge_path(today_trash_path, file_middle_path)
    file_service.move_file_folder(cloud_path, target_path_in_trash)

