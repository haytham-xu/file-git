
import os
import string
from PIL import Image

from command.command_init import command_init
from facade import index_facade
from facade.queue_facade import queue_instance
from model.config import Mode
from model.queue import QueueItem
from model.logger import logger_instance
from support import encrypt_support
from support import file_support

class TestSupport():
    fgit_password = "default_password"
    test_folder_name = "test_fgit"
    mock_tmp_vpath = os.getcwd() + "/uttest/tmp"

    def get_mock_cloud_vpath(self):
        return TestSupport.mock_tmp_vpath + file_support.merge_vpath("cloud", TestSupport.test_folder_name)
    def get_mock_local_vpath(self):
        return file_support.merge_vpath(file_support.get_current_vpath())
    def get_local_buffer_folder_vpath(self):
        return file_support.merge_vpath(self.get_mock_local_vpath(), ".fgit", "buffer")
    def get_local_trash_folder_vpath(self):
        return file_support.merge_vpath(self.get_mock_local_vpath(), ".fgit", "trash")
    def get_cloud_trash_folder_vpath(self):
        return file_support.merge_vpath(self.get_mock_cloud_vpath(), ".trash")
    
    def create_file(self, type, localtion, file_middle_vpath, mode:Mode):
        # local uncrypted -> uncrypted
        # cloud uncrypted -> uncrypted
        # local encrypted -> uncrypted
        # cloud encrypted -> encrypted
        base_vpath = ""
        if "cloud" == localtion:
            base_vpath = self.get_mock_cloud_vpath()
        else: 
            base_vpath = self.get_mock_local_vpath()
        final_file_middle_vpath = file_middle_vpath
        if mode == Mode.ENCRYPTED and "cloud" == localtion:
            final_file_middle_vpath = encrypt_support.encode_path(file_middle_vpath)
        file_output_vpath = file_support.merge_vpath(base_vpath, final_file_middle_vpath)
        logger_instance.log_debug("creating in {}: {}".format(localtion, file_middle_vpath))
        if "png" == type:
            create_image(1, file_output_vpath, mode, localtion)
        else:
            create_file(1, file_output_vpath, mode, localtion)
    
test_support_instance = TestSupport()

def list_file_recursion_with_hidden(root_path):
    res = []
    for root, _, files in os.walk(root_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            res.append({
                'path': file_path,
                'size': file_size,
                'server_filename': file
            })
    return res

def create_file(size, output_vpath, mode:Mode, localtion):
    """size is MB, store the file to the output."""
    size_in_bytes = size * 1024 * 1024  # convert MB to bytes
    chars = string.digits + string.ascii_lowercase + string.ascii_uppercase + " "
    repeated_chars = (chars * ((size_in_bytes // len(chars)) + 1))[:size_in_bytes]
    _, virtual_parent_path = file_support.get_file_name_and_parent_vpath(output_vpath)
    file_support.create_local_folder(virtual_parent_path)
    file_support.real_write_file(output_vpath, repeated_chars)
    if mode == Mode.ENCRYPTED and "cloud" == localtion:
        buffer_file_vpath = output_vpath + "_buffer"
        file_support.real_write_file(buffer_file_vpath, repeated_chars)
        encrypt_support.encrypt_file(buffer_file_vpath, output_vpath, TestSupport.fgit_password)
        file_support.real_delete_local_path(buffer_file_vpath)
        logger_instance.log_debug("create encrypted file in cloud", output_vpath)
        return
    logger_instance.log_debug("create unencrypted file", output_vpath)
    file_support.real_write_file(output_vpath, repeated_chars)

def create_image(size, output_vpath, mode:Mode, localtion):
    """Create an image with specified size in MB, and save to output_path."""
    size_in_bytes = size * 1024 * 1024  # convert MB to bytes
    num_pixels = size_in_bytes // 3  # each pixel is 3 bytes (RGB)
    side_length = int(num_pixels ** 0.5)  # assume a square image

    image = Image.new('RGB', (side_length, side_length), color='white')
    for x in range(side_length):
        for y in range(side_length):
            # Create a subtle gradient
            r = int((x / side_length) * 128 + 64)  # range from 64 to 192
            g = int((y / side_length) * 128 + 64)  # range from 64 to 192
            b = 192  # constant value for blue
            image.putpixel((x, y), (r, g, b))
    # Ensure the image size matches the specified size
    _, virtual_parent_path = file_support.get_file_name_and_parent_vpath(output_vpath)
    file_support.create_local_folder(virtual_parent_path)
    if mode == Mode.ENCRYPTED and "cloud" == localtion:
        buffer_file_vpath = output_vpath + "_buffer"
        real_create_png(buffer_file_vpath, image, size_in_bytes)
        encrypt_support.encrypt_file(buffer_file_vpath, output_vpath, TestSupport.fgit_password)
        file_support.real_delete_local_path(buffer_file_vpath)
        logger_instance.log_debug("cloud encrypted png", output_vpath)
        return
    logger_instance.log_debug("unencrypted png", output_vpath)
    real_create_png(output_vpath, image, size_in_bytes)

def real_create_png(output_vpath, image, size_in_bytes):
    file_rpath = file_support.convert_to_rpath(output_vpath)
    with open(file_rpath, 'wb') as f:
        image.save(f, format='PNG')
        current_size = f.tell()
        if current_size < size_in_bytes:
            f.write(b'\0' * (size_in_bytes - current_size))

def count_file(target_vpath):
    target_real_path = file_support.convert_to_rpath(target_vpath)
    file_count = 0
    for _, dirnames, filenames in os.walk(target_real_path):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        visible_files = [f for f in filenames if not f.startswith('.')]
        file_count += len(visible_files)
    return file_count

def count_lines_in_file(file_vpath):
    filet_real_path = file_support.convert_to_rpath(file_vpath)
    line_count = 0
    with open(filet_real_path, 'r') as file:
        for _ in file:
            line_count += 1
    return line_count

def get_path_hash(orginal_path:str):
    return file_support.get_string_hash(orginal_path)

def get_encrypted(orginal_path:str):
    return encrypt_support.encode_path(orginal_path)


def prepare_action(mode:Mode, txt_file_list, png_file_list):
    # local path: ./uttest/tmp/local/test_fgit
    # cloud path: ./uttest/tmp/cloud/test_fgit
    command_init(mode=mode, local_vpath=test_support_instance.get_mock_local_vpath(), remote_vpath=test_support_instance.get_mock_cloud_vpath(), password=TestSupport.fgit_password)
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
    cloud_trash_file_meta_fist = list_file_recursion_with_hidden(cloud_trash_folder_vpath)
    logger_instance.log_debug("file in cloud trash",  str(cloud_trash_file_meta_fist))
    assert len(cloud_trash_file_meta_fist) == len(cloud_trash_list)
        
    # verify message queue
    assert queue_instance.is_lock() == False 
    assert queue_instance.is_queue_empty() == True

    # assert log file
    assert file_support.is_local_exist(logger_instance.get_log_error_file_vpath()) == False
    assert count_lines_in_file(logger_instance.get_log_success_file_vpath()) == success_log_length


