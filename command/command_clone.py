
from command import command_pull
from command import command_init

def command_clone(mode, password, local_path, remote_path, app_id, secret_key, app_key, sign_code, expires_in, refresh_token, access_token):
    command_init.command_init(mode, password, local_path, remote_path, app_id, secret_key, app_key, sign_code, expires_in, refresh_token, access_token)
    command_pull.command_pull()
    
