
import os
import string
from PIL import Image
from model.config import Mode

from support import file_support
from support import encrypt_support
from model.logger import logger_instance

'''
["/l_1.txt", "/lf_1/l_2.txt", "/lf_2/lf_22/l_3.txt"]
["/bF8xLnR4dA==", "/bGZfMQ==/bF8yLnR4dA==", "/bGZfMg==/bGZfMjI=/bF8zLnR4dA=="]
["637772eb0c3dc923a5fe1a5bc7c1fae9", "1c32dc70c6f1f445b7422d2e72d1c575", "0497a49c66bf337994c3b9afdddd0bc3"]
["/c_1.png", "/cf_1/c_2.png", "/cf_2/cf_22/c_3.png"]
["/Y18xLnBuZw==", "/Y2ZfMQ==/Y18yLnBuZw==", "/Y2ZfMg==/Y2ZfMjI=/Y18zLnBuZw=="]
["", "", ""]
'''

class TestSupport():
    fgit_password = "default_password"
    test_folder_name = "test_fgit"
    test_file_txt_1_middle_vpath = "test_1.txt"
    test_file_txt_2_middle_vpath = "folder1/test_2.txt"
    test_file_txt_3_middle_vpath = "folder2/folder22/test_3.txt"
    test_file_png_1_middle_vpath = "test_1.png"
    test_file_png_2_middle_vpath = "folder1/test_2.png"
    test_file_png_3_middle_vpath = "folder2/folder22/test_3.png"
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
    # def get_fgit_local_vpath(self):
    #     return self.get_mock_local_vpath()
    # def get_fgit_remote_vpath(self):
    #     return self.get_mock_cloud_vpath()
    # def get_fgit_app_id(self):
    #     return os.getenv("BDWP_APP_ID", "")
    # def get_fgit_secret_key(self):
    #     return os.getenv("BDWP_SECRET_KEY", "")
    # def get_fgit_app_key(self):
    #     return os.getenv("BDWP_APP_KEY", "")
    # def get_fgit_sign_code(self):
    #     return os.getenv("BDWP_SIGN_CODE", "")
    # def get_fgit_expires_in(self):
    #     return os.getenv("BDWP_EXPIRES_IN", "")
    # def get_fgit_refresh_token(self):
    #     return os.getenv("BDWP_REFRESH_TOKEN", "")
    # def get_fgit_access_token(self):
    #     return os.getenv("BDWP_ACCESS_TOKEN", "")
    
    def create_file(self, type, localtion, file_middle_vpath, mode:Mode):
        # local uncrypted -> 不加密
        # cloud uncrypted -> 不加密
        # local encrypted -> 不加密
        # cloud encrypted -> 加密
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
        logger_instance.log_debug("cloud encrypted file", output_vpath)
        return
    logger_instance.log_debug("unencrypted file", output_vpath)
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



# def create_file_in_remote(local_file_vpath, cloud_file_vpath, file_type, mode: Mode = Mode.ORIGINAL):
#     if file_type == 'txt':
#         create_file(1, local_file_vpath)
#     elif file_type == 'png':
#         create_image(1, local_file_vpath)
#     else:
#         raise ValueError("Unsupported file type")
    
#     file_middle_vpath = local_file_vpath.removeprefix(local_test_root_folder_vpath)
#     file_vpath_in_local = file_support.merge_vpath(local_test_root_folder_vpath, file_middle_vpath)
#     file_vpath_in_buffer = buffer_service.get_file_buffer_path(local_buffer_folder_vpath, file_middle_vpath)

#     file_vpath_in_remote = None
#     if mode == Mode.ENCRYPTED:
#         file_vpath_in_remote = file_support.merge_vpath(cloud_test_folder_root_vpath, encrypt_support.encode_path(file_middle_vpath))
#     else:
#         file_vpath_in_remote = file_support.merge_vpath(cloud_test_folder_root_vpath, file_middle_vpath)
#     buffer_service.move_to_buffer(file_vpath_in_local, local_test_root_folder_vpath, local_buffer_folder_vpath, mode, fgit_password)
#     file_service.upload_file(file_vpath_in_buffer, file_vpath_in_remote)
#     buffer_service.post_move_to_buffer(file_vpath_in_buffer)
#     file_support.real_delete_local_path(local_file_vpath)

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
    pass

def get_encrypted(orginal_path:str):
    pass
