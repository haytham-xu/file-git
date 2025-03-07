
from command import command_push
from command.command_init import command_init

from facade import index_facade
from facade.queue_facade import queue_instance

from model.queue import QueueItem
from model.logger import logger_instance
from model.file_git import fgit_instance

from support import file_support
from support.bdwp_support import bdwp_instance

from uttest.abstract_test import AbstractBDWPTestCase
from uttest.test_support import test_support_instance
from uttest import test_support
from model.config import Mode

'''
python3 -m unittest uttest.test_command_push.TestCommandPush -v -f

python3 -m unittest uttest.test_command_push.TestCommandPush.test_command_pus_online_original -v -f
python3 -m unittest uttest.test_command_push.TestCommandPush.test_command_pus_offline_original -v -f
python3 -m unittest uttest.test_command_push.TestCommandPush.test_command_pus_online_encrypted -v -f
python3 -m unittest uttest.test_command_push.TestCommandPush.test_command_pus_offline_encrypted -v -f

{
    "637772eb0c3dc923a5fe1a5bc7c1fae9": {
        "middle_path": "/Y18xLnBuZw==",
        "size": 1048624
    },
    "1c32dc70c6f1f445b7422d2e72d1c575": {
        "middle_path": "/Y2ZfMQ==/Y18yLnBuZw==",
        "size": 1048624
    },
    "0497a49c66bf337994c3b9afdddd0bc3": {
        "middle_path": "/Y2ZfMg==/Y2ZfMjI=/Y18zLnBuZw==",
        "size": 1048624
    }
}
'''
class TestCommandPush(AbstractBDWPTestCase):
    
    # before each function
    def setUp(self):
        bdwp_instance.create_folder(test_support_instance.get_mock_cloud_vpath())
        file_support.create_local_folder(test_support_instance.get_mock_local_vpath())

    def test_command_pus_online_original(self):
        txt_file_list = ["/l_1.txt", "/lf_1/l_2.txt", "/lf_2/lf_22/l_3.txt"]
        png_file_list = ["/c_1.png", "/cf_1/c_2.png", "/cf_2/cf_22/c_3.png"]
        prepare_push(Mode.ORIGINAL, txt_file_list, png_file_list)
        command_push.command_push(offline=False)
        verify_action_result(
            local_file_list=txt_file_list,
            cloud_file_list=txt_file_list,
            local_trash_list=[],
            cloud_trash_list=txt_file_list,
            buffer_file_list=[],
            success_log_length=6
        )

    def test_command_pus_offline_original(self):
        txt_file_list = ["/l_1.txt", "/lf_1/l_2.txt", "/lf_2/lf_22/l_3.txt"]
        png_file_list = ["/c_1.png", "/cf_1/c_2.png", "/cf_2/cf_22/c_3.png"]
        prepare_push(Mode.ORIGINAL, txt_file_list, png_file_list)
        remote_json_content = {
            "637772eb0c3dc923a5fe1a5bc7c1fae9": {"middle_path": "/c_1.png", "size": 1048576},
            "1c32dc70c6f1f445b7422d2e72d1c575": {"middle_path": "/cf_1/c_2.png", "size": 1048576},
            "0497a49c66bf337994c3b9afdddd0bc3": {"middle_path": "/cf_2/cf_22/c_3.png", "size": 1048576 }
        }
        file_support.real_write_json_file(fgit_instance.get_cloud_index_file_vpath(test_support_instance.get_mock_local_vpath()), remote_json_content)
        command_push.command_push(offline=True)
        verify_action_result(
            local_file_list=txt_file_list,
            cloud_file_list=txt_file_list,
            local_trash_list=[],
            cloud_trash_list=txt_file_list,
            buffer_file_list=[],
            success_log_length=6
        )

    def test_command_pus_online_encrypted(self):
        txt_file_list = ["/l_1.txt", "/lf_1/l_2.txt", "/lf_2/lf_22/l_3.txt"]
        encrypted_txt_file_list = ["/bF8xLnR4dA==", "/bGZfMQ==/bF8yLnR4dA==", "/bGZfMg==/bGZfMjI=/bF8zLnR4dA=="]
        png_file_list = ["/c_1.png", "/cf_1/c_2.png", "/cf_2/cf_22/c_3.png"]
        prepare_push(Mode.ENCRYPTED, txt_file_list, png_file_list)
        command_push.command_push(offline=False)
        verify_action_result(
            local_file_list=txt_file_list,
            cloud_file_list=encrypted_txt_file_list,
            local_trash_list=[],
            cloud_trash_list=txt_file_list,
            buffer_file_list=[],
            success_log_length=6
        )

    def test_command_pus_offline_encrypted(self):
        txt_file_list = ["/l_1.txt", "/lf_1/l_2.txt", "/lf_2/lf_22/l_3.txt"]
        encrypted_txt_file_list = ["/bF8xLnR4dA==", "/bGZfMQ==/bF8yLnR4dA==", "/bGZfMg==/bGZfMjI=/bF8zLnR4dA=="]
        png_file_list = ["/c_1.png", "/cf_1/c_2.png", "/cf_2/cf_22/c_3.png"]
        prepare_push(Mode.ENCRYPTED, txt_file_list, png_file_list)
        remote_json_content = {
            "637772eb0c3dc923a5fe1a5bc7c1fae9": {"middle_path": "/Y18xLnBuZw==", "size": 1048576},
            "1c32dc70c6f1f445b7422d2e72d1c575": {"middle_path": "/Y2ZfMQ==/Y18yLnBuZw==", "size": 1048576},
            "0497a49c66bf337994c3b9afdddd0bc3": {"middle_path": "/Y2ZfMg==/Y2ZfMjI=/Y18zLnBuZw==", "size": 1048576 }
        }
        file_support.real_write_json_file(fgit_instance.get_cloud_index_file_vpath(test_support_instance.get_mock_local_vpath()), remote_json_content)
        command_push.command_push(offline=True)
        verify_action_result(
            local_file_list=txt_file_list,
            cloud_file_list=encrypted_txt_file_list,
            local_trash_list=[],
            cloud_trash_list=txt_file_list,
            buffer_file_list=[],
            success_log_length=6
        )

    # after each function
    def tearDown(self):
        bdwp_instance.delete_file_folder(test_support_instance.get_mock_cloud_vpath())
        file_support.real_delete_local_path(test_support_instance.get_mock_local_vpath())


def prepare_push(mode:Mode, txt_file_list, png_file_list):
    # local path: ./uttest/tmp/local/test_fgit
    # cloud path: ./uttest/tmp/cloud/test_fgit
    command_init(mode=mode, local_vpath=test_support_instance.get_mock_local_vpath(), remote_vpath=test_support_instance.get_mock_cloud_vpath())
    for txt_file in txt_file_list:
        test_support_instance.create_file('txt', "local", txt_file, mode)
    for png_file in png_file_list:
        test_support_instance.create_file('png', "cloud", png_file, mode)

def verify_action_result(local_file_list=[], cloud_file_list=[], local_trash_list=[], cloud_trash_list=[], buffer_file_list=[], success_log_length=0):
    # verify cloud files
    cloud_file_meta_list = index_facade.get_cloud_index(test_support_instance.get_mock_cloud_vpath())
    cloud_files_path_list = [value[QueueItem.KEY_MIDDLE_PATH] for value in cloud_file_meta_list.values()]
    logger_instance.log_debug("file in cloud", str(cloud_files_path_list))
    assert len(cloud_file_meta_list) == len(cloud_file_list)
    for txt_file in cloud_file_list:
        assert txt_file in cloud_files_path_list

    # verify local files
    local_file_meta_list = index_facade.get_local_index(test_support_instance.get_mock_local_vpath())
    local_files_path_list = [value[QueueItem.KEY_MIDDLE_PATH] for value in local_file_meta_list.values()]
    logger_instance.log_debug("file in local", str(local_files_path_list))
    assert len(local_file_meta_list) == len(local_file_list)
    for txt_file in local_file_list:
        assert txt_file in local_files_path_list

    # verify local trash
    local_trash_folder_vpath = test_support_instance.get_local_trash_folder_vpath()
    local_trash_file_meta_fist = index_facade.get_local_index(local_trash_folder_vpath)
    assert len(local_trash_file_meta_fist) == len(local_trash_list)
    # verify buffer folder
    local_buffer_folder_vpath = test_support_instance.get_local_buffer_folder_vpath()
    local_buffer_file_meta_fist = index_facade.get_local_index(local_buffer_folder_vpath)
    assert len(local_buffer_file_meta_fist) == len(buffer_file_list)
    # verify cloud trash
    cloud_trash_folder_vpath = test_support_instance.get_cloud_trash_folder_vpath()
    cloud_trash_file_meta_fist = test_support.list_file_recursion_with_hidden(cloud_trash_folder_vpath)
    logger_instance.log_debug("file in cloud trash",  str(cloud_trash_file_meta_fist))
    assert len(cloud_trash_file_meta_fist) == len(cloud_trash_list)
        
    # verify message queue
    assert queue_instance.is_lock() == False 
    assert queue_instance.is_queue_empty() == True

    # assert log file
    assert file_support.is_local_exist(logger_instance.get_log_error_file_vpath()) == False
    assert test_support.count_lines_in_file(logger_instance.get_log_success_file_vpath()) == success_log_length


'''
[DEBUG] 2025-03-01 19:15:18 test_command_push.py.verify_action_result file in cloud  ['/YkY4eExuUjRkQT09', '/YkdaZk1RPT0=/YkY4eUxuUjRkQT09', '/YkdaZk1nPT0=/YkdaZk1qST0=/YkY4ekxuUjRkQT09']
[DEBUG] 2025-03-01 19:15:18 test_command_push.py.verify_action_result file in local  ['/bF8xLnR4dA==', '/bGZfMg==/bGZfMjI=/bF8zLnR4dA==', '/bGZfMQ==/bF8yLnR4dA==']
'''