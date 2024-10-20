

from uttest.abstract_test import AbstractTestCase
from unittest.mock import patch

from uttest import test_support
from hook.hook import Hooks
from command.command_set_config import command_set_config
from support.config_support import config_instance
from support import file_support
from support.constant_support import constant_instance

from support.bdwp_support import bdwp_instance
from command import command_verify


from service import file_service
from facade import index_facade
from support import time_support
from support.config_support import config_instance
from support.queue_support import queue_instance
from support.constant_support import constant_instance

class TestCommandVerify(AbstractTestCase):
    
    # before each function
    def setUp(self):
        bdwp_instance.set_access_token(test_support.fgit_access_token)
        bdwp_instance.create_folder(test_support.cloud_test_folder_root_virtual_path)
        file_support.real_create_local_folder(test_support.local_test_root_folder_virtual_path)

    @patch('os.getcwd')
    def test_command_verify_original(self, mock_getcwd):
        # mocking
        mock_getcwd.return_value = test_support.local_test_root_folder_virtual_path
        
        test_support.run_command_init(test_support.original_fgit_mode)
        test_support.create_file_in_remote(test_support.test_file_txt_1_local_virtual_path, test_support.test_file_txt_1_cloud_virtual_path, "txt")
        test_support.create_file_in_remote(test_support.test_file_txt_2_local_virtual_path, test_support.test_file_txt_2_cloud_virtual_path, "txt")
        test_support.create_file_in_remote(test_support.test_file_txt_3_local_virtual_path, test_support.test_file_txt_3_cloud_virtual_path, "txt")
        test_support.create_file(1, test_support.test_file_txt_1_local_virtual_path)
        test_support.create_file(1, test_support.test_file_txt_2_local_virtual_path)
        test_support.create_file(1, test_support.test_file_txt_3_local_virtual_path)

        Hooks.base_hook()
        Hooks.clean_trash()
        result = command_verify.command_verify()
        
        
        assert result == False

        queue_instance.read_queue()
        today_ymd = time_support.get_time_with_ymd()
        current_action_folder_name = time_support.get_action_folder_name("pull")

        local_today_trash_folder_path = file_support.virtual_merge_path(constant_instance.get_virtual_trash_folder_path(), today_ymd)
        remote_today_trash_folder_path = file_support.virtual_merge_path(config_instance.get_virtual_remote_path(), ".trash", today_ymd)
        current_action_folder_path = file_support.virtual_merge_path(constant_instance.get_virtual_action_folder_path(), current_action_folder_name)
        
        local_log_folder_path = file_support.virtual_merge_path(current_action_folder_path, "log")
        success_log_file_path = file_support.virtual_merge_path(local_log_folder_path, "success.log")
        error_log_file_path = file_support.virtual_merge_path(local_log_folder_path, "error.log")

        # assert local files
        assert test_support.count_file(test_support.local_test_root_folder_virtual_path) == 3
        # asert cloud files
        assert len(index_facade.get_cloud_index(config_instance.get_virtual_remote_path())) == 3
        # assert local trash    
        assert test_support.count_file(local_today_trash_folder_path) == 0
        # assert remote trash
        assert file_service.is_file_exist_in_cloud(remote_today_trash_folder_path) == False
        # assert buffer folder
        assert test_support.count_file(constant_instance.get_virtual_buffer_folder_path()) == 0

        # assert queue.json
        assert queue_instance.get_virtual_action_folder() == None
        assert queue_instance.is_lock() == False
        assert len(queue_instance.get_key_set()) == 0
        assert len(queue_instance.get_queue_item()) == 0
        
        # assert log file
        assert file_support.real_is_local_exist(error_log_file_path) == False
        assert file_support.real_is_local_exist(success_log_file_path) == False

    @patch('os.getcwd')
    def test_command_verify_encrypted(self, mock_getcwd):
        # mocking
        mock_getcwd.return_value = test_support.local_test_root_folder_virtual_path
        
        test_support.run_command_init(test_support.encrypted_fgit_mode)
        test_support.create_file_in_remote(test_support.test_file_txt_1_local_virtual_path, test_support.test_file_txt_1_cloud_virtual_path, "txt")
        test_support.create_file_in_remote(test_support.test_file_txt_2_local_virtual_path, test_support.test_file_txt_2_cloud_virtual_path, "txt")
        test_support.create_file_in_remote(test_support.test_file_txt_3_local_virtual_path, test_support.test_file_txt_3_cloud_virtual_path, "txt")
        test_support.create_file(1, test_support.test_file_txt_1_local_virtual_path)
        test_support.create_file(1, test_support.test_file_txt_2_local_virtual_path)
        test_support.create_file(1, test_support.test_file_txt_3_local_virtual_path)

        Hooks.base_hook()
        Hooks.clean_trash()
        result = command_verify.command_verify()
        
        
        assert result == False

        queue_instance.read_queue()
        today_ymd = time_support.get_time_with_ymd()
        current_action_folder_name = time_support.get_action_folder_name("pull")

        local_today_trash_folder_path = file_support.virtual_merge_path(constant_instance.get_virtual_trash_folder_path(), today_ymd)
        remote_today_trash_folder_path = file_support.virtual_merge_path(config_instance.get_virtual_remote_path(), ".trash", today_ymd)
        current_action_folder_path = file_support.virtual_merge_path(constant_instance.get_virtual_action_folder_path(), current_action_folder_name)
        
        local_log_folder_path = file_support.virtual_merge_path(current_action_folder_path, "log")
        success_log_file_path = file_support.virtual_merge_path(local_log_folder_path, "success.log")
        error_log_file_path = file_support.virtual_merge_path(local_log_folder_path, "error.log")

        # assert local files
        assert test_support.count_file(test_support.local_test_root_folder_virtual_path) == 3
        # asert cloud files
        assert len(index_facade.get_cloud_index(config_instance.get_virtual_remote_path())) == 3
        # assert local trash    
        assert test_support.count_file(local_today_trash_folder_path) == 0
        # assert remote trash
        assert file_service.is_file_exist_in_cloud(remote_today_trash_folder_path) == False
        # assert buffer folder
        assert test_support.count_file(constant_instance.get_virtual_buffer_folder_path()) == 0

        # assert queue.json
        assert queue_instance.get_virtual_action_folder() == None
        assert queue_instance.is_lock() == False
        assert len(queue_instance.get_key_set()) == 0
        assert len(queue_instance.get_queue_item()) == 0
        
        # assert log file
        assert file_support.real_is_local_exist(error_log_file_path) == False
        assert file_support.real_is_local_exist(success_log_file_path) == False

    # after each function
    def tearDown(self):
        bdwp_instance.delete_file_folder(test_support.cloud_test_folder_root_virtual_path)
        file_support.real_delete_local_path(test_support.local_test_root_folder_virtual_path)



