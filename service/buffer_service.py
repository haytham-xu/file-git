

from model.config import config_instance, Mode

from model.file_git import fgit_instance

from support import file_support
from support import encrypt_support

def move_to_local(source_file_vpath_in_buffer:str):
    local_vpath = file_support.get_current_vpath()

    file_buffer_middle_vpath = source_file_vpath_in_buffer.removeprefix(fgit_instance.get_buffer_folder_vpath(local_vpath))
    if config_instance.get_mode() == Mode.ENCRYPTED:
        decode_middle_vpath = encrypt_support.decode_path(file_buffer_middle_vpath)
        file_local_vpath = file_support.merge_vpath(config_instance.get_local_vpath(), decode_middle_vpath)
        encrypt_support.decrypt_file(source_file_vpath_in_buffer, file_local_vpath, config_instance.get_password())
    else:
        file_local_vpath = file_support.merge_vpath(config_instance.get_local_vpath(), file_buffer_middle_vpath)
        file_support.real_move_file_folder(source_file_vpath_in_buffer, file_local_vpath)

def post_move_to_local(source_file_vpath_in_buffer):
    file_support.real_delete_local_path(source_file_vpath_in_buffer)
    file_support.local_delete_empty_parent_folders(source_file_vpath_in_buffer)

def move_to_buffer(file_local_vpath:str, local_root_vpath, buffer_root_vpath, mode:Mode=Mode.ORIGINAL, encrtpted_password=None):
    file_virtual_local_middle_path = file_local_vpath.removeprefix(local_root_vpath)
    if mode == Mode.ENCRYPTED:
        encode_middle_vpath = encrypt_support.encode_path(file_virtual_local_middle_path)
        encode_file_vpath = file_support.merge_vpath(buffer_root_vpath, encode_middle_vpath)
        if file_support.is_local_exist(encode_file_vpath):
            print("encryptes file exist, skip: ", encode_file_vpath)
            return
        encrypt_support.encrypt_file(file_local_vpath, encode_file_vpath, encrtpted_password)
    else:
        file_buffer_vpath = file_support.merge_vpath(buffer_root_vpath, file_virtual_local_middle_path)
        file_support.real_copy_file_folder(file_local_vpath, file_buffer_vpath)

def post_move_to_buffer(file_vpath_in_buffer):
    file_support.real_delete_local_path(file_vpath_in_buffer)
    file_support.local_delete_empty_parent_folders(file_vpath_in_buffer)

def get_file_buffer_path(file_root_path, file_middle_path):
    if config_instance.get_mode() == Mode.ENCRYPTED:
        return file_support.merge_vpath(file_root_path, encrypt_support.encode_path(file_middle_path))
    return file_support.merge_vpath(file_root_path, file_middle_path)

def get_file_cloud_path_for_local_use(file_root_path, file_middle_path):
    return file_support.merge_vpath(file_root_path, file_middle_path)

def get_file_cloud_path_for_cloud_use(file_root_path, file_middle_path):
    if config_instance.get_mode() == Mode.ENCRYPTED:
        return file_support.merge_vpath(file_root_path, encrypt_support.encode_path(file_middle_path))
    return file_support.merge_vpath(file_root_path, file_middle_path)

def get_file_cloud_path(file_root_path, file_middle_path):
    return file_support.merge_vpath(file_root_path, file_middle_path)

def get_unencrypted_path(a_path): # a_path coule be a middle_path or a absolute path
    if config_instance.get_mode() == Mode.ENCRYPTED:
        return encrypt_support.decode_path(a_path)
    return a_path
