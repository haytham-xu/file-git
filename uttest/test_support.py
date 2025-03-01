
import os
import string
from PIL import Image

from support import file_support
from command.command_init import command_init
from support import file_support
# from support.file_support import CURRENT_VPAT

class TestSupport():
    test_folder_name = "test_fgit"
    test_file_txt_1_middle_vpath = "test_1.txt"
    test_file_txt_2_middle_vpath = "folder1/test_2.txt"
    test_file_txt_3_middle_vpath = "folder2/folder22/test_3.txt"
    test_file_png_1_middle_vpath = "test_1.png"
    test_file_png_2_middle_vpath = "folder1/test_2.png"
    test_file_png_3_middle_vpath = "folder2/folder22/test_3.png"
    mock_tmp_vpath = os.getcwd() + "/uttest/tmp"

# os.getcwd --> ~/uttest/tmp/local/test_fgit
# 

    # def get_a(self):
    #     return TestSupport.mock_tmp_vpath + "/cloud/test_fgit"
        # return file_support.merge_vpath(file_support.get_current_vpath())
    def get_mock_cloud_vpath(self):
        # return file_support.merge_vpath(self.get_a(), "cloud", TestSupport.test_folder_name)
        return TestSupport.mock_tmp_vpath + file_support.merge_vpath("cloud", TestSupport.test_folder_name)
    def get_mock_local_vpath(self):
        return file_support.merge_vpath(file_support.get_current_vpath()) # "local", TestSupport.test_folder_name
    def get_local_buffer_folder_vpath(self):
        return file_support.merge_vpath(self.get_mock_local_vpath(), ".fgit", "buffer")
    def get_local_trash_folder_vpath(self):
        return file_support.merge_vpath(self.get_mock_local_vpath(), ".fgit", "trash")
    def get_cloud_trash_folder_vpath(self):
        return file_support.merge_vpath(self.get_mock_cloud_vpath(), ".trash")
    
    def create_file(self, type, localtion, file_middle_vpath):
        base_vpath = self.get_mock_cloud_vpath() if "cloud" == localtion else self.get_mock_local_vpath()
        file_output_vpath = file_support.merge_vpath(base_vpath, file_middle_vpath)
        create_image(1, file_output_vpath) if "png" == type else create_file(1, file_output_vpath)

    
    original_fgit_mode = "ORIGINAL"
    encrypted_fgit_mode = "ENCRYPTED"
    fgit_password = "default_password"
    # fgit_local_vpath = self.get_mock_local_test_vpath()
    # fgit_remote_vpath = self.get_mock_cloud_test_vpath()
    # fgit_app_id = os.getenv("BDWP_APP_ID", "")
    # fgit_secret_key = os.getenv("BDWP_SECRET_KEY", "")
    # fgit_app_key = os.getenv("BDWP_APP_KEY", "")
    # fgit_sign_code = os.getenv("BDWP_SIGN_CODE", "")
    # fgit_expires_in = os.getenv("BDWP_EXPIRES_IN", "")
    # fgit_refresh_token = os.getenv("BDWP_REFRESH_TOKEN", "")
    # fgit_access_token = os.getenv("BDWP_ACCESS_TOKEN", "")
    def get_fgit_local_vpath(self):
        return self.get_mock_local_vpath()
    def get_fgit_remote_vpath(self):
        return self.get_mock_cloud_vpath()
    def get_fgit_app_id(self):
        return os.getenv("BDWP_APP_ID", "")
    def get_fgit_secret_key(self):
        return os.getenv("BDWP_SECRET_KEY", "")
    def get_fgit_app_key(self):
        return os.getenv("BDWP_APP_KEY", "")
    def get_fgit_sign_code(self):
        return os.getenv("BDWP_SIGN_CODE", "")
    def get_fgit_expires_in(self):
        return os.getenv("BDWP_EXPIRES_IN", "")
    def get_fgit_refresh_token(self):
        return os.getenv("BDWP_REFRESH_TOKEN", "")
    def get_fgit_access_token(self):
        return os.getenv("BDWP_ACCESS_TOKEN", "")
    

test_support_instance = TestSupport()


def list_file_recursion_with_hidden(root_path):
    res = []

    for root, dirs, files in os.walk(root_path):
        # dirs[:] = [d for d in dirs if not is_hidden(d)]
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            res.append({
                'path': file_path,
                'size': file_size,
                'server_filename': file
            })
    return res

# ----------------------------------------------------------------


# fgit config
# test_support_instance.get_fgit_local_vpath() = self.get_mock_local_test_vpath()
# test_support_instance.get_fgit_remote_vpath() = self.get_mock_cloud_test_vpath()
# test_support_instance.get_fgit_app_id() = os.getenv("BDWP_APP_ID", "")
# test_support_instance.get_fgit_secret_key() = os.getenv("BDWP_SECRET_KEY", "")
# test_support_instance.get_fgit_app_key() = os.getenv("BDWP_APP_KEY", "")
# test_support_instance.get_fgit_sign_code() = os.getenv("BDWP_SIGN_CODE", "")
# test_support_instance.get_fgit_expires_in() = os.getenv("BDWP_EXPIRES_IN", "")
# test_support_instance.get_fgit_refresh_token() = os.getenv("BDWP_REFRESH_TOKEN", "")
# test_support_instance.get_fgit_access_token() = os.getenv("BDWP_ACCESS_TOKEN", "")

def create_file(size, output_vpath):
    """size is MB, store the file to the output."""
    size_in_bytes = size * 1024 * 1024  # convert MB to bytes
    chars = string.digits + string.ascii_lowercase + string.ascii_uppercase + " "
    repeated_chars = (chars * ((size_in_bytes // len(chars)) + 1))[:size_in_bytes]
    _, virtual_parent_path = file_support.get_file_name_and_parent_vpath(output_vpath)
    file_support.create_local_folder(virtual_parent_path)
    file_support.real_write_file(output_vpath, repeated_chars)
    # with open(output_vpath, 'w') as f:
    #     f.write(repeated_chars)

def create_image(size, output_vpath):
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
    file_support.real_create_png(output_vpath, image, size_in_bytes)
    # with open(output_vpath, 'wb') as f:
    #     image.save(f, format='PNG')
    #     current_size = f.tell()
    #     if current_size < size_in_bytes:
    #         f.write(b'\0' * (size_in_bytes - current_size))

def run_command_init(fgit_mode):
    command_init(fgit_mode, TestSupport.fgit_password, test_support_instance.get_fgit_local_vpath(), test_support_instance.get_fgit_remote_vpath(), test_support_instance.get_fgit_app_id(), test_support_instance.get_fgit_secret_key(), test_support_instance.get_fgit_app_key(), test_support_instance.get_fgit_sign_code(), test_support_instance.get_fgit_expires_in(), test_support_instance.get_fgit_refresh_token(), test_support_instance.get_fgit_access_token())

# def run_command_clone(fgit_mode):
#     command_clone(fgit_mode, fgit_password, fgit_local_vpath, fgit_remote_vpath, fgit_app_id, fgit_secret_key, fgit_app_key, fgit_sign_code, fgit_expires_in, fgit_refresh_token, fgit_access_token)

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
    target_real_path = file_support.real_local_path_convert(target_vpath)
    file_count = 0
    for _, dirnames, filenames in os.walk(target_real_path):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        visible_files = [f for f in filenames if not f.startswith('.')]
        file_count += len(visible_files)
    return file_count

def count_lines_in_file(file_vpath):
    filet_real_path = file_support.real_local_path_convert(file_vpath)
    line_count = 0
    with open(filet_real_path, 'r') as file:
        for _ in file:
            line_count += 1
    return line_count
