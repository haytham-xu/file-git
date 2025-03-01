
import os

from support.bdwp_support import bdwp_instance

from model.config import FilegitConfig

def refresh_token():
    refresh_token = FilegitConfig.get_refresh_token()
    app_key = FilegitConfig.get_app_key()
    secret_key = FilegitConfig.get_secret_key()
    res = bdwp_instance.refresh_token(refresh_token, app_key, secret_key)
    
    access_token = res['access_token']
    refresh_token = res['refresh_token']
    expire_in = res['expires_in']
    
    print(res)

    FilegitConfig.set_access_token(access_token)
    FilegitConfig.set_refresh_token(refresh_token)
    FilegitConfig.set_expires_in(expire_in)
    FilegitConfig.write_config(constant_support.CONFIG_FILE_VPATH)
