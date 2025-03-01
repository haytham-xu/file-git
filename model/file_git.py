
from support import file_support
from support import time_support
from model.constant import FilegitConstant
from model.config import config_instance
from model.logger import logger_instance

class Filegit():

    def get_fgit_folder_vpath(self, local_vpath):
        return file_support.merge_vpath(local_vpath, FilegitConstant.FGIT_FOLDER_NAME) # /PWD/.fgit/
    def get_trash_folder_vpath(self, local_vpath):
        return file_support.merge_vpath(local_vpath, FilegitConstant.FGIT_FOLDER_NAME, FilegitConstant.TRASH_FOLDER_NAME) # /PWD/.fgit/trash/
    def get_action_folder_vpath(self, local_vpath):
        return file_support.merge_vpath(local_vpath, FilegitConstant.FGIT_FOLDER_NAME, FilegitConstant.ACTION_FOLDER_NAME) # /PWD/.fgit/action/
    def get_buffer_folder_vpath(self, local_vpath):
        return file_support.merge_vpath(local_vpath, FilegitConstant.FGIT_FOLDER_NAME, FilegitConstant.BUFFER_FOLDER_NAME) # /PWD/.fgit/buffer/
    def get_chunk_folder_vpath(self, local_vpath):
        return file_support.merge_vpath(local_vpath, FilegitConstant.FGIT_FOLDER_NAME, FilegitConstant.CHUNK_FOLDER_NAME) # /PWD/.fgit/chunks/
    def get_config_file_vpath(self, local_vpath):
        return file_support.merge_vpath(local_vpath, FilegitConstant.FGIT_FOLDER_NAME, FilegitConstant.CONFIG_FILE_NAME) # /PWD/.fgit/config.json
    def get_local_index_file_vpath(self, local_vpath):
        return file_support.merge_vpath(local_vpath, FilegitConstant.FGIT_FOLDER_NAME, FilegitConstant.LOCAL_INDEX_FILE_NAME) # /PWD/.fgit/local.json
    def get_cloud_index_file_vpath(self, local_vpath):
        return file_support.merge_vpath(local_vpath, FilegitConstant.FGIT_FOLDER_NAME, FilegitConstant.CLOUD_INDEX_FILE_NAME) # /PWD/.fgit/remote.json

    def init_action(self, action_name):
        # 1. init current path， init constant
        # 2. init action folder
        local_vpath = file_support.get_current_vpath()
        action_folder_name = "{}_{}".format(time_support.get_time_with_ymd(), action_name)
        action_folder_vpath = file_support.merge_vpath(self.get_action_folder_vpath(local_vpath), action_folder_name)
        file_support.create_local_folder(vpath=action_folder_vpath)
        # 3. init config
        config_instance.init(self.get_config_file_vpath(local_vpath))
        # 3. init log
        logger_instance.init_log_file(action_folder_vpath)

fgit_instance = Filegit()
