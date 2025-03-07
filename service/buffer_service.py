
'''
Buffer always keep the same with cloud,
if the cloud is unencrypted, the buffer is unencrypted
if the cloud is encrypted, the buffer is encrypted

if the mode is encrypted, unencrypted file during move from buffer to local
if the mode is encrypted, encrypted file during move from local to buffer
'''
from model.config import config_instance, Mode

from model.file_git import fgit_instance

from support import file_support
from support import encrypt_support
from model.logger import logger_instance

# def move_to_local(source_file_vpath_in_buffer:str):
#     local_vpath = file_support.get_current_vpath()

#     file_buffer_middle_vpath = source_file_vpath_in_buffer.removeprefix(fgit_instance.get_buffer_folder_vpath(local_vpath))
#     if config_instance.get_mode() == Mode.ENCRYPTED:
#         decode_middle_vpath = encrypt_support.decode_path(file_buffer_middle_vpath)
#         file_local_vpath = file_support.merge_vpath(config_instance.get_local_vpath(), decode_middle_vpath)
#         encrypt_support.decrypt_file(source_file_vpath_in_buffer, file_local_vpath, config_instance.get_password())
#     else:
#         file_local_vpath = file_support.merge_vpath(config_instance.get_local_vpath(), file_buffer_middle_vpath)
#         file_support.real_move_file_folder(source_file_vpath_in_buffer, file_local_vpath)
def move_to_local(buffer_root_vpath:str, buffer_middle_vpath:str, local_root_vpath:str, local_middle_vpath:str):
    buffer_file_rpath = file_support.merge_convert_rpath(buffer_root_vpath, buffer_middle_vpath)
    file_local_rpath = file_support.merge_convert_rpath(local_root_vpath, local_middle_vpath)
    if config_instance.get_mode() == Mode.ENCRYPTED:
        encrypt_support.decrypt_file(buffer_file_rpath, file_local_rpath, config_instance.get_password())
    else:
        file_support.real_move_file_folder(buffer_file_rpath, file_local_rpath)

# def post_move_to_local(source_file_vpath_in_buffer):
#     file_support.real_delete_local_path(source_file_vpath_in_buffer)
#     file_support.local_delete_empty_parent_folders(source_file_vpath_in_buffer)
def post_move_to_local(buffer_root_vpath:str, buffer_middle_vpath:str):
    buffer_file_rpath = file_support.merge_convert_rpath(buffer_root_vpath, buffer_middle_vpath)
    file_support.real_delete_local_path(buffer_file_rpath)
    file_support.local_delete_empty_parent_folders(buffer_file_rpath)

# def move_to_buffer(file_local_vpath:str, local_root_vpath, buffer_root_vpath, mode:Mode=Mode.ORIGINAL, encrtpted_password=None):
#     file_virtual_local_middle_path = file_local_vpath.removeprefix(local_root_vpath)
#     logger_instance.log_debug("{} : moving {} buffer".format(mode, file_virtual_local_middle_path))
#     if mode == Mode.ENCRYPTED:
#         encode_middle_vpath = encrypt_support.encode_path(file_virtual_local_middle_path)
#         encode_file_vpath = file_support.merge_vpath(buffer_root_vpath, encode_middle_vpath)
#         if file_support.is_local_exist(encode_file_vpath):
#             print("encryptes file exist, skip: ", encode_file_vpath)
#             return
#         encrypt_support.encrypt_file(file_local_vpath, encode_file_vpath, encrtpted_password)
#         logger_instance.log_debug("ENCRYPTE mode: {} {}".format(mode, encode_middle_vpath))
#     else:
#         file_buffer_vpath = file_support.merge_vpath(buffer_root_vpath, file_virtual_local_middle_path)
#         file_support.real_copy_file_folder(file_local_vpath, file_buffer_vpath)
#         logger_instance.log_debug("ORIGINAL mode: {} {}".format(mode, file_virtual_local_middle_path))

def move_to_buffer(local_root_vpath:str, local_middle_vpath:str, buffer_root_vpath:str, buffer_middle_vpath:str):
    local_file_rpath = file_support.merge_convert_rpath(local_root_vpath, local_middle_vpath)
    buffer_file_rpath = file_support.merge_convert_rpath(buffer_root_vpath, buffer_middle_vpath)
    if config_instance.get_mode() == Mode.ENCRYPTED:
        encrypt_support.encrypt_file(local_file_rpath, buffer_file_rpath, config_instance.get_password())
    else:
        file_support.real_copy_file_folder(local_file_rpath, buffer_file_rpath)

# def post_move_to_buffer(file_vpath_in_buffer):
#     file_support.real_delete_local_path(file_vpath_in_buffer)
#     file_support.local_delete_empty_parent_folders(file_vpath_in_buffer)
#     logger_instance.log_debug("Post Move To Buffer delete: {}".format(file_vpath_in_buffer))
def post_move_to_buffer(buffer_root_vpath:str, buffer_middle_vpath:str):
    buffer_file_rpath = file_support.merge_convert_rpath(buffer_root_vpath, buffer_middle_vpath)
    file_support.real_delete_local_path(buffer_file_rpath)
    file_support.local_delete_empty_parent_folders(buffer_file_rpath)
    # logger_instance.log_debug("Post Move To Buffer delete: {}".format(file_vpath_in_buffer))


# def get_file_buffer_path(file_root_path, file_middle_path):
#     if config_instance.get_mode() == Mode.ENCRYPTED:
#         return file_support.merge_vpath(file_root_path, encrypt_support.encode_path(file_middle_path))
#     return file_support.merge_vpath(file_root_path, file_middle_path)

# def get_file_cloud_path_for_local_use(file_root_path, file_middle_path):
#     return file_support.merge_vpath(file_root_path, file_middle_path)

# def get_file_cloud_path_for_cloud_use(file_root_path, file_middle_path):
#     logger_instance.log_debug("get_file_cloud_path_for_cloud_use before: {}".format(file_middle_path))
#     res = ""
#     if config_instance.get_mode() == Mode.ENCRYPTED:
#         res = file_support.merge_vpath(file_root_path, encrypt_support.encode_path(file_middle_path))
#     res = file_support.merge_vpath(file_root_path, file_middle_path)
#     logger_instance.log_debug("get_file_cloud_path_for_cloud_use: {} {} {}".format(config_instance.get_mode(), file_middle_path, res))
#     return res

def get_buffer_cloud_middle_path_base_mode(original_vpath:str):
    res = original_vpath
    if config_instance.get_mode() == Mode.ENCRYPTED:
        res = encrypt_support.encode_path(original_vpath)
    return res

# def get_file_cloud_path(file_root_path, file_middle_path):
#     return file_support.merge_vpath(file_root_path, file_middle_path)

def get_unencrypted_path(file_vpath): # a_path coule be a middle_path or a absolute path
    if config_instance.get_mode() == Mode.ENCRYPTED:
        return encrypt_support.decode_path(file_vpath)
    return file_vpath
