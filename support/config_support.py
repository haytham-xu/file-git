
from enum import Enum

from support import file_support

class Mode(Enum):
    ORIGINAL = 'ORIGINAL'
    ENCRYPTED = 'ENCRYPTED'

    @classmethod
    def from_string(cls, string_value):
        try:
            return cls(string_value)
        except ValueError:
            raise ValueError(f"'{string_value}' is not a valid {cls.__name__}")

class config_instance():
    # mode, password, local_path, remote_path, app_id, secret_key, app_key, sign_code, expires_in, refresh_token, access_token
    def __init__(self, mode=None, password=None, local_path=None, remote_path=None, app_id=None,
                secret_key=None, app_key=None, sign_code=None, expires_in=None, refresh_token=None, access_token=None):
        self.mode = mode
        self.password = password
        self.virtual_local_path = local_path
        self.virtual_remote_path = remote_path
        self.app_id = app_id
        self.secret_key = secret_key
        self.app_key = app_key
        self.sign_code = sign_code
        self.expires_in = expires_in
        self.refresh_token = refresh_token
        self.access_token = access_token

    def read_config(self, config_file_virtual_path):
        if not file_support.real_is_local_exist(config_file_virtual_path):
            raise FileNotFoundError(f"config_instance file '{config_file_virtual_path}' does not exist.")
        config_data = file_support.real_read_json_file(config_file_virtual_path)
        self.mode = Mode.from_string(config_data.get('mode', self.mode))
        self.password = config_data.get('password', self.password)
        self.virtual_local_path = config_data.get('local_path', self.virtual_local_path)
        self.virtual_remote_path = config_data.get('remote_path', self.virtual_remote_path)
        self.app_id = config_data.get('app_id', self.app_id)
        self.secret_key = config_data.get('secret_key', self.secret_key)
        self.app_key = config_data.get('app_key', self.app_key)
        self.sign_code = config_data.get('sign_code', self.sign_code)
        self.expires_in = config_data.get('expires_in', self.expires_in)
        self.refresh_token = config_data.get('refresh_token', self.refresh_token)
        self.access_token = config_data.get('access_token', self.access_token)

    def write_config(self, config_file_virtual_path):
        config_data = {
            'mode': self.mode.value,
            'password': self.password,
            'local_path': self.virtual_local_path,
            'remote_path': self.virtual_remote_path,
            'app_id': self.app_id,
            'secret_key': self.secret_key,
            'app_key': self.app_key,
            'sign_code': self.sign_code,
            'expires_in': self.expires_in,
            'refresh_token': self.refresh_token,
            'access_token': self.access_token
        }
        file_support.real_write_json_file(config_file_virtual_path, config_data)
    
    def get_mode(self):
        return self.mode
    def set_mode(self, mode):
        self.mode = mode

    def get_password(self):
        return self.password
    def set_password(self, password):
        self.password = password

    def get_virtual_local_path(self):
        return self.virtual_local_path
    def set_virtual_local_path(self, local_path):
        self.virtual_local_path = local_path

    def get_virtual_remote_path(self):
        return self.virtual_remote_path
    def set_virtual_remote_path(self, remote_path):
        self.virtual_remote_path = remote_path

    def get_app_id(self):
        return self.app_id
    def set_app_id(self, app_id):
        self.app_id = app_id

    def get_secret_key(self):
        return self.secret_key
    def set_secret_key(self, secret_key):
        self.secret_key = secret_key

    def get_app_key(self):
        return self.app_key
    def set_app_key(self, app_key):
        self.app_key = app_key

    def get_sign_code(self):
        return self.sign_code
    def set_sign_code(self, sign_code):
        self.sign_code = sign_code

    def get_expires_in(self):
        return self.expires_in
    def set_expires_in(self, expires_in):
        self.expires_in = expires_in

    def get_refresh_token(self):
        return self.refresh_token
    def set_refresh_token(self, refresh_token):
        self.refresh_token = refresh_token

    def get_access_token(self):
        return self.access_token
    def set_access_token(self, access_token):
        self.access_token = access_token

config_instance = config_instance()
