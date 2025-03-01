
import json

from support import file_support

def command_set_config(key, value):
    real_current_config = file_support.real_read_json_file(constant_support.CONFIG_FILE_VPATH)
    # verify key is valid
    if key not in real_current_config:
        raise Exception(f"Key {key} not found in the configuration.")
    # for enum key, verify value is valid
    if key == "mode" and value not in ["ORIGINAL", "ENCRYPT"]:
        raise Exception(f"Value {value} is invalid for key {key}.")
    real_current_config[key] = value
    
    file_support.real_write_json_file(constant_support.CONFIG_FILE_VPATH, real_current_config)
