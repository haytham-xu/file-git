
from uttest.abstract_test import AbstractBDWPTestCase
from unittest.mock import patch

from uttest import test_support
from hook.hook import Hooks
from command.command_set_config import command_set_config
from model.config import FilegitConfig
from model.config import Mode
from support import file_support
from model import constant


class TestCommandBase(AbstractBDWPTestCase):

    # before each function
    def setUp(self):
        file_support.create_local_folder(test_support.test_support_instance.get_mock_local_vpath())

    # init
    @patch('os.getcwd')
    def test_init(self, mock_getcwd):
        pass
        # mocking
        # mock_getcwd.return_value = test_support.mock_local_test_vpath
        # # prepare
        # # execute
        # test_support.run_command_init(test_support.original_fgit_mode)
        # # assert
        # assert file_support.is_local_exist(FilegitConstant.fgit_folder_vpath)
        # assert file_support.is_local_exist(FilegitConstant.trash_folder_vpath)
        # assert file_support.is_local_exist(FilegitConstant.action_folder_vpath)
        # assert file_support.is_local_exist(constant.QUEUE_FILE_VPATH)
        # assert file_support.is_local_exist(FilegitConstant.config_folder_vpath)

        # FilegitConfig.init(FilegitConstant.config_folder_vpath)
        # assert FilegitConfig.get_mode() == Mode.ORIGINAL
        # assert FilegitConfig.get_password() == test_support.fgit_password
        # assert FilegitConfig.get_local_vpath() == test_support.fgit_local_vpath
        # assert FilegitConfig.get_remote_vpath() == test_support.fgit_remote_vpath
        # assert FilegitConfig.get_app_id() == test_support.fgit_app_id
        # assert FilegitConfig.get_secret_key() == test_support.fgit_secret_key
        # assert FilegitConfig.get_app_key() == test_support.fgit_app_key
        # assert FilegitConfig.get_sign_code() == test_support.fgit_sign_code
        # assert FilegitConfig.get_expires_in() == test_support.fgit_expires_in
        # assert FilegitConfig.get_refresh_token() == test_support.fgit_refresh_token
        # assert FilegitConfig.get_access_token() == test_support.fgit_access_token

    # set-config_instance.
    @patch('os.getcwd')
    def test_set_config(self, mock_getcwd):
        # mocking
        mock_getcwd.return_value = test_support.test_support_instance.get_mock_local_vpath()
        # prepare
        test_support.run_command_init(test_support.TestSupport.original_fgit_mode)
        test_config_key = "access_token"
        test_config_value = "new_access_token"
        # execute
        Hooks.base_hook()
        command_set_config(test_config_key, test_config_value)
        # assert
        FilegitConfig.init(FilegitConstant.config_folder_vpath)
        assert FilegitConfig.get_access_token() == test_config_value

    # after each function
    def tearDown(self):
        file_support.real_delete_local_path(test_support.test_support_instance.get_mock_local_vpath())
        

