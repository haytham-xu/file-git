
import os

from datetime import datetime

from service import file_service
from service import buffer_service
from service import trash_service

from support.config_support import config_instance
from support.constant_support import constant_instance
from support.queue_support import queue_instance
from support.queue_support import Action, Status, QueueItem
from support import file_support
from support.logger_support import logger_instance

def get_latest_action_folder(action_folder_path):
    latest_folder = None
    latest_time = None
    for folder_name in os.listdir(action_folder_path):
        folder_path = os.path.join(action_folder_path, folder_name)
        if os.path.isdir(folder_path):
            try:
                time_str = folder_name.split('_')[0]
                # folder_time = datetime.strptime(time_str, "%Y%m%d%H%M")
                folder_time = datetime.strptime(time_str, "%Y%m%d")
                if latest_time is None or folder_time > latest_time:
                    latest_time = folder_time
                    latest_folder = folder_name
            except ValueError:
                continue
    return latest_folder

def trigger():

    action_folder_name = get_latest_action_folder(constant_instance.get_action_folder_path())
    current_action_folder_path = file_support.merge_path(constant_instance.get_action_folder_path(), action_folder_name)

    current_action_log_path = file_support.merge_path(current_action_folder_path, "log")
    logger_instance.init_log_file(current_action_log_path)
    
    queue_instance.acquire_lock()
    while not queue_instance.is_queue_empty():
        a_key: str
        a_queue_item: QueueItem
        a_key, a_queue_item = queue_instance.get_a_queue_item()

        file_path_in_local = file_support.merge_path(config_instance.get_local_path(), a_queue_item.get_middle_path())
        file_path_in_buffer = buffer_service.get_file_buffer_path(constant_instance.get_buffer_folder_path(), a_queue_item.get_middle_path())
        file_cloud_path_for_local_use = buffer_service.get_file_cloud_path_for_local_use(config_instance.get_remote_path(), a_queue_item.get_middle_path())
        file_path_in_remote_for_cloud_use = buffer_service.get_file_cloud_path_for_cloud_use(config_instance.get_remote_path(), a_queue_item.get_middle_path())
        try:
            queue_instance.update_queue_item(a_key, Status.IN_PROGRESS)
            if a_queue_item.get_action() == Action.DOWNLOAD:
                source_file_path_in_buffer = file_support.merge_path(constant_instance.get_buffer_folder_path(), a_queue_item.get_middle_path())
                file_service.download_file(file_cloud_path_for_local_use, source_file_path_in_buffer)
                buffer_service.move_to_local(source_file_path_in_buffer)
                buffer_service.post_move_to_local(source_file_path_in_buffer)
            elif a_queue_item.get_action() == Action.UPLOAD:
                buffer_service.move_to_buffer(file_path_in_local)
                file_service.upload_file(file_path_in_buffer, file_path_in_remote_for_cloud_use)
                buffer_service.post_move_to_buffer(file_path_in_buffer)
            elif a_queue_item.get_action() == Action.LOCAL_DELETE:
                trash_service.local_move_to_trash(file_path_in_local)
            elif a_queue_item.get_action() == Action.REMOTE_DELETE:
                trash_service.remote_move_to_trash(file_support.merge_path(config_instance.get_remote_path(), a_queue_item.get_middle_path()))
            else:
                pass
            queue_instance.removed_queue_item(a_key)
            queue_instance.write_queue()
            logger_instance.log_success(a_queue_item.get_action(), file_path_in_local, file_path_in_remote_for_cloud_use)
        except Exception as e:
            print(e)
            queue_instance.update_queue_item(a_key, Status.FAILED)
            queue_instance.write_queue()
            logger_instance.log_error(a_queue_item.get_action(), file_path_in_local, file_path_in_remote_for_cloud_use, e)
            
    if queue_instance.is_queue_empty():
        queue_instance.release_lock()
        queue_instance.set_action_folder("")
