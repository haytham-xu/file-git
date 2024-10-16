
import os
import string
from PIL import Image

from support import file_support

cloud_test_folder_name = "test_fgit"
cloud_test_root_path = "/apps/sync-assistant/"
test_file_name = "test_1.txt"

local_test_root_folder = file_support.merge_path(os.getcwd(), "uttest" ,cloud_test_folder_name)
cloud_test_folder_root_path = file_support.merge_path(cloud_test_root_path, cloud_test_folder_name)

test_file_local_path = file_support.merge_path(local_test_root_folder, test_file_name)
test_file_cloud_path = file_support.merge_path(cloud_test_folder_root_path, test_file_name)

fgit_mode = "ORIGINAL"
fgit_password = "default_password"
fgit_local_path = local_test_root_folder
fgit_remote_path = "/apps/sync-assistant/test_fgit/"
fgit_app_id = os.getenv("BDWP_APP_ID", "")
fgit_secret_key = os.getenv("BDWP_SECRET_KEY", "")
fgit_app_key = os.getenv("BDWP_APP_KEY", "")
fgit_sign_code = os.getenv("BDWP_SIGN_CODE", "")
fgit_expires_in = os.getenv("BDWP_EXPIRES_IN", "")
fgit_refresh_token = os.getenv("BDWP_REFRESH_TOKEN", "")
fgit_access_token = os.getenv("BDWP_ACCESS_TOKEN", "")

def create_file(size, output_path):
    """size is MB, store the file to the output."""
    size_in_bytes = size * 1024 * 1024  # convert MB to bytes
    chars = string.digits + string.ascii_lowercase + string.ascii_uppercase + " "
    repeated_chars = (chars * ((size_in_bytes // len(chars)) + 1))[:size_in_bytes]
    with open(output_path, 'w') as f:
        f.write(repeated_chars)

def create_image(size, output_path):
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
    with open(output_path, 'wb') as f:
        image.save(f, format='PNG')
        current_size = f.tell()
        if current_size < size_in_bytes:
            f.write(b'\0' * (size_in_bytes - current_size))
