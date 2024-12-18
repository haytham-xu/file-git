
from support import file_support
from support.constant_support import constant_instance
from support.config_support import config_instance
from support import time_support

from facade import index_facade
from facade import push_facade
from facade import queue_facade

from support.queue_support import Action, queue_instance

action_name = "push"

def command_push():

    current_action_folder_name = time_support.get_action_folder_name(action_name)
    current_action_folder_virtual_path = file_support.virtual_merge_path(constant_instance.get_virtual_action_folder_path(), current_action_folder_name)
    file_support.real_create_local_folder(current_action_folder_virtual_path)

    current_action_index_virtual_path = file_support.virtual_merge_path(current_action_folder_virtual_path, "index")
    file_support.real_create_local_folder(current_action_index_virtual_path)

    current_action_log_virtual_path = file_support.virtual_merge_path(current_action_folder_virtual_path, "log")
    file_support.real_create_local_folder(current_action_log_virtual_path)

    local_index_json_virtual_path = file_support.virtual_merge_path(current_action_index_virtual_path, "local.json")
    local_index_json = index_facade.get_local_index(config_instance.get_virtual_local_path())
    file_support.real_write_json_file(local_index_json_virtual_path, local_index_json)

    remote_index_json_virtual_path = file_support.virtual_merge_path(current_action_index_virtual_path, "remote.json")
    cloud_index_json = index_facade.get_cloud_index(config_instance.get_virtual_remote_path())
    file_support.real_write_json_file(remote_index_json_virtual_path, cloud_index_json)

    only_in_local_json = index_facade.get_only_in_local(local_index_json, cloud_index_json)
    only_in_cloud_json = index_facade.get_only_in_remote(local_index_json, cloud_index_json)
    local_cloud_diff_json = index_facade.get_local_remote_diff(local_index_json, cloud_index_json)
    push_facade.handle_index_json(only_in_local_json, Action.UPLOAD)
    push_facade.handle_index_json(only_in_cloud_json, Action.REMOTE_DELETE)
    push_facade.handle_index_json(local_cloud_diff_json, Action.UPLOAD)

    queue_instance.set_virtual_action_folder(current_action_folder_virtual_path)
    queue_instance.write_queue()
    queue_facade.trigger()
