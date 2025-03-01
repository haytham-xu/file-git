

from model.config import Mode
from support import file_support
from model.config import config_instance
from model.file_git import fgit_instance
from model.logger import logger_instance

def command_init(mode='ORIGINAL', password='', local_vpath='', remote_vpath='', app_id='', secret_key='', app_key='', sign_code='', expires_in='', refresh_token='', access_token=''):
    # create folder trash
    # create folder action
    logger_instance.log_debug("command_init is running")
    local_vpath=file_support.get_current_vpath()
    logger_instance.log_debug("current local_vpath is", local_vpath)
    logger_instance.log_debug("fgit, trash, action, buffer folder creating...")
    file_support.create_local_folder(fgit_instance.get_fgit_folder_vpath(local_vpath))
    logger_instance.log_debug("folder create successfully", fgit_instance.get_fgit_folder_vpath(local_vpath))
    file_support.create_local_folder(fgit_instance.get_trash_folder_vpath(local_vpath))
    logger_instance.log_debug("folder create successfully", fgit_instance.get_trash_folder_vpath(local_vpath))
    file_support.create_local_folder(fgit_instance.get_action_folder_vpath(local_vpath))
    logger_instance.log_debug("folder create successfully", fgit_instance.get_action_folder_vpath(local_vpath))
    file_support.create_local_folder(fgit_instance.get_buffer_folder_vpath(local_vpath))
    logger_instance.log_debug("folder create successfully", fgit_instance.get_buffer_folder_vpath(local_vpath))

    # create file config_instance.json
    # create file queue.json
    logger_instance.log_debug("config file, local index file, cloud index file creating...")
    file_support.real_create_local_file(fgit_instance.get_config_file_vpath(local_vpath))
    logger_instance.log_debug("file create successfully", fgit_instance.get_config_file_vpath(local_vpath))
    file_support.real_create_local_file(fgit_instance.get_local_index_file_vpath(local_vpath))
    logger_instance.log_debug("file create successfully", fgit_instance.get_local_index_file_vpath(local_vpath))
    file_support.real_create_local_file(fgit_instance.get_cloud_index_file_vpath(local_vpath))
    logger_instance.log_debug("file create successfully", fgit_instance.get_cloud_index_file_vpath(local_vpath))

    logger_instance.log_debug("config_instance init...")
    config_instance.set_mode(Mode.from_string(mode))
    config_instance.set_password(password)
    config_instance.set_local_vpath(local_vpath)
    config_instance.set_remote_vpath(remote_vpath)
    config_instance.set_app_id(app_id)
    config_instance.set_secret_key(secret_key)
    config_instance.set_app_key(app_key)
    config_instance.set_sign_code(sign_code)
    config_instance.set_expires_in(expires_in)
    config_instance.set_refresh_token(refresh_token)
    config_instance.set_access_token(access_token)
    config_instance.write_config(fgit_instance.get_config_file_vpath(local_vpath))

    logger_instance.log_debug("command_init end")
