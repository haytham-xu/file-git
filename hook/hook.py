
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

    @staticmethod
    def init_constant():
        current_path = os.getcwd()
        constant_instance.set_local_path(current_path)

    @staticmethod
    def init_config():
        config_instance.read_config(constant_instance.get_config_file_path())

    @staticmethod
    def verify_fgit_folder():
        if not file_support.is_exist(constant_instance.get_file_git_folder_path()):
            raise FileNotFoundError(f"File git folder '{constant_instance.get_file_git_folder_path()}' does not exist.")
        if not file_support.is_exist(constant_instance.get_trash_folder_path()):
            raise FileNotFoundError(f"Trash folder '{constant_instance.get_trash_folder_path()}' does not exist.")
        if not file_support.is_exist(constant_instance.get_action_folder_path()):
            raise FileNotFoundError(f"Action folder '{constant_instance.get_action_folder_path()}' does not exist.")
        if not file_support.is_exist(constant_instance.get_config_file_path()):
            raise FileNotFoundError(f"config_instance file '{constant_instance.get_config_file_path()}' does not exist.")
        if not file_support.is_exist(constant_instance.get_queue_file_path()):
            raise FileNotFoundError(f"Queue file '{constant_instance.get_queue_file_path()}' does not exist.")
        queue_file_json = file_support.read_json_file(constant_instance.get_queue_file_path())
        if 'lock' not in queue_file_json:
            raise KeyError(f"Key 'lock' does not exist in queue file '{constant_instance.get_queue_file_path()}'")
        if 'queue_item' not in queue_file_json:
            raise KeyError(f"Key 'queue_item' does not exist in queue file '{constant_instance.get_queue_file_path()}'")

    @staticmethod
    def init_baidu_wangpan():
        bdwp_instance.set_access_token(config_instance.get_access_token())

    @staticmethod
    def init_queue():
        queue_instance.read_queue(constant_instance.get_queue_file_path())

    @staticmethod
    def check_queue_lock():
        if queue_instance.is_lock():
            raise Exception("Queue is locked, please run 'fgit queue' to continue queue.")

    @staticmethod
    def clean_trash():
        trash_folder_path = constant_instance.get_trash_folder_path()
        current_date = datetime.now()
        for folder_name in os.listdir(trash_folder_path):
            folder_path = os.path.join(trash_folder_path, folder_name)
            if os.path.isdir(folder_path):
                try:
                    folder_date = datetime.strptime(folder_name, "%Y%m%d")
                    date_diff = (current_date - folder_date).days
                    if date_diff > 7:
                        file_support.delete_path(folder_path)
                        print(f"Deleted folder: {folder_path}")
                except ValueError:
                    print(f"Skipped invalid folder: {folder_path}")
