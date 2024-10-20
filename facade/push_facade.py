
from support.queue_support import queue_instance
from support.queue_support import QueueItem
from support.queue_support import Action, Status
from support import file_support

def get_only_in_local(local_index_json, cloud_index_json):
    only_in_local = {key: value for key, value in local_index_json.items() if key not in cloud_index_json}
    return only_in_local

def get_only_in_remote(local_index_json, cloud_index_json):
    only_in_remote = {key: value for key, value in cloud_index_json.items() if key not in local_index_json}
    return only_in_remote

def get_local_remote_diff(local_index_json, cloud_index_json):
    diff = {}
    # for key, local_value in local_index_json.items():
    #     if key in cloud_index_json:
    #         cloud_value = cloud_index_json[key]
    #         if local_value['size'] != cloud_value['size']:
    #             diff[key] = {
    #                 'local': local_value,
    #                 'remote': cloud_value
    #             }
    return diff

def handle_index_json(index_json, action):
    for key in index_json:
        value = index_json[key]
        item_status = Status.PENDING
        item_action = action
        virtual_middle_path = value['middle_path']
        item_remote_path_hash = file_support.get_string_hash(virtual_middle_path)
        queue_item = QueueItem(virtual_middle_path, item_action, item_status)
        queue_instance.add_queue_item(item_remote_path_hash, queue_item)

