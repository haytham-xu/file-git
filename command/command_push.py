
from facade.queue_facade import queue_instance
from facade import index_facade

from model.queue import Action
from model.file_git import fgit_instance
from model.queue import QueueItem
from model.config import config_instance
from model.logger import logger_instance

from support import file_support

action_name = "push"

def command_push(offline=True):
    logger_instance.log_debug("command_push is executing...", "offline mode", offline)
    queue_instance.acquire_lock()
    local_vpath = file_support.get_current_vpath()
    fgit_instance.init_action(action_name)

    local_index_json = index_facade.get_local_index(config_instance.get_local_vpath())
    file_support.real_write_json_file(fgit_instance.get_local_index_file_vpath(local_vpath), local_index_json)

    if offline:
        cloud_index_json = file_support.real_read_json_file(fgit_instance.get_cloud_index_file_vpath(local_vpath))
    else:
        cloud_index_json = index_facade.get_cloud_index(config_instance.get_remote_vpath())
        file_support.real_write_json_file(fgit_instance.get_cloud_index_file_vpath(local_vpath), cloud_index_json)

    only_in_local_json = index_facade.get_only_in_local(local_index_json, cloud_index_json)
    # todo: if encrypted mode, then the middle path in cloud_json is enctypted path not the source one. should decode. !!!!
    only_in_cloud_json = index_facade.get_only_in_remote(local_index_json, cloud_index_json)
    local_cloud_diff_json = index_facade.get_local_remote_diff(local_index_json, cloud_index_json)

    for key in only_in_local_json:
        middle_vpath = only_in_local_json[key][QueueItem.KEY_MIDDLE_PATH]
        queue_instance.push(middle_vpath, Action.UPLOAD)

    for key in only_in_cloud_json:
        middle_vpath = only_in_cloud_json[key][QueueItem.KEY_MIDDLE_PATH]
        queue_instance.push(middle_vpath, Action.REMOTE_DELETE)

    for key in local_cloud_diff_json:
        middle_vpath = local_cloud_diff_json[key][QueueItem.KEY_MIDDLE_PATH]
        queue_instance.push(middle_vpath, Action.UPLOAD)

    queue_instance.trigger()
