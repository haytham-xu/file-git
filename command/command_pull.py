
from support import file_support
from support.constant_support import constant_instance
from support import time_support

from facade import index_facade
from facade import pull_facade
from facade import queue_facade

from support.queue_support import Action, queue_instance

action_name = "pull"

def command_pull():

    current_action_folder_name = time_support.get_action_folder_name(action_name)
    current_action_folder_path = file_support.merge_path(constant_instance.get_action_folder_path(), current_action_folder_name)
    file_support.create_folder(current_action_folder_path)

    current_action_index_path = file_support.merge_path(current_action_folder_path, "index")
    file_support.create_folder(current_action_index_path)

    current_action_log_path = file_support.merge_path(current_action_folder_path, "log")
    file_support.create_folder(current_action_log_path)

    local_index_json_path = file_support.merge_path(current_action_folder_path, "local.json")
    local_index_json = index_facade.get_local_index(local_index_json_path)
    file_support.write_json_file(local_index_json_path, local_index_json)

    remote_index_json_path = file_support.merge_path(current_action_folder_path, "remote.json")
    cloud_index_json = index_facade.get_cloud_index(remote_index_json_path)
    file_support.write_json_file(remote_index_json_path, cloud_index_json)

    only_in_local_json = pull_facade.get_only_in_local(local_index_json, cloud_index_json)
    only_in_cloud_json = pull_facade.get_only_in_remote(local_index_json, cloud_index_json)
    local_cloud_diff_json = pull_facade.get_local_remote_diff(local_index_json, cloud_index_json)
    pull_facade.handle_index_json(only_in_local_json, Action.LOCAL_DELETE)
    pull_facade.handle_index_json(only_in_cloud_json, Action.DOWNLOAD)
    pull_facade.handle_index_json(local_cloud_diff_json, Action.DOWNLOAD)

    queue_instance.set_action_folder(current_action_folder_path)
    queue_instance.write_queue()
    queue_facade.trigger()

