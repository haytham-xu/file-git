
from concurrent.futures import ThreadPoolExecutor

from model.constant import FilegitConstant
from model.file_git import fgit_instance
from service import file_service
from service import buffer_service
from service import trash_service

from model.config import config_instance

from model.queue import Action, QueueItem
from support import file_support
from model.logger import logger_instance

from threading import Lock

import redis

class QueueManager:
    KEY_LOCK = "lock"
    KEY_ACTION_FOLDER = "action_folder"
    KEY_MESSAGE_QUEUE = "message_queue"
    KEY_DEAD_QUEUE = "dead_queue"

    def __init__(self):
        self.redis_instance = redis.Redis(host='localhost', port=6379, db=0)
        self.lock = Lock()

    # lock operation
    def acquire_lock(self):
        if not self.is_queue_empty():
            raise Exception("Queue is not empty, can not acquire lock")
        self.release_lock()    
        self.redis_instance.set(QueueManager.KEY_LOCK, str(True))
        
    def release_lock(self):
        self.redis_instance.set(QueueManager.KEY_LOCK, str(False))
    def is_lock(self):
        return self.redis_instance.get(QueueManager.KEY_LOCK) == str(True)

    # action folder operation
    def get_action_folder(self):
        return self.redis_instance.get(QueueManager.KEY_ACTION_FOLDER).decode('utf-8')
    def set_action_folder(self, action_folder_vpath):
        self.redis_instance.set(QueueManager.KEY_ACTION_FOLDER, action_folder_vpath)

    # queue operation
    def is_queue_empty(self):
        return self.redis_instance.llen(QueueManager.KEY_MESSAGE_QUEUE) == 0

    # message queue operation
    def push(self, middle_vpath:str, action:Action):
        index_item = QueueItem(middle_vpath, action)
        self.redis_instance.lpush(QueueManager.KEY_MESSAGE_QUEUE, index_item.to_json())

    def trigger(self, max_workers=5):
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            while True:
                message = self.redis_instance.brpop(QueueManager.KEY_MESSAGE_QUEUE, timeout=5)
                if message == None:
                    print("Queue is empty, exiting...")
                    break
                a_queue_item = QueueItem.from_string(message[1].decode('utf-8'))
                executor.submit(self.process_message, a_queue_item)

    def process_message(self, a_queue_item:QueueItem):
        retries = 0
        while retries < FilegitConstant.MAX_RETRIES:
            try:
                local_root_vpath = file_support.get_current_vpath()
                file_local_vpath = file_support.merge_vpath(config_instance.get_local_vpath(), a_queue_item.get_middle_vpath())
                file_vpath_in_buffer = buffer_service.get_file_buffer_path(fgit_instance.get_buffer_folder_vpath(local_root_vpath), a_queue_item.get_middle_vpath())
                file_cloud_vpath_for_local_use = buffer_service.get_file_cloud_path_for_local_use(config_instance.get_remote_vpath(), a_queue_item.get_middle_vpath())
                file_vpath_in_remote_for_cloud_use = buffer_service.get_file_cloud_path_for_cloud_use(config_instance.get_remote_vpath(), a_queue_item.get_middle_vpath())
                if a_queue_item.get_action() == Action.DOWNLOAD:
                    source_file_vpath_in_buffer = file_support.merge_vpath(fgit_instance.get_buffer_folder_vpath(local_root_vpath), a_queue_item.get_middle_vpath())
                    file_service.download_file(file_cloud_vpath_for_local_use, source_file_vpath_in_buffer)
                    buffer_service.move_to_local(source_file_vpath_in_buffer)
                    buffer_service.post_move_to_local(source_file_vpath_in_buffer)
                elif a_queue_item.get_action() == Action.UPLOAD:
                    buffer_service.move_to_buffer(file_local_vpath, local_root_vpath, fgit_instance.get_buffer_folder_vpath(local_root_vpath), config_instance.get_mode(), config_instance.get_password())
                    file_service.upload_file(file_vpath_in_buffer, file_vpath_in_remote_for_cloud_use)
                    buffer_service.post_move_to_buffer(file_vpath_in_buffer)
                elif a_queue_item.get_action() == Action.LOCAL_DELETE:
                    trash_service.local_move_to_trash(file_local_vpath)
                elif a_queue_item.get_action() == Action.REMOTE_DELETE:
                    trash_service.remote_move_to_trash(file_support.merge_vpath(config_instance.get_remote_vpath(), a_queue_item.get_middle_vpath()))
                elif a_queue_item.get_action() == Action.ONLY_ENCRYPTED:
                    buffer_service.move_to_buffer(file_local_vpath)
                else:
                    pass
                logger_instance.log_success(a_queue_item.get_action(), file_local_vpath, file_vpath_in_remote_for_cloud_use)
                break
            except Exception as e:
                retries += 1
                print(e)
                logger_instance.log_error("fail {} times: ".format(retries) + a_queue_item.get_action(), file_local_vpath, file_vpath_in_remote_for_cloud_use, e)
                
        else:
            logger_instance.log_error("move to dead queue ".format(retries) + a_queue_item.get_action(), file_local_vpath, file_vpath_in_remote_for_cloud_use, e)
            self.redis_instance.lpush(QueueManager.KEY_DEAD_QUEUE, a_queue_item.to_json())

queue_instance = QueueManager()
