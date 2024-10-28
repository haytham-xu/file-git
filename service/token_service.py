
import os

from support.bdwp_support import bdwp_instance

from support.config_support import config_instance
from support.constant_support import constant_instance

def refresh_token():
    refresh_token = config_instance.get_refresh_token()
    app_key = config_instance.get_app_key()
    secret_key = config_instance.get_secret_key()
    res = bdwp_instance.refresh_token(refresh_token, app_key, secret_key)
    
    access_token = res['access_token']
    refresh_token = res['refresh_token']
    expire_in = res['expires_in']
    
    print(res)

    config_instance.set_access_token(access_token)
    config_instance.set_refresh_token(refresh_token)
    config_instance.set_expires_in(expire_in)
    config_instance.write_config(constant_instance.get_virtual_config_file_path())
