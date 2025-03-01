
import os
import unittest
from support import file_support
from support.bdwp_support import BaiduWangPan
from uttest import test_support
from uttest.test_support import test_support_instance
from unittest.mock import patch, MagicMock
from support.bdwp_support import bdwp_instance

class AbstractBDWPTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        '''
        ./uttest/tmp/
            |__local/test_fgit/
            |__cloud/test_fgit/
        '''
        # stubbing, set test current path to ./uttest/tmp/local/test_fgit
        mock_current_path = file_support.merge_vpath(os.getcwd(), "uttest", "tmp", "local", "test_fgit")
        cls.patcher_getcwd = patch('os.getcwd', return_value=mock_current_path)
        # Cloud method stubbing statement.
        cls.patcher_download_file_with_path = patch.object(BaiduWangPan, 'download_file_with_path', side_effect=fake_download_file_with_path)
        cls.patcher_upload_file = patch.object(BaiduWangPan, 'upload_file', side_effect=fake_upload_file)
        cls.patcher_move_file_folder = patch.object(BaiduWangPan, 'move_file_folder', side_effect=fake_move_file_folder)
        cls.patcher_list_file_recursion = patch.object(BaiduWangPan, 'list_file_recursion', side_effect=fake_list_file_recursion)
        cls.patcher_create_folder = patch.object(BaiduWangPan, 'create_folder', side_effect=fake_create_folder)
        cls.patcher_delete_file_folder = patch.object(BaiduWangPan, 'delete_file_folder', side_effect=fake_delete_file_folder)
        
        cls.mock_download_file_with_path = cls.patcher_download_file_with_path.start()
        cls.mock_upload_file = cls.patcher_upload_file.start()
        cls.mock_move_file_folder = cls.patcher_move_file_folder.start()
        cls.mock_list_file_recursion = cls.patcher_list_file_recursion.start()
        cls.mock_create_folder = cls.patcher_create_folder.start()
        cls.mock_delete_file_folder = cls.patcher_delete_file_folder.start()
        cls.mock_getcwd = cls.patcher_getcwd.start()
        # create temp test folder: ./uttest/tmp/
        file_support.create_local_folder(test_support_instance.mock_tmp_vpath)

    @classmethod 
    def tearDownClass(cls):
        # Stop Cloud method stubbing
        cls.patcher_download_file_with_path.stop()
        cls.patcher_upload_file.stop()
        cls.patcher_move_file_folder.stop()
        cls.patcher_list_file_recursion.stop()
        cls.patcher_create_folder.stop()
        cls.patcher_delete_file_folder.stop()
        cls.patcher_getcwd.stop()
        # delete temp test folder: ./uttest/tmp/
        file_support.real_delete_local_path(test_support_instance.mock_tmp_vpath)

def fake_create_folder(cloud_folder_vpath):
    file_support.create_local_folder(cloud_folder_vpath)

def fake_delete_file_folder(cloud_folder_vpath):
    file_support.real_delete_local_path(cloud_folder_vpath)

def fake_download_file_with_path(cloud_download_abs_rpath, local_download_abs_rpath):
    print("Fake download file with path, end here!")

def fake_upload_file(local_upload_abs_rpath, cloud_upload_abs_rpath):
    file_support.real_move_file_folder(local_upload_abs_rpath, cloud_upload_abs_rpath)

def fake_move_file_folder(cloud_source_file_rpath, cloud_target_folder_rpath):
    file_support.create_local_folder(cloud_target_folder_rpath)
    filename = cloud_source_file_rpath.split(os.sep)[-1]
    file_target_vpath = file_support.merge_vpath(cloud_target_folder_rpath, filename)
    file_support.real_move_file_folder(cloud_source_file_rpath, file_target_vpath)

def fake_list_file_recursion(remote_path):
    res = []
    def is_hidden(filepath):
        return any(part.startswith('.') for part in filepath.split(os.sep))
    for root, dirs, files in os.walk(remote_path):
        dirs[:] = [d for d in dirs if not is_hidden(d)]
        for file in files:
            file_path = os.path.join(root, file)
            if is_hidden(file_path):
                continue
            file_size = os.path.getsize(file_path)
            res.append({
                'path': file_path,
                'size': file_size,
                'server_filename': file
            })
    return res
