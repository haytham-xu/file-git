
import os

from support.bdwp_support import bdwp_instance

from support.config_support import config_instance
from support.constant_support import constant_instance

def refresh_token():
    refresh_token = config_instance.get_refresh_token()
    app_key = config_instance.get_app_key()
    secret_key = config_instance.get_secret_key()
    res = bdwp_instance.refresh_token(refresh_token, app_key, secret_key)
    print("==> ", res)
    access_token = res['access_token']
    refresh_token = res['refresh_token']
    expire_in = res['expires_in']

    config_instance.set_access_token(access_token)
    config_instance.set_refresh_token(refresh_token)
    config_instance.set_expire_in(expire_in)
    config_instance.write_config(constant_instance.get_config_file_path())

    env_file_path = os.path.expanduser("~/.zshrc")
    
    if os.path.exists(env_file_path):
        with open(env_file_path, 'r') as env_file:
            lines = env_file.readlines()
    else:
        lines = []
    
    env_vars = {
        'BDWP_EXPIRES_IN': expire_in,
        'DWP_REFRESH_TOKEN': refresh_token,
        'BDWP_ACCESS_TOKEN': access_token
    }
    
    updated_lines = []
    for line in lines:
        for key in env_vars:
            if line.startswith(f'export {key}='):
                line = f'export {key}="{env_vars[key]}"\n'
        updated_lines.append(line)
    
    for key, value in env_vars.items():
        if not any(line.startswith(f'export {key}=') for line in updated_lines):
            updated_lines.append(f'export {key}="{value}"\n')
    
    with open(env_file_path, 'w') as env_file:
        env_file.writelines(updated_lines)
    
    print(f"please run this commend in your terminal:\nsource {env_file_path}")

