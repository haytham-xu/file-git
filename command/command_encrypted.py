
from facade.queue_facade import queue_instance
from support import file_support

from model.config import FilegitConfig
from support import fgit_support

from facade import index_facade
from facade import queue_facade

from model.queue import Action

from facade import encrypted_facade

action_name = "encrypted"

def command_encrypted(all_flag):

    current_action_folder_name = fgit_support.get_action_folder_name(action_name)
    current_action_folder_vpath = file_support.merge_vpath(constant_support.ACTION_FOLDER_VPATH, current_action_folder_name)
    file_support.create_local_folder(current_action_folder_vpath)

    current_action_index_vpath = file_support.merge_vpath(current_action_folder_vpath, "index")
    file_support.create_local_folder(current_action_index_vpath)

    current_action_log_vpath = file_support.merge_vpath(current_action_folder_vpath, "log")
    file_support.create_local_folder(current_action_log_vpath)

    target_index_json = {}
    if all_flag == None or all_flag == False:
        remote_index_json_vpath = file_support.merge_vpath(current_action_index_vpath, "target.json")
        target_index_json = index_facade.get_cloud_index(FilegitConfig.get_remote_vpath())

    file_support.real_write_json_file(remote_index_json_vpath, target_index_json)
    local_index_json_vpath = file_support.merge_vpath(current_action_index_vpath, "source.json")
    local_index_json = index_facade.get_local_index(FilegitConfig.get_local_vpath())

    file_support.real_write_json_file(local_index_json_vpath, local_index_json)
    only_in_local_json = index_facade.get_only_in_local(local_index_json, target_index_json)

    encrypted_facade.handle_index_json(only_in_local_json, Action.ONLY_ENCRYPTED)

    queue_instance.set_virtual_action_folder(current_action_folder_vpath)
    queue_instance.write_queue()
    queue_facade.trigger()
