


import support.fgit_support
from uttest.abstract_test import AbstractBDWPTestCase
from unittest.mock import patch

from uttest import test_support
from hook.hook import Hooks
from command.command_set_config import command_set_config
from model.config import FilegitConfig
from support import file_support

from support.bdwp_support import bdwp_instance
from command import command_queue

from service import file_service
from facade import index_facade
from support import time_support
from model.config import FilegitConfig
from facade.queue_facade import queue_instance
from model import constant

class TestCommandPush(AbstractBDWPTestCase):
    
    # before each function
    def setUp(self):
        bdwp_instance.set_access_token(test_support.test_support_instance.get_fgit_access_token())
        bdwp_instance.create_folder(test_support.test_support_instance.get_mock_cloud_vpath())
        file_support.create_local_folder(test_support.test_support_instance.get_mock_local_vpath())

    @patch('os.getcwd')
    def test_command_clone_original(self, mock_getcwd):
        # mocking
        mock_getcwd.return_value = test_support.test_support_instance.get_mock_local_vpath()
        test_support.run_command_init(test_support.TestSupport.original_fgit_mode)
        test_support.create_file_in_remote(test_support.test_support_instance.get_test_file_txt_2_local_vpath(), test_support.test_support_instance.get_test_file_txt_2_cloud_vpath(), "txt")
        test_support.create_file(1, test_support.test_support_instance.get_test_file_txt_1_local_vpath())
        test_support.create_file(1, test_support.test_support_instance.get_test_file_txt_2_local_vpath())
        test_support.create_file(1, test_support.test_support_instance.get_test_file_txt_3_local_vpath())

        today_ymd = time_support.get_time_with_ymd()
        current_action_folder_name = support.fgit_support.get_action_folder_name("push")
        current_action_folder_path = file_support.merge_vpath(FilegitConstant.action_folder_vpath, current_action_folder_name)
        file_support.create_local_folder(current_action_folder_path)

        # prepare queue.json
        queue_json_data = {
            "lock": True,
            "action_folder": current_action_folder_name,
            "key_set": ["15a6507461227f6a48b8cbe5663b4785", "44961f61736f40a8b16f919a42689636"],
            "queue_item": {    
                "15a6507461227f6a48b8cbe5663b4785": {
                    "middle_path": "test_1.txt",
                    "action": "UPLOAD",
                    "status": "PENDING"
                },
                "44961f61736f40a8b16f919a42689636": {
                    "middle_path": "folder2/folder22/test_3.txt",
                    "action": "UPLOAD",
                    "status": "PENDING"
                }
            }
        }

        file_support.real_write_json_file(constant.QUEUE_FILE_VPATH, queue_json_data)
        queue_instance.read_queue()

        Hooks.base_hook()
        Hooks.clean_trash()
        command_queue.command_queue()

        queue_instance.read_queue()

        local_today_trash_folder_path = file_support.merge_vpath(FilegitConstant.trash_folder_vpath, today_ymd)
        remote_today_trash_folder_path = file_support.merge_vpath(FilegitConfig.get_remote_vpath(), ".trash", today_ymd)
        
        
        local_log_folder_path = file_support.merge_vpath(current_action_folder_path, "log")
        success_log_file_path = file_support.merge_vpath(local_log_folder_path, "success.log")
        error_log_file_path = file_support.merge_vpath(local_log_folder_path, "error.log")

        # assert local files
        assert test_support.count_file(test_support.test_support_instance.get_mock_local_vpath()) == 3
        # asert cloud files
        assert len(index_facade.get_cloud_index(FilegitConfig.get_remote_vpath())) == 3
        # assert local trash    
        assert test_support.count_file(local_today_trash_folder_path) == 0
        # assert remote trash
        assert file_service.cloud_is_file_exist(remote_today_trash_folder_path) == False
        # assert buffer folder
        assert test_support.count_file(FilegitConstant.buffer_folder_vpath) == 0

        # assert queue.json
        assert queue_instance.get_virtual_action_folder() == None
        assert queue_instance.is_lock() == False
        assert len(queue_instance.get_key_set()) == 0
        assert len(queue_instance.get_queue_item()) == 0
        
        # assert log file
        assert file_support.is_local_exist(error_log_file_path) == False
        assert test_support.count_lines_in_file(success_log_file_path) == 2


    @patch('os.getcwd')
    def test_command_clone_encrypted(self, mock_getcwd):
        # mocking
        mock_getcwd.return_value = test_support.test_support_instance.get_mock_local_vpath()

        test_support.run_command_init(test_support.TestSupport.encrypted_fgit_mode)
        test_support.create_file_in_remote(test_support.test_support_instance.get_test_file_txt_2_local_vpath(), test_support.test_support_instance.get_test_file_txt_2_cloud_vpath(), "txt")
        test_support.create_file(1, test_support.test_support_instance.get_test_file_txt_1_local_vpath())
        test_support.create_file(1, test_support.test_support_instance.get_test_file_txt_2_local_vpath())
        test_support.create_file(1, test_support.test_support_instance.get_test_file_txt_3_local_vpath())

        today_ymd = time_support.get_time_with_ymd()
        current_action_folder_name = support.fgit_support.get_action_folder_name("push")
        current_action_folder_path = file_support.merge_vpath(FilegitConstant.action_folder_vpath, current_action_folder_name)
        file_support.create_local_folder(current_action_folder_path)

        # prepare queue.json
        queue_json_data = {
            "lock": True,
            "action_folder": current_action_folder_name,
            "key_set": ["15a6507461227f6a48b8cbe5663b4785", "44961f61736f40a8b16f919a42689636"],
            "queue_item": {    
                "15a6507461227f6a48b8cbe5663b4785": {
                    "middle_path": "test_1.txt",
                    "action": "UPLOAD",
                    "status": "PENDING"
                },
                "44961f61736f40a8b16f919a42689636": {
                    "middle_path": "folder2/folder22/test_3.txt",
                    "action": "UPLOAD",
                    "status": "PENDING"
                }
            }
        }

        file_support.real_write_json_file(constant.QUEUE_FILE_VPATH, queue_json_data)
        queue_instance.read_queue()

        Hooks.base_hook()
        Hooks.clean_trash()
        command_queue.command_queue()

        queue_instance.read_queue()

        local_today_trash_folder_path = file_support.merge_vpath(FilegitConstant.trash_folder_vpath, today_ymd)
        remote_today_trash_folder_path = file_support.merge_vpath(FilegitConfig.get_remote_vpath(), ".trash", today_ymd)
        
        
        local_log_folder_path = file_support.merge_vpath(current_action_folder_path, "log")
        success_log_file_path = file_support.merge_vpath(local_log_folder_path, "success.log")
        error_log_file_path = file_support.merge_vpath(local_log_folder_path, "error.log")

        # assert local files
        assert test_support.count_file(test_support.test_support_instance.get_mock_local_vpath()) == 3
        # asert cloud files
        assert len(index_facade.get_cloud_index(FilegitConfig.get_remote_vpath())) == 3
        # assert local trash    
        assert test_support.count_file(local_today_trash_folder_path) == 0
        # assert remote trash
        assert file_service.cloud_is_file_exist(remote_today_trash_folder_path) == False
        # assert buffer folder
        assert test_support.count_file(FilegitConstant.buffer_folder_vpath) == 0

        # assert queue.json
        assert queue_instance.get_virtual_action_folder() == None
        assert queue_instance.is_lock() == False
        assert len(queue_instance.get_key_set()) == 0
        assert len(queue_instance.get_queue_item()) == 0
        
        # assert log file
        assert file_support.is_local_exist(error_log_file_path) == False
        assert test_support.count_lines_in_file(success_log_file_path) == 2

    # after each function
    def tearDown(self):
        bdwp_instance.delete_file_folder(test_support.test_support_instance.get_mock_cloud_vpath())
        file_support.real_delete_local_path(test_support.test_support_instance.get_mock_local_vpath())
