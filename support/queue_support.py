
import json
from enum import Enum
from typing import List, Dict

from support import file_support
from support import constant_support

class Status(Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Action(Enum):
    DOWNLOAD = "DOWNLOAD"
    UPLOAD = "UPLOAD"
    LOCAL_DELETE = "LOCAL_DELETE"
    REMOTE_DELETE = "REMOTE_DELETE"
    ONLY_ENCRYPTED = "ONLY_ENCRYPTED"

class QueueItem:
    def __init__(self, middle_path:str="", action:Action=None, status:Status=Status.PENDING):
        self.middle_path = middle_path
        self.action = action
        self.status = status

    def get_virtual_middle_path(self):
        return self.middle_path
    def set_virtual_middle_path(self, middle_path):
        self.middle_path = middle_path
    def get_action(self):
        return self.action
    def set_action(self, action):
        self.action = action
    def get_status(self):
        return self.status
    def set_status(self, status):
        self.status = status

    @staticmethod
    def from_json(item):
        return QueueItem(
            middle_path=item['middle_path'],
            action=Action(item['action']),
            status=Status(item['status'])
        )



    def to_json(self):
        return json.dumps({
            'middle_path': self.middle_path,
            'action': self.action.value,
            'status': self.status.value
        })

class QueueManager:
    def __init__(self):
        self.lock = False
        self.key_set: List[str] = []
        self.queue_item: Dict[QueueItem] = {}
        self.action_folder_virtual_path = ""
        self.queue_file_virtual_path = ""
        self.buffer = 0

    def get_queue_item(self):
        return self.queue_item
    def get_key_set(self):
        return self.key_set
    def is_lock(self):
        return self.lock
    def acquire_lock(self):
        if self.lock != True:
            self.lock = True
    def release_lock(self):
        if self.lock != False:
            self.lock = False
            self.action_folder_virtual_path = None
            self.write_queue()
    def is_queue_empty(self):
        pending_count = sum(1 for item in self.queue_item.values() if item.get_status() == Status.PENDING)
        return pending_count == 0
    
    def set_virtual_action_folder(self, action_folder_virtual_path):
        self.action_folder_virtual_path = action_folder_virtual_path
    def get_virtual_action_folder(self):
        return self.action_folder_virtual_path
    def get_virtual_queue_file_path(self):
        return self.queue_file_virtual_path
    def set_virtual_queue_file_path(self, queue_file_virtual_path):
        self.queue_file_virtual_path = queue_file_virtual_path
    
    def get_a_queue_item(self):
        for a_key in self.key_set:
            a_queue_item:QueueItem = self.queue_item[a_key]
            if a_queue_item.get_status() == Status.PENDING:
                a_queue_item.set_status(Status.IN_PROGRESS)
                return a_key, a_queue_item
        raise ValueError("No queue item is in PENDING status.")
    
    def add_queue_item(self, key:str, queue_item: QueueItem):
        self.key_set.append(key)
        self.queue_item[key] = queue_item

    def removed_queue_item(self, key):
        self.key_set.remove(key)
        self.queue_item.pop(key)

    def update_queue_item(self, a_key, status):
        a_queue_item:QueueItem = self.queue_item[a_key]
        a_queue_item.set_status(status)

    def read_queue(self):
        if not file_support.real_is_local_exist(self.get_virtual_queue_file_path()):
            raise FileNotFoundError(f"queue_instance file '{self.get_virtual_queue_file_path()}' does not exist.")
        json_data = file_support.real_read_json_file(self.get_virtual_queue_file_path())
        self.lock = json_data['lock']
        self.key_set = json_data['key_set']
        self.action_folder_virtual_path = json_data['action_folder']
        self.queue_item = {key: QueueItem.from_json(item) for key, item in json_data['queue_item'].items()}   

    def write_queue(self):
        if self.is_queue_empty() or (not self.is_queue_empty() and self.buffer >= constant_support.buffer_size):
            json_data = {
                'lock': self.lock,
                'action_folder': self.action_folder_virtual_path,
                'key_set': self.key_set,
                'queue_item': {key: json.loads(item.to_json()) for key, item in self.queue_item.items()}
            }
            file_support.real_write_json_file(self.get_virtual_queue_file_path(), json_data)
            self.buffer = 0
        else:
            self.buffer += 1

queue_instance = QueueManager()
