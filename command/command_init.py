
from support.config_support import Mode

from support import file_support
from support.constant_support import constant_instance
from support.config_support import config_instance

def command_init(mode, password, local_path, remote_path, app_id, secret_key, app_key, sign_code, expires_in, refresh_token, access_token):
    # create folder trash
    # create folder action
    file_support.create_folder(constant_instance.get_file_git_folder_path())
    file_support.create_folder(constant_instance.get_trash_folder_path())
    file_support.create_folder(constant_instance.get_action_folder_path())

    # create file config_instance.json
    # create file queue.json
    file_support.create_file(constant_instance.get_queue_file_path())
    file_support.create_file(constant_instance.get_config_file_path())

    config_instance.set_mode(Mode.from_string(mode))
    config_instance.set_password(password)
    config_instance.set_local_path(local_path)
    config_instance.set_remote_path(remote_path)
    config_instance.set_app_id(app_id)
    config_instance.set_secret_key(secret_key)
    config_instance.set_app_key(app_key)
    config_instance.set_sign_code(sign_code)
    config_instance.set_expires_in(expires_in)
    config_instance.set_refresh_token(refresh_token)
    config_instance.set_access_token(access_token)
    config_instance.write_config(constant_instance.get_config_file_path())
