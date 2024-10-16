
from uttest.abstract_test import AbstractTestCase
from support.bdwp_support import bdwp_instance
from support import file_support
from uttest import test_support

class TestBaiduWangpan(AbstractTestCase):

    # before each function
    def setUp(self):
        bdwp_instance.set_access_token(test_support.fgit_access_token)
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
        create_txt_and_upload(test_support.test_file_name)
        # verify upload file
        res = bdwp_instance.search_file(test_support.test_file_name, test_support.cloud_test_folder_root_path)
        assert res["errno"] == 0
        assert len(res["list"]) == 1
        assert res["list"][0]["isdir"] == 0    
        # test delete file
        res = bdwp_instance.delete_file_folder(test_support.test_file_cloud_path)
        assert res["errno"] == 0

    def test_download_file(self):
        create_txt_and_upload(test_support.test_file_name)
        file_support.delete_path(test_support.test_file_local_path)
        assert file_support.is_exist(test_support.test_file_local_path) == False
        bdwp_instance.download_file_with_path(test_support.test_file_cloud_path, test_support.test_file_local_path)
        # verify download file
        assert file_support.is_exist(test_support.test_file_local_path) == True

    def test_move_file(self):
        # test move file
        create_txt_and_upload(test_support.test_file_name)
        move_parent_path = file_support.merge_path(test_support.cloud_test_folder_root_path, "move")
        bdwp_instance.move_file_folder(test_support.test_file_cloud_path, move_parent_path)
        # verify move result
        res = bdwp_instance.search_file(test_support.test_file_name, move_parent_path)
        assert res["errno"] == 0
        assert len(res["list"]) == 1
        assert res["list"][0]["isdir"] == 0

    def test_list_folder_file_recursion(self):
        create_txt_and_upload("test_1.txt")
        create_png_and_upload("test_1.png")
        file_support.create_folder(file_support.merge_path(test_support.local_test_root_folder, "level1"))
        create_txt_and_upload("level1/test_2.txt")
        create_png_and_upload("level1/test_2.png")
        file_support.create_folder(file_support.merge_path(test_support.local_test_root_folder, "level1/level2"))
        create_txt_and_upload("level1/level2/test_3.txt")
        create_png_and_upload("level1/level2/test_3.png")
        
        folder_list, file_list = bdwp_instance.list_folder_file_recursion(test_support.cloud_test_folder_root_path)
        assert len(folder_list) == 2
        assert len(file_list) == 6

    # after each function
    def tearDown(self):
        file_support.delete_path(test_support.local_test_root_folder)
        bdwp_instance.delete_file_folder(test_support.cloud_test_folder_root_path)

def create_txt_and_upload(middle_path):
    local_file_path = file_support.merge_path(test_support.local_test_root_folder, middle_path)
    clooud_file_path = file_support.merge_path(test_support.cloud_test_folder_root_path, middle_path)
    test_support.create_file(1, local_file_path)
    res = bdwp_instance.upload_file(local_file_path, clooud_file_path)
    assert res !=0

def create_png_and_upload(middle_path):
    local_file_path = file_support.merge_path(test_support.local_test_root_folder, middle_path)
    clooud_file_path = file_support.merge_path(test_support.cloud_test_folder_root_path, middle_path)
    test_support.create_image(1, local_file_path)
    res = bdwp_instance.upload_file(local_file_path, clooud_file_path)
    assert res !=0
