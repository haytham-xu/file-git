
import json
from enum import Enum

class Action(Enum):
    DOWNLOAD = "DOWNLOAD"
    UPLOAD = "UPLOAD"
    LOCAL_DELETE = "LOCAL_DELETE"
    REMOTE_DELETE = "REMOTE_DELETE"
    ONLY_ENCRYPTED = "ONLY_ENCRYPTED"

class QueueItem:
    KEY_MIDDLE_PATH = 'middle_path'
    KEY_ACTION = 'action'

    def __init__(self, middle_path:str="", action:Action=None):
        self.middle_path = middle_path
        self.action = action

    def get_middle_vpath(self):
        return self.middle_path
    def set_middle_vpath(self, middle_path):
        self.middle_path = middle_path
    def get_action(self):
        return self.action
    def set_action(self, action):
        self.action = action

    @staticmethod
    def from_json(item):
        return QueueItem(
            middle_path=item[QueueItem.KEY_MIDDLE_PATH],
            action=Action(item[QueueItem.KEY_ACTION])
        )
    
    @staticmethod
    def from_string(item):
        item_dict = json.loads(item)
        return QueueItem(
            middle_path=item_dict[QueueItem.KEY_MIDDLE_PATH],
            action=Action(item_dict[QueueItem.KEY_ACTION])
        )

    def to_json(self):
        return json.dumps({
            QueueItem.KEY_MIDDLE_PATH: self.middle_path,
            QueueItem.KEY_ACTION: self.action.value
        })
