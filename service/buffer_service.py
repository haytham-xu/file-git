
'''
Buffer always keep the same with cloud,
if the cloud is unencrypted, the buffer is unencrypted
if the cloud is encrypted, the buffer is encrypted

if the mode is encrypted, unencrypted file during move from buffer to local
if the mode is encrypted, encrypted file during move from local to buffer
'''
from model.config import config_instance, Mode

from support import file_support
from support import encrypt_support
from model.logger import logger_instance

def move_to_local(buffer_root_vpath:str, buffer_middle_vpath:str, local_root_vpath:str, local_middle_vpath:str):
    buffer_file_rpath = file_support.merge_convert_rpath(buffer_root_vpath, buffer_middle_vpath)
    file_local_rpath = file_support.merge_convert_rpath(local_root_vpath, local_middle_vpath)
    if config_instance.get_mode() == Mode.ENCRYPTED:
        encrypt_support.decrypt_file(buffer_file_rpath, file_local_rpath, config_instance.get_password())
    else:
        file_support.real_move_file_folder(buffer_file_rpath, file_local_rpath)
    logger_instance.log_debug("Move To Local: {} {}".format(buffer_middle_vpath, local_middle_vpath))

def post_move_to_local(buffer_root_vpath:str, buffer_middle_vpath:str):
    buffer_file_rpath = file_support.merge_convert_rpath(buffer_root_vpath, buffer_middle_vpath)
    file_support.real_delete_local_path(buffer_file_rpath)
    file_support.local_delete_empty_parent_folders(buffer_file_rpath)
    logger_instance.log_debug("Post Move To Local delete: {}".format(buffer_middle_vpath))

def move_to_buffer(local_root_vpath:str, local_middle_vpath:str, buffer_root_vpath:str, buffer_middle_vpath:str):
    local_file_rpath = file_support.merge_convert_rpath(local_root_vpath, local_middle_vpath)
    buffer_file_rpath = file_support.merge_convert_rpath(buffer_root_vpath, buffer_middle_vpath)
    if config_instance.get_mode() == Mode.ENCRYPTED:
        encrypt_support.encrypt_file(local_file_rpath, buffer_file_rpath, config_instance.get_password())
    else:
        file_support.real_copy_file_folder(local_file_rpath, buffer_file_rpath)
    logger_instance.log_debug("Move To Buffer: {} {}".format(local_middle_vpath, buffer_middle_vpath))


def post_move_to_buffer(buffer_root_vpath:str, buffer_middle_vpath:str):
    buffer_file_rpath = file_support.merge_convert_rpath(buffer_root_vpath, buffer_middle_vpath)
    file_support.real_delete_local_path(buffer_file_rpath)
    file_support.local_delete_empty_parent_folders(buffer_file_rpath)
    logger_instance.log_debug("Post Move To Buffer delete: {}".format(buffer_middle_vpath))

def get_buffer_cloud_middle_path_base_mode(original_vpath:str):
    res = original_vpath
    if config_instance.get_mode() == Mode.ENCRYPTED:
        res = encrypt_support.encode_path(original_vpath)
    return res

def get_unencrypted_path(file_vpath): # a_path coule be a middle_path or a absolute path
    if config_instance.get_mode() == Mode.ENCRYPTED:
        return encrypt_support.decode_path(file_vpath)
    return file_vpath
