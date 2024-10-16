
import os 

from support import file_support
from support.config_support import config_instance
from support.constant_support import constant_instance
from support.bdwp_support import bdwp_instance

class Hooks:

    @staticmethod
    def execute():
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
        if not file_support.is_exist(constant_instance.get_queue_file_path()):
            raise FileNotFoundError(f"Queue file '{constant_instance.get_queue_file_path()}' does not exist.")
        if not file_support.is_exist(constant_instance.get_config_file_path()):
            raise FileNotFoundError(f"config_instance file '{constant_instance.get_config_file_path()}' does not exist.")

    @staticmethod
    def init_baidu_wangpan():
        bdwp_instance.set_access_token(config_instance.get_access_token())
