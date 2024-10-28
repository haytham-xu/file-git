

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

def get_latest_action_folder(action_folder_virtual_path):
    latest_folder_name = None
    latest_time = None
    for folder_name in file_support.real_listdir(action_folder_virtual_path):
        folder_virtual_path = file_support.virtual_merge_path(action_folder_virtual_path, folder_name)
        if file_support.real_is_local_exist(folder_virtual_path):
            try:
                time_str = folder_name.split('_')[0]
                # folder_time = datetime.strptime(time_str, "%Y%m%d%H%M")
                folder_time = datetime.strptime(time_str, "%Y%m%d")
                if latest_time is None or folder_time > latest_time:
                    latest_time = folder_time
                    latest_folder_name = folder_name
            except ValueError:
                continue
    return latest_folder_name

def trigger():

    action_folder_name = get_latest_action_folder(constant_instance.get_virtual_action_folder_path())
    current_action_folder_virtual_path = file_support.virtual_merge_path(constant_instance.get_virtual_action_folder_path(), action_folder_name)

    current_action_log_virtual_path = file_support.virtual_merge_path(current_action_folder_virtual_path, "log")
    logger_instance.init_log_file(current_action_log_virtual_path)
    
    queue_instance.acquire_lock()
    while not queue_instance.is_queue_empty():
        a_key: str
        a_queue_item: QueueItem
        a_key, a_queue_item = queue_instance.get_a_queue_item()

        file_virtual_path_in_local = file_support.virtual_merge_path(config_instance.get_virtual_local_path(), a_queue_item.get_virtual_middle_path())
        file_virtual_path_in_buffer = buffer_service.get_file_buffer_path(constant_instance.get_virtual_buffer_folder_path(), a_queue_item.get_virtual_middle_path())
        file_cloud_virtual_path_for_local_use = buffer_service.get_file_cloud_path_for_local_use(config_instance.get_virtual_remote_path(), a_queue_item.get_virtual_middle_path())
        file_virtual_path_in_remote_for_cloud_use = buffer_service.get_file_cloud_path_for_cloud_use(config_instance.get_virtual_remote_path(), a_queue_item.get_virtual_middle_path())
        try:
            queue_instance.update_queue_item(a_key, Status.IN_PROGRESS)
            queue_instance.write_queue()
            if a_queue_item.get_action() == Action.DOWNLOAD:
                source_file_virtual_path_in_buffer = file_support.virtual_merge_path(constant_instance.get_virtual_buffer_folder_path(), a_queue_item.get_virtual_middle_path())
                file_service.download_file(file_cloud_virtual_path_for_local_use, source_file_virtual_path_in_buffer)
                buffer_service.move_to_local(source_file_virtual_path_in_buffer)
                buffer_service.post_move_to_local(source_file_virtual_path_in_buffer)
            elif a_queue_item.get_action() == Action.UPLOAD:
                buffer_service.move_to_buffer(file_virtual_path_in_local)
                file_service.upload_file(file_virtual_path_in_buffer, file_virtual_path_in_remote_for_cloud_use)
                buffer_service.post_move_to_buffer(file_virtual_path_in_buffer)
            elif a_queue_item.get_action() == Action.LOCAL_DELETE:
                trash_service.local_move_to_trash(file_virtual_path_in_local)
            elif a_queue_item.get_action() == Action.REMOTE_DELETE:
                trash_service.remote_move_to_trash(file_support.virtual_merge_path(config_instance.get_virtual_remote_path(), a_queue_item.get_virtual_middle_path()))
            elif a_queue_item.get_action() == Action.ONLY_ENCRYPTED:
                buffer_service.move_to_buffer(file_virtual_path_in_local)
            else:
                pass
            queue_instance.removed_queue_item(a_key)
            queue_instance.write_queue()
            logger_instance.log_success(a_queue_item.get_action(), file_virtual_path_in_local, file_virtual_path_in_remote_for_cloud_use)
        except Exception as e:
            print(e)
            queue_instance.update_queue_item(a_key, Status.FAILED)
            queue_instance.write_queue()
            logger_instance.log_error(a_queue_item.get_action(), file_virtual_path_in_local, file_virtual_path_in_remote_for_cloud_use, e)
            
    if queue_instance.is_queue_empty():
        queue_instance.release_lock()
        queue_instance.set_virtual_action_folder("")
