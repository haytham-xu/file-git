
import os
import base64

from support.config_support import config_instance
from support.constant_support import constant_instance

from support import file_support
from support import encrypt_support

def move_to_local(file_buffer_path):
    file_buffer_middle_path = file_buffer_path.removeprefix(constant_instance.get_buffer_folder_path())
    decode_middle_path = file_buffer_middle_path
    file_local_path = file_support.merge_path(config_instance.get_local_path(), decode_middle_path)
    if config_instance.get_mode() == 'ENCRYPTED':
        decode_middle_path = decode_path(file_buffer_middle_path)
        decode_file_path = file_support.merge_path(constant_instance.get_buffer_folder_path(), decode_middle_path)
        file_local_path = file_support.merge_path(config_instance.get_local_path(), decode_middle_path)
        encrypt_support.decrypt_file(file_buffer_path, decode_file_path, config_instance.get_password())
        file_support.delete_path(decode_file_path)
    file_support.move_file_folder(file_buffer_path, file_local_path)

def post_move_to_local(file_buffer_path):
    if config_instance.get_mode() == 'ENCRYPTED':
        file_buffer_middle_path = file_buffer_path.removeprefix(constant_instance.get_buffer_folder_path())
        decode_middle_path = decode_path(file_buffer_middle_path)
        decode_file_path = file_support.merge_path(constant_instance.get_buffer_folder_path(), decode_middle_path)
        file_support.delete_path(decode_file_path)

def move_to_buffer(file_path_in_local):
    file_local_middle_path = file_path_in_local.removeprefix(config_instance.get_local_path())
    if config_instance.get_mode() == 'ENCRYPTED':
        encode_middle_path = encode_path(file_local_middle_path)
        encode_file_path = file_support.merge_path(constant_instance.get_buffer_folder_path(), encode_middle_path)
        encrypt_support.encrypt_file(file_path_in_local, encode_file_path, config_instance.get_password())
    else:
        file_buffer_path = file_support.merge_path(constant_instance.get_buffer_folder_path(), file_local_middle_path)
        file_support.copy_file_folder(file_path_in_local, file_buffer_path)

def post_move_to_buffer(file_path_in_local):
    file_local_middle_path = file_path_in_local.removeprefix(config_instance.get_local_path())
    if config_instance.get_mode() == 'ENCRYPTED':
        encode_middle_path = encode_path(file_local_middle_path)
        encode_file_path = file_support.merge_path(constant_instance.get_buffer_folder_path(), encode_middle_path)
        file_support.delete_path(encode_file_path)
    else:
        file_buffer_path = file_support.merge_path(constant_instance.get_buffer_folder_path(), file_local_middle_path)
        file_support.delete_path(file_buffer_path)

def get_file_buffer_path(file_root_path, file_middle_path):
    if config_instance.get_mode() == 'ENCRYPTED':
        return file_support.merge_path(file_root_path, encode_path(file_middle_path))
    return file_support.merge_path(file_root_path, file_middle_path)


def get_file_cloud_path(file_root_path, file_middle_path):
    if config_instance.get_mode() == 'ENCRYPTED':
        return file_support.merge_path(file_root_path, encode_path(file_middle_path))
    return file_support.merge_path(file_root_path, file_middle_path)

def encode_path(source_path):
    path_segments = source_path.split(os.sep)
    encoded_segments = [base64.urlsafe_b64encode(segment.encode()).decode() for segment in path_segments]
    return os.sep.join(encoded_segments)

def decode_path(encoded_path):
    encoded_segments = encoded_path.split(os.sep)
    decoded_segments = [base64.urlsafe_b64decode(segment.encode()).decode() for segment in encoded_segments]
    return os.sep.join(decoded_segments)
