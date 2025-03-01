
from command import command_push
from command.command_init import command_init

from facade import index_facade
from facade.queue_facade import queue_instance

from model.queue import QueueItem
from model.logger import logger_instance

from support import file_support
from support.bdwp_support import bdwp_instance

from uttest.abstract_test import AbstractBDWPTestCase
from uttest.test_support import test_support_instance
from uttest import test_support

class TestCommandPush(AbstractBDWPTestCase):
    
    # before each function
    def setUp(self):
        bdwp_instance.create_folder(test_support_instance.get_mock_cloud_vpath())
        file_support.create_local_folder(test_support_instance.get_mock_local_vpath())

    # python3 -m unittest uttest.test_command_push.TestCommandPush.test_command_push_original -v -f
    def test_command_push_original(self):
        file_support.real_delete_local_path("/Users/I353667/Documents/code/github/file-git/uttest/tmp")
        # local path: ./uttest/tmp/local/test_fgit
        # cloud path: ./uttest/tmp/cloud/test_fgit
        command_init(local_vpath=test_support_instance.get_mock_local_vpath(), remote_vpath=test_support_instance.get_mock_cloud_vpath())

        txt_1_name = "/l_1.txt"
        txt_2_name = "/lf_1/l_2.txt"
        txt_3_name = "/lf_2/lf_22/l_3.txt"
        png_1_name = "/c_1.png"
        png_2_name = "/cf_1/c_2.png"
        png_3_name = "/cf_2/cf_22/c_3.png"

        test_support_instance.create_file('txt', "local", txt_1_name)
        test_support_instance.create_file('txt', "local", txt_2_name)
        test_support_instance.create_file('txt', "local", txt_3_name)
        test_support_instance.create_file('png', "cloud", png_1_name)
        test_support_instance.create_file('png', "cloud", png_2_name)
        test_support_instance.create_file('png', "cloud", png_3_name)

        command_push.command_push(False)

        # verify cloud files
        cloud_file_meta_list = index_facade.get_cloud_index(test_support_instance.get_mock_cloud_vpath())
        cloud_files_path_list = [value[QueueItem.KEY_MIDDLE_PATH] for value in cloud_file_meta_list.values()]
        logger_instance.log_debug("file in cloud", str(cloud_files_path_list))
        assert len(cloud_file_meta_list) == 3
        assert txt_1_name in cloud_files_path_list
        assert txt_2_name in cloud_files_path_list
        assert txt_3_name in cloud_files_path_list

        # verify local files
        local_file_meta_list = index_facade.get_local_index(test_support_instance.get_mock_local_vpath())
        local_files_path_list = [value[QueueItem.KEY_MIDDLE_PATH] for value in local_file_meta_list.values()]
        logger_instance.log_debug("file in local", str(local_files_path_list))
        assert len(local_file_meta_list) == 3
        assert txt_1_name in local_files_path_list
        assert txt_2_name in local_files_path_list
        assert txt_3_name in local_files_path_list

        # verify local trash
        local_trash_folder_vpath = test_support_instance.get_local_trash_folder_vpath()
        local_trash_file_meta_fist = index_facade.get_local_index(local_trash_folder_vpath)
        assert len(local_trash_file_meta_fist) == 0
        # verify buffer folder
        local_buffer_folder_vpath = test_support_instance.get_local_buffer_folder_vpath()
        local_buffer_file_meta_fist = index_facade.get_local_index(local_buffer_folder_vpath)
        assert len(local_buffer_file_meta_fist) == 0
        # verify cloud trash
        cloud_trash_folder_vpath = test_support_instance.get_cloud_trash_folder_vpath()
        cloud_trash_file_meta_fist = test_support.list_file_recursion_with_hidden(cloud_trash_folder_vpath)
        logger_instance.log_debug("file in cloud trash",  str(cloud_trash_file_meta_fist))
        assert len(cloud_trash_file_meta_fist) == 3
        
        # verify message queue
        assert queue_instance.is_lock() == False 
        assert queue_instance.is_queue_empty() == True

        # assert log file
        assert file_support.is_local_exist(logger_instance.get_log_error_file_vpath()) == False
        assert test_support.count_lines_in_file(logger_instance.get_log_success_file_vpath()) == 6

        # input("Press Enter to continue...")

        
    # @patch('os.getcwd')
    # def test_command_push_encrypted(self, mock_getcwd):
    #     # mocking
    #     mock_getcwd.return_value = test_support_instance.get_mock_local_test_vpath()
    #     run_command_init(TestSupport.encrypted_fgit_mode)
    #     create_file_in_remote(test_support_instance.get_test_file_txt_1_local_vpath(), test_support_instance.get_test_file_txt_1_cloud_vpath(), "txt")
    #     create_file_in_remote(test_support_instance.get_test_file_txt_2_local_vpath(), test_support_instance.get_test_file_txt_2_cloud_vpath(), "txt")
    #     create_file_in_remote(test_support_instance.get_test_file_txt_3_local_vpath(), test_support_instance.get_test_file_txt_3_cloud_vpath(), "txt")
    #     create_image(1, test_support_instance.get_test_file_png_1_local_vpath())
    #     create_image(1, test_support_instance.get_test_file_png_2_local_vpath())
    #     create_image(1, test_support_instance.get_test_file_png_3_local_vpath())

    #     Hooks.base_hook()
    #     Hooks.clean_trash()
    #     command_push.command_push()

    #     queue_instance.read_queue()
    #     today_ymd = time_support.get_time_with_ymd()
    #     current_action_folder_name = support.fgit_support.get_action_folder_name("push")

    #     local_today_trash_folder_path = file_support.merge_vpath(FilegitConstant.trash_folder_vpath, today_ymd)
    #     remote_today_trash_folder_path = file_support.merge_vpath(FilegitConfig.get_remote_vpath(), ".trash", today_ymd)
    #     current_action_folder_path = file_support.merge_vpath(FilegitConstant.action_folder_vpath, current_action_folder_name)
        
    #     local_log_folder_path = file_support.merge_vpath(current_action_folder_path, "log")
    #     success_log_file_path = file_support.merge_vpath(local_log_folder_path, "success.log")
    #     error_log_file_path = file_support.merge_vpath(local_log_folder_path, "error.log")
        
    #     # assert local files
    #     assert count_file(test_support_instance.get_mock_local_test_vpath()) == 3
    #     # asert cloud files
    #     assert len(index_facade.get_cloud_index(FilegitConfig.get_remote_vpath())) == 3
    #     # assert local trash    
    #     assert count_file(local_today_trash_folder_path) == 0
    #     # assert remote trash
    #     res = file_service.list_cloud_file_recursion(remote_today_trash_folder_path)
    #     assert len(res) == 3
    #     # assert buffer folder
    #     assert count_file(FilegitConstant.buffer_folder_vpath) == 0

    #     # assert queue.json
    #     assert queue_instance.get_virtual_action_folder() == None
    #     assert queue_instance.is_lock() == False
    #     assert len(queue_instance.get_key_set()) == 0
    #     assert len(queue_instance.get_queue_item()) == 0
        
    #     # assert log file
    #     assert file_support.is_local_exist(error_log_file_path) == False
    #     assert count_lines_in_file(success_log_file_path) == 6

    # after each function
    def tearDown(self):
        bdwp_instance.delete_file_folder(test_support_instance.get_mock_cloud_vpath())
        file_support.real_delete_local_path(test_support_instance.get_mock_local_vpath())
