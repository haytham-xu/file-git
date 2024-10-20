
import os
import string
from PIL import Image

from support import file_support
from hook.hook import Hooks
from command.command_init import command_init
from command.command_clone import command_clone
from support.bdwp_support import bdwp_instance
from support.config_support import Mode
from support.constant_support import constant_instance
from support.config_support import config_instance
from service import buffer_service
from service import file_service

from support import encrypt_support 

# test data
cloud_test_folder_name = "test_fgit"
cloud_test_root_virtual_path = file_support.virtual_merge_path("apps", "sync-assistant")
local_test_root_folder_virtual_path = file_support.virtual_merge_path(file_support.virtual_get_current_path(), "uttest", cloud_test_folder_name)
cloud_test_folder_root_virtual_path = file_support.virtual_merge_path(cloud_test_root_virtual_path, cloud_test_folder_name)

test_file_txt_1_middle_virtual_path = "test_1.txt"
test_file_txt_1_local_virtual_path = file_support.virtual_merge_path(local_test_root_folder_virtual_path, test_file_txt_1_middle_virtual_path)
test_file_txt_1_cloud_virtual_path = file_support.virtual_merge_path(cloud_test_folder_root_virtual_path, test_file_txt_1_middle_virtual_path)

test_file_txt_2_middle_virtual_path = "folder1/test_2.txt"
test_file_txt_2_local_virtual_path = file_support.virtual_merge_path(local_test_root_folder_virtual_path, test_file_txt_2_middle_virtual_path)
test_file_txt_2_cloud_virtual_path = file_support.virtual_merge_path(cloud_test_folder_root_virtual_path, test_file_txt_2_middle_virtual_path)

test_file_txt_3_middle_virtual_path = "folder2/folder22/test_3.txt"
test_file_txt_3_local_virtual_path = file_support.virtual_merge_path(local_test_root_folder_virtual_path, test_file_txt_3_middle_virtual_path)
test_file_txt_3_cloud_virtual_path = file_support.virtual_merge_path(cloud_test_folder_root_virtual_path, test_file_txt_3_middle_virtual_path)

test_file_png_1_middle_virtual_path = "test_1.png"
test_file_png_1_local_virtual_path = file_support.virtual_merge_path(local_test_root_folder_virtual_path, test_file_png_1_middle_virtual_path)
test_file_png_1_cloud_virtual_path = file_support.virtual_merge_path(cloud_test_folder_root_virtual_path, test_file_png_1_middle_virtual_path)

test_file_png_2_middle_virtual_path = "folder1/test_2.png"
test_file_png_2_local_virtual_path = file_support.virtual_merge_path(local_test_root_folder_virtual_path, test_file_png_2_middle_virtual_path)
test_file_png_2_cloud_virtual_path = file_support.virtual_merge_path(cloud_test_folder_root_virtual_path, test_file_png_2_middle_virtual_path)

test_file_png_3_middle_virtual_path = "folder2/folder22/test_3.png"
test_file_png_3_local_virtual_path = file_support.virtual_merge_path(local_test_root_folder_virtual_path, test_file_png_3_middle_virtual_path)
test_file_png_3_cloud_virtual_path = file_support.virtual_merge_path(cloud_test_folder_root_virtual_path, test_file_png_3_middle_virtual_path)

# fgit config
original_fgit_mode = "ORIGINAL"
encrypted_fgit_mode = "ENCRYPTED"
fgit_password = "default_password"
fgit_local_virtual_path = local_test_root_folder_virtual_path
fgit_remote_virtual_path = cloud_test_folder_root_virtual_path
fgit_app_id = os.getenv("BDWP_APP_ID", "")
fgit_secret_key = os.getenv("BDWP_SECRET_KEY", "")
fgit_app_key = os.getenv("BDWP_APP_KEY", "")
fgit_sign_code = os.getenv("BDWP_SIGN_CODE", "")
fgit_expires_in = os.getenv("BDWP_EXPIRES_IN", "")
fgit_refresh_token = os.getenv("BDWP_REFRESH_TOKEN", "")
fgit_access_token = os.getenv("BDWP_ACCESS_TOKEN", "")

def create_file(size, output_virtual_path):
    """size is MB, store the file to the output."""
    size_in_bytes = size * 1024 * 1024  # convert MB to bytes
    chars = string.digits + string.ascii_lowercase + string.ascii_uppercase + " "
    repeated_chars = (chars * ((size_in_bytes // len(chars)) + 1))[:size_in_bytes]
    _, virtual_parent_path = file_support.virtual_get_file_name_and_parent_path(output_virtual_path)
    file_support.real_create_local_folder(virtual_parent_path)
    file_support.real_write_file(output_virtual_path, repeated_chars)
    # with open(output_virtual_path, 'w') as f:
    #     f.write(repeated_chars)

def create_image(size, output_virtual_path):
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
    _, virtual_parent_path = file_support.virtual_get_file_name_and_parent_path(output_virtual_path)
    file_support.real_create_local_folder(virtual_parent_path)
    file_support.real_create_png(output_virtual_path, image, size_in_bytes)
    # with open(output_virtual_path, 'wb') as f:
    #     image.save(f, format='PNG')
    #     current_size = f.tell()
    #     if current_size < size_in_bytes:
    #         f.write(b'\0' * (size_in_bytes - current_size))

def run_command_init(fgit_mode):
    command_init(fgit_mode, fgit_password, fgit_local_virtual_path, fgit_remote_virtual_path, fgit_app_id, fgit_secret_key, fgit_app_key, fgit_sign_code, fgit_expires_in, fgit_refresh_token, fgit_access_token)

def run_command_clone(fgit_mode):
    command_clone(fgit_mode, fgit_password, fgit_local_virtual_path, fgit_remote_virtual_path, fgit_app_id, fgit_secret_key, fgit_app_key, fgit_sign_code, fgit_expires_in, fgit_refresh_token, fgit_access_token)

def create_file_in_remote(local_file_virtual_path, cloud_file_virtual_path, file_type):
    if file_type == 'txt':
        create_file(1, local_file_virtual_path)
    elif file_type == 'png':
        create_image(1, local_file_virtual_path)
    else:
        raise ValueError("Unsupported file type")
    
    file_middle_virtual_path = local_file_virtual_path.removeprefix(config_instance.get_virtual_local_path())
    file_path_in_virtual_local = file_support.virtual_merge_path(config_instance.get_virtual_local_path(), file_middle_virtual_path)
    file_virtual_path_in_buffer = buffer_service.get_file_buffer_path(constant_instance.get_virtual_buffer_folder_path(), file_middle_virtual_path)

    file_virtual_path_in_remote = None
    if config_instance.get_mode() == Mode.ENCRYPTED:
        file_virtual_path_in_remote = file_support.virtual_merge_path(config_instance.get_virtual_remote_path(), encrypt_support.encode_path(file_middle_virtual_path))
    else:
        file_virtual_path_in_remote = file_support.virtual_merge_path(config_instance.get_virtual_remote_path(), file_middle_virtual_path)

    buffer_service.move_to_buffer(file_path_in_virtual_local)
    file_service.upload_file(file_virtual_path_in_buffer, file_virtual_path_in_remote)
    buffer_service.post_move_to_buffer(file_virtual_path_in_buffer)
    file_support.real_delete_local_path(local_file_virtual_path)

def count_file(target_virtual_path):
    target_real_path = file_support.real_local_path_convert(target_virtual_path)
    file_count = 0
    for _, dirnames, filenames in os.walk(target_real_path):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        visible_files = [f for f in filenames if not f.startswith('.')]
        file_count += len(visible_files)
    return file_count

def count_lines_in_file(file_virtual_path):
    filet_real_path = file_support.real_local_path_convert(file_virtual_path)
    line_count = 0
    with open(filet_real_path, 'r') as file:
        for _ in file:
            line_count += 1
    return line_count
