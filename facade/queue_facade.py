


from service import file_service
from service import buffer_service
from service import trash_service

from support.config_support import config_instance
from support.constant_support import constant_instance
from support.queue_support import queue_instance
from support.queue_support import Action, Status, QueueItem
from support import file_support
from support.logger_support import logger_instance

def triggrt():
    current_action_folder_path = file_support.merge_path(constant_instance.get_action_folder_path(), queue_instance.get_action_folder())

    if current_action_folder_path == "":
        raise Exception("No action folder found")

    current_action_log_path = file_support.join_path(current_action_folder_path, "log")
    logger_instance.init_log_file(current_action_log_path)
    
    queue_instance.acquire_lock()
    while not queue_instance.is_queue_empty():
        result = queue_instance.get_a_queue_item()
        a_key: str
        a_queue_item: QueueItem
        a_key, a_queue_item = result

        file_path_in_local = file_support.merge_path(config_instance.get_local_path(), a_queue_item.get_middle_path())
        file_path_in_buffer = buffer_service.get_file_buffer_path(constant_instance.get_buffer_folder_path(), a_queue_item.get_middle_path())
        file_path_in_remote = buffer_service.get_file_cloud_path(config_instance.get_remote_path(), a_queue_item.get_middle_path())
        try:
            if a_queue_item.action == Action.DOWNLOAD:
                file_service.download_file(file_path_in_remote, file_path_in_buffer)
                buffer_service.move_to_local(file_path_in_buffer)
                buffer_service.post_move_to_local(file_path_in_buffer)
            elif a_queue_item.action == Action.UPLOAD:
                buffer_service.move_to_buffer(file_path_in_local)
                file_service.upload_file(file_path_in_buffer, file_path_in_remote)
                buffer_service.post_move_to_buffer(file_path_in_buffer)
            elif a_queue_item.action == Action.LOCAL_DELETE:
                trash_service.local_move_to_trash(file_path_in_local)
            elif a_queue_item.action == Action.REMOTE_DELETE:
                trash_service.remote_move_to_trash(file_path_in_remote)
            else:
                pass
            queue_instance.removed_queue_item(a_key)
            logger_instance.log_success(a_queue_item.get_action(), file_path_in_local, file_path_in_remote)
        except Exception as e:
            queue_instance.update_queue_item(a_key, Status.FAILED)
            logger_instance.log_error(a_queue_item.get_action(), file_path_in_local, file_path_in_remote, e)
            print(e)
    if queue_instance.is_queue_empty():
        queue_instance.release_lock()
        queue_instance.set_action_folder("")
