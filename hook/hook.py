
import os 

from support import file_support
from support.config_support import config_instance
from support.constant_support import constant_instance
from support.bdwp_support import bdwp_instance
from support.queue_support import queue_instance

from datetime import datetime

class Hooks:

    @staticmethod
    def base_hook():
        Hooks.init_constant()
        Hooks.init_config()
        Hooks.verify_fgit_folder()
        Hooks.init_baidu_wangpan()
        Hooks.init_queue_file_path()

    @staticmethod
    def init_constant():
        virtual_current_path = file_support.virtual_get_current_path()
        constant_instance.set_virtual_local_path(virtual_current_path)

    @staticmethod
    def init_config():
        config_instance.read_config(constant_instance.get_virtual_config_file_path())

    @staticmethod
    def verify_fgit_folder():
        if not file_support.real_is_local_exist(constant_instance.get_virtual_file_git_folder_path()):
            raise FileNotFoundError(f"File git folder '{constant_instance.get_virtual_file_git_folder_path()}' does not exist.")
        if not file_support.real_is_local_exist(constant_instance.get_virtual_trash_folder_path()):
            raise FileNotFoundError(f"Trash folder '{constant_instance.get_virtual_trash_folder_path()}' does not exist.")
        if not file_support.real_is_local_exist(constant_instance.get_virtual_action_folder_path()):
            raise FileNotFoundError(f"Action folder '{constant_instance.get_virtual_action_folder_path()}' does not exist.")
        if not file_support.real_is_local_exist(constant_instance.get_virtual_config_file_path()):
            raise FileNotFoundError(f"config_instance file '{constant_instance.get_virtual_config_file_path()}' does not exist.")
        if not file_support.real_is_local_exist(constant_instance.get_virtual_queue_file_path()):
            raise FileNotFoundError(f"Queue file '{constant_instance.get_virtual_queue_file_path()}' does not exist.")
        queue_file_json = file_support.real_read_json_file(constant_instance.get_virtual_queue_file_path())
        if 'lock' not in queue_file_json:
            raise KeyError(f"Key 'lock' does not exist in queue file '{constant_instance.get_virtual_queue_file_path()}'")
        if 'queue_item' not in queue_file_json:
            raise KeyError(f"Key 'queue_item' does not exist in queue file '{constant_instance.get_virtual_queue_file_path()}'")

    @staticmethod
    def init_baidu_wangpan():
        bdwp_instance.set_access_token(config_instance.get_access_token())

    @staticmethod
    def init_queue_file_path():
        queue_instance.set_virtual_queue_file_path(constant_instance.get_virtual_queue_file_path())

    @staticmethod
    def init_queue_instance():
        queue_instance.read_queue()

    @staticmethod
    def check_queue_lock():
        if queue_instance.is_lock():
            raise Exception("Queue is locked, please run 'fgit queue' to continue queue.")

    @staticmethod
    def clean_trash():
        trash_folder_virtual_path = constant_instance.get_virtual_trash_folder_path()
        current_date = datetime.now()
        for folder_name in file_support.real_listdir(trash_folder_virtual_path):
            folder_virtual_path = os.path.join(trash_folder_virtual_path, folder_name)
            if file_support.real_is_dir(folder_virtual_path):
                try:
                    folder_date = datetime.strptime(folder_name, "%Y%m%d")
                    date_diff = (current_date - folder_date).days
                    if date_diff > 7:
                        file_support.real_delete_local_path(folder_virtual_path)
                        print(f"Deleted folder: {folder_virtual_path}")
                except ValueError:
                    print(f"Skipped invalid folder: {folder_virtual_path}")
