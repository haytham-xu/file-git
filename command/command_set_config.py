
import json

from support import file_support
from support.constant_support import constant_instance

def command_set_config(key, value):
    current_config = file_support.read_json_file(constant_instance.get_config_file_path())
    # verify key is valid
    if key not in current_config:
        raise Exception(f"Key {key} not found in the configuration.")
    # for enum key, verify value is valid
    if key == "mode" and value not in ["ORIGINAL", "ENCRYPT"]:
        raise Exception(f"Value {value} is invalid for key {key}.")
    current_config[key] = value

    with open(constant_instance.get_config_file_path(), 'w') as config_file:
        json.dump(current_config, config_file, indent=4)
