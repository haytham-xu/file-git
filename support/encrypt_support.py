
import os
import base64

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from support import file_support
from model.logger import logger_instance

def encode_path(source_vpath):
    vpath_segments = source_vpath.split("/")
    virtual_encoded_segments = [base64.urlsafe_b64encode(segment.encode()).decode() for segment in vpath_segments]
    encoded_path = "/".join(virtual_encoded_segments)
    logger_instance.log_debug("encoding path: {} --> {}".format(source_vpath, encoded_path))
    return encoded_path
                              
def decode_path(source_vpath):
    encoded_virtual_segments = source_vpath.split("/")
    decoded_virtual_segments = [base64.urlsafe_b64decode(segment.encode()).decode() for segment in encoded_virtual_segments]
    decoded_path = "/".join(decoded_virtual_segments)
    logger_instance.log_debug("decoding path: {} --> {}".format(source_vpath, decoded_path))
    return decoded_path

def generate_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_file(file_vpath: str, output_vpath: str, password: str):
    file_real_path = file_support.convert_to_rpath(file_vpath)
    output_real_path = file_support.convert_to_rpath(output_vpath)
    file_support.real_create_local_file(output_vpath)
    salt = os.urandom(16)
    key = generate_key(password, salt)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()

    buffer_size = 64 * 1024  # 64KB
    with open(file_real_path, 'rb') as f_in, open(output_real_path, 'wb') as f_out:
        f_out.write(salt + iv)
        while True:
            data = f_in.read(buffer_size)
            if len(data) == 0:
                break
            padded_data = padder.update(data)
            encrypted_data = encryptor.update(padded_data)
            f_out.write(encrypted_data)
        padded_data = padder.finalize()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        f_out.write(encrypted_data)

def decrypt_file(file_vpath: str, output_vpath: str, password: str):
    logger_instance.log_debug("start decrypting file: {} --> {}".format(file_vpath, output_vpath))
    file_real_path = file_support.convert_to_rpath(file_vpath)
    output_real_path = file_support.convert_to_rpath(output_vpath)
    file_support.real_create_local_file(output_vpath)
    buffer_size = 64 * 1024  # 64KB
    with open(file_real_path, 'rb') as f_in, open(output_real_path, 'wb') as f_out:
        salt = f_in.read(16)
        iv = f_in.read(16)
        key = generate_key(password, salt)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()

        while True:
            encrypted_data = f_in.read(buffer_size)
            if len(encrypted_data) == 0:
                break
            padded_data = decryptor.update(encrypted_data)
            data = unpadder.update(padded_data)
            f_out.write(data)
        padded_data = decryptor.finalize()
        data = unpadder.update(padded_data) + unpadder.finalize()
        f_out.write(data)
    logger_instance.log_debug("decrypt file finished: {} --> {}".format(file_vpath, output_vpath))
