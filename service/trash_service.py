
from datetime import datetime

from model.config import config_instance
from model.file_git import fgit_instance
from model.logger import logger_instance

from support import file_support
from service import file_service

def local_move_to_trash(file_local_vpath):
    now = datetime.now()
    formatted_date = now.strftime("%Y%m%d")
    local_root_vapth = file_support.get_current_vpath()
    today_trash_vpath = file_support.merge_vpath(fgit_instance.get_trash_folder_vpath(local_root_vapth), formatted_date)

    file_support.create_local_folder(today_trash_vpath)
    file_middle_vpath = file_local_vpath.removeprefix(local_root_vapth)
    target_path_in_virtual_trash = file_support.merge_vpath(today_trash_vpath, file_middle_vpath)
    file_support.real_move_file_folder(file_local_vpath, target_path_in_virtual_trash)

    # check parent, if parent is empty, remove parent folder
    file_support.local_delete_empty_parent_folders(file_local_vpath)

def remote_move_to_trash(file_cloud_vpath):
    now = datetime.now()
    formatted_date = now.strftime("%Y%m%d")
    today_trash_vpath = file_support.merge_vpath(config_instance.get_remote_vpath(), ".trash", formatted_date)

    file_middle_vpath = file_cloud_vpath.removeprefix(config_instance.get_remote_vpath())
    
    _, file_parent_middle_vpath = file_support.get_file_name_and_parent_vpath(file_middle_vpath)
    target_path_in_trash = file_support.merge_vpath(today_trash_vpath, file_parent_middle_vpath)

    file_service.cloud_move_file_folder(file_cloud_vpath, target_path_in_trash)

    # check parent, if parent is empty, remove parent folder
    cloud_delete_empty_parent_folders(file_cloud_vpath)


def cloud_delete_empty_parent_folders(file_cloud_vpath):
    _, parent_folder_vpath = file_support.get_file_name_and_parent_vpath(file_cloud_vpath)
    while True:
        folder_size = len(file_service.list_cloud_file_recursion(parent_folder_vpath))
        if folder_size == 0:
            file_service.cloud_delete_folder(parent_folder_vpath)
            _, parent_folder_vpath = file_support.get_file_name_and_parent_vpath(parent_folder_vpath)
        else:
            break
