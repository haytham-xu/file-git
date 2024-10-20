
import json

from support import file_support
from support.constant_support import constant_instance

def command_set_config(key, value):
    real_current_config = file_support.real_read_json_file(constant_instance.get_virtual_config_file_path())
    # verify key is valid
    if key not in real_current_config:
        raise Exception(f"Key {key} not found in the configuration.")
    # for enum key, verify value is valid
    if key == "mode" and value not in ["ORIGINAL", "ENCRYPT"]:
        raise Exception(f"Value {value} is invalid for key {key}.")
    real_current_config[key] = value
    
    file_support.real_write_json_file(constant_instance.get_virtual_config_file_path(), real_current_config)
