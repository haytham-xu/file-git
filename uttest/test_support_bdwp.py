
import os
import unittest

from service import buffer_service
from service import file_service
from model.config import Mode
from support.bdwp_support import bdwp_instance
from support import file_support
from uttest import test_support

fgit_password = "default_password"
fgit_access_token = os.getenv("BDWP_ACCESS_TOKEN", "")

cloud_test_folder_name = "test_fgit"
cloud_test_root_vpath = file_support.merge_vpath("apps", "sync-assistant")
local_test_root_folder_vpath = file_support.merge_vpath(file_support.get_current_vpath(), "uttest", cloud_test_folder_name)
# .buffer_folder_vpath
local_buffer_folder_vpath = file_support.merge_vpath(local_test_root_folder_vpath, "fgit", "buffer")
cloud_test_folder_root_vpath = file_support.merge_vpath(cloud_test_root_vpath, cloud_test_folder_name)

test_file_txt_1_middle_vpath = "test_1.txt"
test_file_txt_1_local_vpath = file_support.merge_vpath(local_test_root_folder_vpath, test_file_txt_1_middle_vpath)
test_file_txt_1_cloud_vpath = file_support.merge_vpath(cloud_test_folder_root_vpath, test_file_txt_1_middle_vpath)

test_file_txt_2_middle_vpath = "folder1/test_2.txt"
test_file_txt_2_local_vpath = file_support.merge_vpath(local_test_root_folder_vpath, test_file_txt_2_middle_vpath)
test_file_txt_2_cloud_vpath = file_support.merge_vpath(cloud_test_folder_root_vpath, test_file_txt_2_middle_vpath)

test_file_txt_3_middle_vpath = "folder2/folder22/test_3.txt"
test_file_txt_3_local_vpath = file_support.merge_vpath(local_test_root_folder_vpath, test_file_txt_3_middle_vpath)
test_file_txt_3_cloud_vpath = file_support.merge_vpath(cloud_test_folder_root_vpath, test_file_txt_3_middle_vpath)

test_file_png_1_middle_vpath = "test_1.png"
test_file_png_1_local_vpath = file_support.merge_vpath(local_test_root_folder_vpath, test_file_png_1_middle_vpath)
test_file_png_1_cloud_vpath = file_support.merge_vpath(cloud_test_folder_root_vpath, test_file_png_1_middle_vpath)

test_file_png_2_middle_vpath = "folder1/test_2.png"
test_file_png_2_local_vpath = file_support.merge_vpath(local_test_root_folder_vpath, test_file_png_2_middle_vpath)
test_file_png_2_cloud_vpath = file_support.merge_vpath(cloud_test_folder_root_vpath, test_file_png_2_middle_vpath)

test_file_png_3_middle_vpath = "folder2/folder22/test_3.png"
test_file_png_3_local_vpath = file_support.merge_vpath(local_test_root_folder_vpath, test_file_png_3_middle_vpath)
test_file_png_3_cloud_vpath = file_support.merge_vpath(cloud_test_folder_root_vpath, test_file_png_3_middle_vpath)

# TODO need a path for chunk, and those test file path should move to class test_suppprt.

# python3 -m unittest uttest.test_support_bdwp.TestBaiduWangpan -v -f
# python3 -m unittest uttest.test_support_bdwp.TestBaiduWangpan.test_create_folder -v -f
class TestBaiduWangpan(unittest.TestCase):

    # before each function
    def setUp(self):
        bdwp_instance.set_access_token(fgit_access_token)
        bdwp_instance.create_folder(cloud_test_folder_root_vpath)
        file_support.create_local_folder(local_test_root_folder_vpath)
    
    def test_create_folder(self):
        # test create folder(in setUp)
        # verify create folder.(also test for search folder)
        assert bdwp_instance.check_folder_exists(cloud_test_folder_name, cloud_test_root_vpath) == True
        # test delete folder(in tearDown)
    
    def test_upload_file(self):
        # test upload file
        create_file_in_remote(test_file_txt_1_local_vpath, test_file_txt_1_cloud_vpath, "txt")
        # verify upload file
        assert bdwp_instance.check_folder_exists(test_file_txt_1_middle_vpath, cloud_test_folder_root_vpath) == True
        res = bdwp_instance.delete_file_folder(test_file_txt_1_cloud_vpath)
        assert res["errno"] == 0

    def test_download_file(self):
        create_file_in_remote(test_file_txt_1_local_vpath, test_file_txt_1_cloud_vpath, "txt")
        file_support.real_delete_local_path(test_file_txt_1_local_vpath)
        assert file_support.is_local_exist(test_file_txt_1_local_vpath) == False
        bdwp_instance.download_file_with_path(test_file_txt_1_cloud_vpath, test_file_txt_1_local_vpath)
        # verify download file
        assert file_support.is_local_exist(test_file_txt_1_local_vpath) == True

    def test_move_file(self):
        # test move file
        create_file_in_remote(test_file_txt_1_local_vpath, test_file_txt_1_cloud_vpath, "txt")
        move_parent_path = file_support.merge_vpath(cloud_test_folder_root_vpath, "move")
        bdwp_instance.move_file_folder(test_file_txt_1_cloud_vpath, move_parent_path)
        # verify move result
        assert bdwp_instance.check_folder_exists(test_file_txt_1_middle_vpath, move_parent_path) == True

    def test_list_folder_file_recursion(self):
        create_file_in_remote(test_file_txt_1_local_vpath, test_file_txt_1_cloud_vpath, "txt")
        create_file_in_remote(test_file_txt_2_local_vpath, test_file_txt_2_cloud_vpath, "txt")
        create_file_in_remote(test_file_txt_3_local_vpath, test_file_txt_3_cloud_vpath, "txt")
        create_file_in_remote(test_file_png_1_local_vpath, test_file_png_1_cloud_vpath, "png")
        create_file_in_remote(test_file_png_2_local_vpath, test_file_png_2_cloud_vpath, "png")
        create_file_in_remote(test_file_png_3_local_vpath, test_file_png_3_cloud_vpath, "png")
        
        folder_list, file_list = bdwp_instance.list_file_recursion(cloud_test_folder_root_vpath)

        assert len(folder_list) == 3
        assert len(file_list) == 6

    # after each function
    def tearDown(self):
        file_support.real_delete_local_path(local_test_root_folder_vpath)
        bdwp_instance.delete_file_folder(cloud_test_folder_root_vpath)

def create_file_in_remote(local_file_vpath, cloud_file_vpath, file_type):
    if file_type == 'txt':
        test_support.create_file(1, local_file_vpath)
    elif file_type == 'png':
        test_support.create_image(1, local_file_vpath)
    else:
        raise ValueError("Unsupported file type")
    
    file_middle_vpath = local_file_vpath.removeprefix(local_test_root_folder_vpath)
    file_vpath_in_local = file_support.merge_vpath(local_test_root_folder_vpath, file_middle_vpath)
    file_vpath_in_buffer = file_support.merge_vpath(local_buffer_folder_vpath, buffer_service.get_buffer_cloud_middle_path_base_mode(file_middle_vpath))

    file_vpath_in_remote = file_support.merge_vpath(cloud_test_folder_root_vpath, file_middle_vpath)
    buffer_service.move_to_buffer(file_vpath_in_local, local_test_root_folder_vpath, local_buffer_folder_vpath, Mode.ORIGINAL, fgit_password)
    file_service.upload_file(file_vpath_in_buffer, file_vpath_in_remote)
    buffer_service.post_move_to_buffer(file_vpath_in_buffer)
    file_support.real_delete_local_path(local_file_vpath)
