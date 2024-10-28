
from support import file_support
from support.constant_support import constant_instance
from support.config_support import config_instance
from support import time_support

from facade import index_facade
from facade import queue_facade

from support.queue_support import Action, queue_instance

from facade import encrypted_facade

action_name = "encrypted"

def command_encrypted(all_flag):

    current_action_folder_name = time_support.get_action_folder_name(action_name)
    current_action_folder_virtual_path = file_support.virtual_merge_path(constant_instance.get_virtual_action_folder_path(), current_action_folder_name)
    file_support.real_create_local_folder(current_action_folder_virtual_path)

    current_action_index_virtual_path = file_support.virtual_merge_path(current_action_folder_virtual_path, "index")
    file_support.real_create_local_folder(current_action_index_virtual_path)

    current_action_log_virtual_path = file_support.virtual_merge_path(current_action_folder_virtual_path, "log")
    file_support.real_create_local_folder(current_action_log_virtual_path)

    target_index_json = {}
    if all_flag == None or all_flag == False:
        remote_index_json_virtual_path = file_support.virtual_merge_path(current_action_index_virtual_path, "target.json")
        target_index_json = index_facade.get_cloud_index(config_instance.get_virtual_remote_path())

    file_support.real_write_json_file(remote_index_json_virtual_path, target_index_json)
    local_index_json_virtual_path = file_support.virtual_merge_path(current_action_index_virtual_path, "source.json")
    local_index_json = index_facade.get_local_index(config_instance.get_virtual_local_path())

    file_support.real_write_json_file(local_index_json_virtual_path, local_index_json)
    only_in_local_json = index_facade.get_only_in_local(local_index_json, target_index_json)

    encrypted_facade.handle_index_json(only_in_local_json, Action.ONLY_ENCRYPTED)

    queue_instance.set_virtual_action_folder(current_action_folder_virtual_path)
    queue_instance.write_queue()
    queue_facade.trigger()
