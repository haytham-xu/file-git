
import json
from enum import Enum
from typing import List, Dict

from support import file_support

class Status(Enum):
    PENDING = 1
    IN_PROGRESS = 2
    COMPLETED = 3
    FAILED = 4

class Action(Enum):
    DOWNLOAD = 1
    UPLOAD = 2
    LOCAL_DELETE = 3
    REMOTE_DELETE = 4

class QueueItem:
    def __init__(self, middle_path:str="", action:Action=None, status:Status=Status.PENDING):
        self.middle_path = middle_path
        self.action = action
        self.status = status

    def get_middle_path(self):
        return self.middle_path
    def set_middle_path(self, middle_path):
        self.middle_path = middle_path
    def get_action(self):
        return self.action
    def set_action(self, action):
        self.action = action
    def get_status(self):
        return self.status
    def set_status(self, status):
        self.status = status

    def from_json():
        pass

    def to_json(self):
        return json.dumps({
            'middle_path': self.remote_middle_path,
            'action': self.action.value,
            'status': self.status.value
        })

class QueueManager:
    def __init__(self):
        self.lock = False
        self.key_set: List[str] = []
        self.queue_item: Dict[QueueItem] = {}
        self.action_folder = ""

    def is_lock(self):
        return self.lock
    def acquire_lock(self):
        if self.lock != True:
            self.lock = True
    def release_lock(self):
        if self.lock != False:
            self.lock = False
    def is_queue_empty(self): 
        return len(self.queue_item) == 0
    
    def set_action_folder(self, action_folder):
        self.action_folder = action_folder
    def get_action_folder(self):
        return self.action_folder
    
    def get_a_queue_item(self):
        a_key = self.key_set[-1]
        a_queue_item = self.queue_item[a_key]
        a_queue_item.status = Status.IN_PROGRESS
        return a_key, a_queue_item
    
    def add_queue_item(self, key:str, queue_item: QueueItem):
        self.key_set.append(key)
        self.queue_item[key] = queue_item

    def removed_queue_item(self, key):
        self.key_set.remove(key)
        self.queue_item.pop(key)

    def update_queue_item(self, a_key, status):
        a_queue_item:QueueItem = self.queue_item[a_key]
        a_queue_item.set_status(status)

    def read_queue(self, queue_file_path):
        if not file_support.is_exist(queue_file_path):
            raise FileNotFoundError(f"queue_instance file '{queue_file_path}' does not exist.")
        with open(queue_file_path, 'r') as file:
            data = json.load(file)
            self.lock = data['lock']
            self.key_set = data['key_set']
            self.action_folder = data['action_folder']
            self.queue_item = {key: QueueItem.from_json(item) for key, item in data['queue_item'].items()}

    def write_queue(self, queue_file_path):
        with open(queue_file_path, 'w') as file:
            json.dump({
                'lock': self.lock,
                'action_folder': self.action_folder,
                'key_set': self.key_set,
                'queue_item': {key: json.loads(item.to_json()) for key, item in self.queue_item.items()}
            }, file, indent=4)

queue_instance = QueueManager()
