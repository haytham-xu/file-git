

from hook.hook import Hooks

from support.config_support import Mode
from support import file_support
from support.constant_support import constant_instance
from support.config_support import config_instance
from support.queue_support import queue_instance

def command_init(mode, password, virtual_local_path, virtual_remote_path, app_id, secret_key, app_key, sign_code, expires_in, refresh_token, access_token):

    Hooks.init_constant()

    # create folder trash
    # create folder action
    file_support.real_create_local_folder(constant_instance.get_virtual_file_git_folder_path())
    file_support.real_create_local_folder(constant_instance.get_virtual_trash_folder_path())
    file_support.real_create_local_folder(constant_instance.get_virtual_action_folder_path())
    file_support.real_create_local_folder(constant_instance.get_virtual_buffer_folder_path())

    # create file config_instance.json
    # create file queue.json
    file_support.real_create_local_file(constant_instance.get_virtual_queue_file_path())
    file_support.real_create_local_file(constant_instance.get_virtual_config_file_path())

    config_instance.set_mode(Mode.from_string(mode))
    config_instance.set_password(password)
    config_instance.set_virtual_local_path(virtual_local_path)
    config_instance.set_virtual_remote_path(virtual_remote_path)
    config_instance.set_app_id(app_id)
    config_instance.set_secret_key(secret_key)
    config_instance.set_app_key(app_key)
    config_instance.set_sign_code(sign_code)
    config_instance.set_expires_in(expires_in)
    config_instance.set_refresh_token(refresh_token)
    config_instance.set_access_token(access_token)
    config_instance.write_config(constant_instance.get_virtual_config_file_path())

    Hooks.init_queue_file_path()
    queue_instance.write_queue()
    Hooks.init_queue_instance()
