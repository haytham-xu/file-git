
from uttest.abstract_test import AbstractTestCase
from support.bdwp_support import bdwp_instance
from support.config_support import config_instance
from support.constant_support import constant_instance
from support import file_support
from uttest import test_support

class TestBaiduWangpan(AbstractTestCase):

    # before each function
    def setUp(self):
        bdwp_instance.set_access_token(test_support.fgit_access_token)
        config_instance.set_local_path(test_support.local_test_root_folder)
        config_instance.set_remote_path(test_support.cloud_test_folder_root_path)
        constant_instance.set_local_path(test_support.local_test_root_folder)
        bdwp_instance.create_folder(test_support.cloud_test_folder_root_path)
        file_support.create_folder(test_support.local_test_root_folder)

    def test_create_folder(self):
        # test create folder(in setUp)
        # verify create folder.(also test for search folder)
        res = bdwp_instance.search_file(test_support.cloud_test_folder_name, test_support.cloud_test_root_path)
        assert res["errno"] == 0
        assert len(res["list"]) == 1
        assert res["list"][0]["isdir"] == 1
        # test delete folder(in tearDown)
    
    def test_upload_file(self):
        # test upload file
        test_support.create_file_in_remote(test_support.test_file_txt_1_local_path, test_support.test_file_txt_1_cloud_path, "txt")
        # verify upload file
        res = bdwp_instance.search_file(test_support.test_file_txt_1_middle_path, test_support.cloud_test_folder_root_path)
        assert res["errno"] == 0
        assert len(res["list"]) == 1
        assert res["list"][0]["isdir"] == 0    
        # test delete file
        res = bdwp_instance.delete_file_folder(test_support.test_file_txt_1_cloud_path)
        assert res["errno"] == 0

    def test_download_file(self):
        test_support.create_file_in_remote(test_support.test_file_txt_1_local_path, test_support.test_file_txt_1_cloud_path, "txt")
        file_support.delete_path(test_support.test_file_txt_1_local_path)
        assert file_support.is_exist(test_support.test_file_txt_1_local_path) == False
        bdwp_instance.download_file_with_path(test_support.test_file_txt_1_cloud_path, test_support.test_file_txt_1_local_path)
        # verify download file
        assert file_support.is_exist(test_support.test_file_txt_1_local_path) == True

    def test_move_file(self):
        # test move file
        test_support.create_file_in_remote(test_support.test_file_txt_1_local_path, test_support.test_file_txt_1_cloud_path, "txt")
        move_parent_path = file_support.merge_path(test_support.cloud_test_folder_root_path, "move")
        bdwp_instance.move_file_folder(test_support.test_file_txt_1_cloud_path, move_parent_path)
        # verify move result
        res = bdwp_instance.search_file(test_support.test_file_txt_1_middle_path, move_parent_path)
        assert res["errno"] == 0
        assert len(res["list"]) == 1
        assert res["list"][0]["isdir"] == 0

    def test_list_folder_file_recursion(self):
        test_support.create_file_in_remote(test_support.test_file_txt_1_local_path, test_support.test_file_txt_1_cloud_path, "txt")
        test_support.create_file_in_remote(test_support.test_file_txt_2_local_path, test_support.test_file_txt_2_cloud_path, "txt")
        test_support.create_file_in_remote(test_support.test_file_txt_3_local_path, test_support.test_file_txt_3_cloud_path, "txt")
        test_support.create_file_in_remote(test_support.test_file_png_1_local_path, test_support.test_file_png_1_cloud_path, "png")
        test_support.create_file_in_remote(test_support.test_file_png_2_local_path, test_support.test_file_png_2_cloud_path, "png")
        test_support.create_file_in_remote(test_support.test_file_png_3_local_path, test_support.test_file_png_3_cloud_path, "png")
        
        folder_list, file_list = bdwp_instance.list_folder_file_recursion(test_support.cloud_test_folder_root_path)
        assert len(folder_list) == 3
        assert len(file_list) == 6

    # after each function
    def tearDown(self):
        file_support.delete_path(test_support.local_test_root_folder)
        bdwp_instance.delete_file_folder(test_support.cloud_test_folder_root_path)

