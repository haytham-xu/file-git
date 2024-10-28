

from support.queue_support import queue_instance
from support.queue_support import QueueItem
from support.queue_support import Action, Status
from support import file_support

def handle_index_json(index_json, action):
    for key in index_json:
        value = index_json[key]
        item_status = Status.PENDING
        item_action = action
        virtual_middle_path = value['middle_path']
        item_remote_path_hash = file_support.get_string_hash(virtual_middle_path)
        queue_item = QueueItem(virtual_middle_path, item_action, item_status)
        queue_instance.add_queue_item(item_remote_path_hash, queue_item)
