
from uttest.abstract_test import AbstractTestCase
from unittest.mock import patch

from uttest import test_support
from hook.hook import Hooks
from command.command_set_config import command_set_config
from support.config_support import config_instance
from support import file_support
from support.constant_support import constant_instance

from support.bdwp_support import bdwp_instance
from command import command_push


from service import file_service
from facade import index_facade
from support import time_support
from support.config_support import config_instance
from support.queue_support import queue_instance
from support.constant_support import constant_instance

class TestCommandPush(AbstractTestCase):
    
    # before each function
    def setUp(self):
        bdwp_instance.set_access_token(test_support.fgit_access_token)
        bdwp_instance.create_folder(test_support.cloud_test_folder_root_path)
        file_support.create_folder(test_support.local_test_root_folder)

    @patch('os.getcwd')
    def test_command_push_original(self, mock_getcwd):
        # mocking
        mock_getcwd.return_value = test_support.local_test_root_folder
        test_support.run_command_init(test_support.original_fgit_mode)
        test_support.create_file_in_remote(test_support.test_file_txt_1_local_path, test_support.test_file_txt_1_cloud_path, "txt")
        test_support.create_file_in_remote(test_support.test_file_txt_2_local_path, test_support.test_file_txt_2_cloud_path, "txt")
        test_support.create_file_in_remote(test_support.test_file_txt_3_local_path, test_support.test_file_txt_3_cloud_path, "txt")
        test_support.create_image(1, test_support.test_file_png_1_local_path)
        test_support.create_image(1, test_support.test_file_png_2_local_path)
        test_support.create_image(1, test_support.test_file_png_3_local_path)

        Hooks.base_hook()
        Hooks.clean_trash()
        command_push.command_push()

        queue_instance.read_queue()
        today_ymd = time_support.get_time_with_ymd()
        current_action_folder_name = time_support.get_action_folder_name("push")

        local_today_trash_folder_path = file_support.merge_path(constant_instance.get_trash_folder_path(), today_ymd)
        remote_today_trash_folder_path = file_support.merge_path(config_instance.get_remote_path(), ".trash", today_ymd)
        current_action_folder_path = file_support.merge_path(constant_instance.get_action_folder_path(), current_action_folder_name)
        
        local_log_folder_path = file_support.merge_path(current_action_folder_path, "log")
        success_log_file_path = file_support.merge_path(local_log_folder_path, "success.log")
        error_log_file_path = file_support.merge_path(local_log_folder_path, "error.log")
        
        # assert local files
        assert test_support.count_file(test_support.local_test_root_folder) == 3
        # asert cloud files
        assert len(index_facade.get_cloud_index(config_instance.get_remote_path())) == 3
        # assert local trash    
        assert test_support.count_file(local_today_trash_folder_path) == 0
        # assert remote trash
        res = file_service.list_cloud_file_recursion(remote_today_trash_folder_path)
        assert len(res) == 3
        # assert buffer folder
        assert test_support.count_file(constant_instance.get_buffer_folder_path()) == 0

        # assert queue.json
        assert queue_instance.get_action_folder() == None
        assert queue_instance.is_lock() == False
        assert len(queue_instance.get_key_set()) == 0
        assert len(queue_instance.get_queue_item()) == 0
        
        # assert log file
        assert file_support.is_exist(error_log_file_path) == False
        assert test_support.count_lines_in_file(success_log_file_path) == 6

    @patch('os.getcwd')
    def test_command_push_encrypted(self, mock_getcwd):
        # mocking
        mock_getcwd.return_value = test_support.local_test_root_folder
        test_support.run_command_init(test_support.encrypted_fgit_mode)
        test_support.create_file_in_remote(test_support.test_file_txt_1_local_path, test_support.test_file_txt_1_cloud_path, "txt")
        test_support.create_file_in_remote(test_support.test_file_txt_2_local_path, test_support.test_file_txt_2_cloud_path, "txt")
        test_support.create_file_in_remote(test_support.test_file_txt_3_local_path, test_support.test_file_txt_3_cloud_path, "txt")
        test_support.create_image(1, test_support.test_file_png_1_local_path)
        test_support.create_image(1, test_support.test_file_png_2_local_path)
        test_support.create_image(1, test_support.test_file_png_3_local_path)

        Hooks.base_hook()
        Hooks.clean_trash()
        command_push.command_push()

        queue_instance.read_queue()
        today_ymd = time_support.get_time_with_ymd()
        current_action_folder_name = time_support.get_action_folder_name("push")

        local_today_trash_folder_path = file_support.merge_path(constant_instance.get_trash_folder_path(), today_ymd)
        remote_today_trash_folder_path = file_support.merge_path(config_instance.get_remote_path(), ".trash", today_ymd)
        current_action_folder_path = file_support.merge_path(constant_instance.get_action_folder_path(), current_action_folder_name)
        
        local_log_folder_path = file_support.merge_path(current_action_folder_path, "log")
        success_log_file_path = file_support.merge_path(local_log_folder_path, "success.log")
        error_log_file_path = file_support.merge_path(local_log_folder_path, "error.log")
        
        # assert local files
        assert test_support.count_file(test_support.local_test_root_folder) == 3
        # asert cloud files
        assert len(index_facade.get_cloud_index(config_instance.get_remote_path())) == 3
        # assert local trash    
        assert test_support.count_file(local_today_trash_folder_path) == 0
        # assert remote trash
        res = file_service.list_cloud_file_recursion(remote_today_trash_folder_path)
        assert len(res) == 3
        # assert buffer folder
        assert test_support.count_file(constant_instance.get_buffer_folder_path()) == 0

        # assert queue.json
        assert queue_instance.get_action_folder() == None
        assert queue_instance.is_lock() == False
        assert len(queue_instance.get_key_set()) == 0
        assert len(queue_instance.get_queue_item()) == 0
        
        # assert log file
        assert file_support.is_exist(error_log_file_path) == False
        assert test_support.count_lines_in_file(success_log_file_path) == 6

    # after each function
    def tearDown(self):
        bdwp_instance.delete_file_folder(test_support.cloud_test_folder_root_path)
        file_support.delete_path(test_support.local_test_root_folder)

