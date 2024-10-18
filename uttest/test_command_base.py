
from uttest.abstract_test import AbstractTestCase
from unittest.mock import patch

from uttest import test_support
from hook.hook import Hooks
from command.command_set_config import command_set_config
from support.config_support import config_instance
from support.config_support import Mode
from support import file_support
from support.constant_support import constant_instance

class TestCommandBase(AbstractTestCase):

    # before each function
    def setUp(self):
        file_support.create_folder(test_support.local_test_root_folder)

    # init
    @patch('os.getcwd')
    def test_init(self, mock_getcwd):
        # mocking
        mock_getcwd.return_value = test_support.local_test_root_folder
        # prepare
        # execute
        test_support.run_command_init(test_support.original_fgit_mode)
        # assert
        assert file_support.is_exist(constant_instance.get_file_git_folder_path())
        assert file_support.is_exist(constant_instance.get_trash_folder_path())
        assert file_support.is_exist(constant_instance.get_action_folder_path())
        assert file_support.is_exist(constant_instance.get_queue_file_path())
        assert file_support.is_exist(constant_instance.get_config_file_path())

        config_instance.read_config(constant_instance.get_config_file_path())
        assert config_instance.get_mode() == Mode.ORIGINAL
        assert config_instance.get_password() == test_support.fgit_password
        assert config_instance.get_local_path() == test_support.fgit_local_path
        assert config_instance.get_remote_path() == test_support.fgit_remote_path
        assert config_instance.get_app_id() == test_support.fgit_app_id
        assert config_instance.get_secret_key() == test_support.fgit_secret_key
        assert config_instance.get_app_key() == test_support.fgit_app_key
        assert config_instance.get_sign_code() == test_support.fgit_sign_code
        assert config_instance.get_expires_in() == test_support.fgit_expires_in
        assert config_instance.get_refresh_token() == test_support.fgit_refresh_token
        assert config_instance.get_access_token() == test_support.fgit_access_token

    # set-config_instance.
    @patch('os.getcwd')
    def test_set_config(self, mock_getcwd):
        # mocking
        mock_getcwd.return_value = test_support.local_test_root_folder
        # prepare
        test_support.run_command_init(test_support.original_fgit_mode)
        test_config_key = "access_token"
        test_config_value = "new_access_token"
        # execute
        Hooks.base_hook()
        command_set_config(test_config_key, test_config_value)
        # assert
        config_instance.read_config(constant_instance.get_config_file_path())
        assert config_instance.get_access_token() == test_config_value

    # after each function
    def tearDown(self):
        file_support.delete_path(test_support.local_test_root_folder)
        

