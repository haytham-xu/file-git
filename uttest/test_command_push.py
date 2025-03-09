
from command import command_push
from model.file_git import fgit_instance
from model.config import Mode
from support import file_support
from support.bdwp_support import bdwp_instance

from uttest.abstract_test import AbstractBDWPTestCase
from uttest.test_support import test_support_instance
from uttest.test_support import get_path_hash, get_encrypted, verify_action_result, prepare_action

# python3 -m unittest uttest.test_command_push.TestCommandPush -v -f
class TestCommandPush(AbstractBDWPTestCase):
    
    # before each function
    def setUp(self):
        bdwp_instance.create_folder(test_support_instance.get_mock_cloud_vpath())
        file_support.create_local_folder(test_support_instance.get_mock_local_vpath())

    # python3 -m unittest uttest.test_command_push.TestCommandPush.test_command_push_online_original -v -f
    def test_command_push_online_original(self):
        txt_file_list = ["/l_1.txt", "/lf_1/l_2.txt", "/lf_2/lf_22/l_3.txt"]
        png_file_list = ["/c_1.png", "/cf_1/c_2.png", "/cf_2/cf_22/c_3.png"]
        prepare_action(Mode.ORIGINAL, txt_file_list, png_file_list)
        command_push.command_push(offline=False)
        verify_action_result(
            local_file_list=txt_file_list,
            cloud_file_list=txt_file_list,
            local_trash_list=[],
            cloud_trash_list=txt_file_list,
            buffer_file_list=[],
            success_log_length=6
        )

    # python3 -m unittest uttest.test_command_push.TestCommandPush.test_command_push_offline_original -v -f
    def test_command_push_offline_original(self):
        txt_file_list = ["/l_1.txt", "/lf_1/l_2.txt", "/lf_2/lf_22/l_3.txt"]
        png_file_list = ["/c_1.png", "/cf_1/c_2.png", "/cf_2/cf_22/c_3.png"]
        prepare_action(Mode.ORIGINAL, txt_file_list, png_file_list)
        remote_json_content = {
            get_path_hash("/c_1.png"): {"middle_path": "/c_1.png", "size": 1048576},
            get_path_hash("/cf_1/c_2.png"): {"middle_path": "/cf_1/c_2.png", "size": 1048576},
            get_path_hash("/cf_2/cf_22/c_3.png"): {"middle_path": "/cf_2/cf_22/c_3.png", "size": 1048576 }
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

    # python3 -m unittest uttest.test_command_push.TestCommandPush.test_command_push_online_encrypted -v -f
    def test_command_push_online_encrypted(self):
        txt_file_list = ["/l_1.txt", "/lf_1/l_2.txt", "/lf_2/lf_22/l_3.txt"]
        encrypted_txt_file_list = [get_encrypted("/l_1.txt"),get_encrypted( "/lf_1/l_2.txt"), get_encrypted("/lf_2/lf_22/l_3.txt")]
        png_file_list = ["/c_1.png", "/cf_1/c_2.png", "/cf_2/cf_22/c_3.png"]
        prepare_action(Mode.ENCRYPTED, txt_file_list, png_file_list)
        command_push.command_push(offline=False)
        verify_action_result(
            local_file_list=txt_file_list,
            cloud_file_list=encrypted_txt_file_list,
            local_trash_list=[],
            cloud_trash_list=txt_file_list,
            buffer_file_list=[],
            success_log_length=6
        )

    # python3 -m unittest uttest.test_command_push.TestCommandPush.test_command_push_offline_encrypted -v -f
    def test_command_push_offline_encrypted(self):
        txt_file_list = ["/l_1.txt", "/lf_1/l_2.txt", "/lf_2/lf_22/l_3.txt"]
        encrypted_txt_file_list = [get_encrypted("/l_1.txt"),get_encrypted( "/lf_1/l_2.txt"), get_encrypted("/lf_2/lf_22/l_3.txt")]
        png_file_list = ["/c_1.png", "/cf_1/c_2.png", "/cf_2/cf_22/c_3.png"]
        prepare_action(Mode.ENCRYPTED, txt_file_list, png_file_list)
        remote_json_content = {
            get_path_hash("/c_1.png"): {"middle_path": get_encrypted("/c_1.png"), "size": 1048576},
            get_path_hash("/cf_1/c_2.png"): {"middle_path": get_encrypted("/cf_1/c_2.png"), "size": 1048576},
            get_path_hash("/cf_2/cf_22/c_3.png"): {"middle_path": get_encrypted("/cf_2/cf_22/c_3.png"), "size": 1048576 }
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

