

from support.config_support import config_instance, Mode
from support.constant_support import constant_instance

from support import file_support
from support import encrypt_support

def move_to_local(source_file_virtual_path_in_buffer):
    file_buffer_middle_virtual_path = source_file_virtual_path_in_buffer.removeprefix(constant_instance.get_virtual_buffer_folder_path())
    if config_instance.get_mode() == Mode.ENCRYPTED:
        decode_middle_virtual_path = encrypt_support.decode_path(file_buffer_middle_virtual_path)
        file_local_virtual_path = file_support.virtual_merge_path(config_instance.get_virtual_local_path(), decode_middle_virtual_path)
        encrypt_support.decrypt_file(source_file_virtual_path_in_buffer, file_local_virtual_path, config_instance.get_password())
    else:
        
        file_local_virtual_path = file_support.virtual_merge_path(config_instance.get_virtual_local_path(), file_buffer_middle_virtual_path)
        file_support.real_move_file_folder(source_file_virtual_path_in_buffer, file_local_virtual_path)

def post_move_to_local(source_file_virtual_path_in_buffer):
    file_support.real_delete_local_path(source_file_virtual_path_in_buffer)

def move_to_buffer(file_virtual_path_in_local):
    file_virtual_local_middle_path = file_virtual_path_in_local.removeprefix(config_instance.get_virtual_local_path())
    if config_instance.get_mode() == Mode.ENCRYPTED:
        encode_middle_virtual_path = encrypt_support.encode_path(file_virtual_local_middle_path)
        encode_file_virtual_path = file_support.virtual_merge_path(constant_instance.get_virtual_buffer_folder_path(), encode_middle_virtual_path)
        if file_support.real_is_local_exist(encode_file_virtual_path):
            print("encryptes file exist, skip: ", encode_file_virtual_path)
            return
        encrypt_support.encrypt_file(file_virtual_path_in_local, encode_file_virtual_path, config_instance.get_password())
    else:
        file_buffer_virtual_path = file_support.virtual_merge_path(constant_instance.get_virtual_buffer_folder_path(), file_virtual_local_middle_path)
        file_support.real_copy_file_folder(file_virtual_path_in_local, file_buffer_virtual_path)

def post_move_to_buffer(file_virtual_path_in_buffer):
    file_support.real_delete_local_path(file_virtual_path_in_buffer)

def get_file_buffer_path(file_root_path, file_middle_path):
    if config_instance.get_mode() == Mode.ENCRYPTED:
        return file_support.virtual_merge_path(file_root_path, encrypt_support.encode_path(file_middle_path))
    return file_support.virtual_merge_path(file_root_path, file_middle_path)

def get_file_cloud_path_for_local_use(file_root_path, file_middle_path):
    return file_support.virtual_merge_path(file_root_path, file_middle_path)

def get_file_cloud_path_for_cloud_use(file_root_path, file_middle_path):
    if config_instance.get_mode() == Mode.ENCRYPTED:
        return file_support.virtual_merge_path(file_root_path, encrypt_support.encode_path(file_middle_path))
    return file_support.virtual_merge_path(file_root_path, file_middle_path)

def get_file_cloud_path(file_root_path, file_middle_path):
    return file_support.virtual_merge_path(file_root_path, file_middle_path)

def get_unencrypted_path(a_path): # a_path coule be a middle_path or a absolute path
    if config_instance.get_mode() == Mode.ENCRYPTED:
        return encrypt_support.decode_path(a_path)
    return a_path
