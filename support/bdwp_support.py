

# office doc: https://pan.baidu.com/union/doc/
# error code: https://pan.baidu.com/union/doc/okumlx17r
# access token valid days: 30days.

import requests
import json
import os
import hashlib
import re
import time

from decorator.timer import timer
from functools import wraps
from datetime import datetime
from support import file_support

MAX_WAIT_TIME = 3600
ERROR_MESSAGE_TEMPLATE = '''Waiting for {wait_time} seconds before retrying...]'''
ERROR_MESSAGE_TEMPLATE = '''
Get a error: {e}.
Waiting for {wait_time} seconds before retrying...]
'''
GET_INDEX_SUCCESS_MESSAGE = '''
Get Chunk {chunk_index} successfully, chunk size: {chunk_size}.
'''

def retry():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            wait_time = 5
            retries = 1
            while wait_time <= MAX_WAIT_TIME:
                res = func(*args, **kwargs)
                response_content_type = res.headers.get('Content-Type', '')
                status_code = res.status_code
                print("status_code: ", status_code)
                print('response_content_type: ', response_content_type)
                print()
                if status_code in [200, 400] and ('application/json' == response_content_type or 'application/json; charset=UTF-8' == response_content_type):
                    json_result = res.json()
                    if "errno" in json_result and json_result["errno"] == 31034:
                        wait_time += 5
                        retries += 1
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print(f"{current_time}: Received 31034, wait {wait_time}s, will try the {retries} times...")
                        time.sleep(wait_time)
                    else:
                        # normal json resoponse
                        return res
                # content response
                elif status_code == 200:
                    return res
                else:
                    raise Exception("Request failed, eror message: ", res.text)
            raise Exception("Max retries reached, operation failed.")
        return wrapper
    return decorator

class BaiduWangPan:
    def __init__(self, split_size=50*1024*1024, oauth_url="https://openapi.baidu.com/oauth/2.0/token", base_url="https://pan.baidu.com", http_url="http://pan.baidu.com", headers={'User-Agent': 'pan.baidu.com'}, access_token=None):
        self.split_size = split_size
        self.oauth_url = oauth_url
        self.base_url = base_url
        self.http_url = http_url
        self.headers = headers
        self.access_token = access_token

    def set_access_token(self, access_token):
        self.access_token = access_token

    # base
    # ---------------------------------------------------------------------------------------
    @retry()
    @timer()
    def http_request(self, url, method, headers, params={}, payload={}, files={}):
        res = requests.request(method, url, params=params, headers=headers, data = payload, files = files, timeout=360)
        res.close()
        time.sleep(3)
        return res

    def http_request_json(self, url, method, headers={}, params={}, payload={} ,files=[]):
        params["access_token"] = self.access_token
        res = self.http_request(url, method, headers, params, payload ,files)
        return res.json()
    
    def http_request_content(self, dlink):
        dlink += "&access_token=" + self.access_token
        res = self.http_request(dlink, "GET", self.headers)
        return res.content
    
    def get_uinfo(self):
        url = self.base_url + "/rest/2.0/xpan/nas"
        params = {"method":"uinfo"}
        return self.http_request_json(url, "GET", self.headers, params)

    # token operation
    # ---------------------------------------------------------------------------------------
    def refresh_token(self, refresh_token, app_key, secret_key):
        params = {"grant_type": "refresh_token", "refresh_token":refresh_token, "client_id":app_key, "client_secret":secret_key}
        res = self.http_request(self.oauth_url, "GET", self.headers, params)
        return res

    # file operation - upload
    # ---------------------------------------------------------------------------------------
    def pre_upload(self, cloud_path, file_size, md5_list):
        cloud_path = BaiduWangPan.convert_to_unix_path(cloud_path)
        pre_create_url = self.base_url + "/rest/2.0/xpan/file"
        block_list = json.dumps(md5_list)
        payload = {'path': cloud_path, 'size': file_size, 'block_list': block_list, 'isdir': '0', 'autoinit': '1', 'rtype': '3'}
        params = {"method": "precreate"}
        res = self.http_request_json(pre_create_url, "POST", self.headers, params, payload)
        upload_id = res['uploadid']
        return upload_id

    def upload_chunk(self, upload_id, chunk_content, chunk_id, cloud_path):
        cloud_path = BaiduWangPan.convert_to_unix_path(cloud_path)
        upload_url = "https://d.pcs.baidu.com/rest/2.0/pcs/superfile2"
        payload = {}
        files = [('file', chunk_content)]
        params = {"path": cloud_path, "uploadid": upload_id, "method": "upload", "type": "tmpfile", "partseq": chunk_id}
        self.http_request_json(upload_url, "POST", self.headers, params, payload, files)

    def create_file(self, cloud_path, upload_id, md5_list, file_size):
        cloud_path = BaiduWangPan.convert_to_unix_path(cloud_path)
        create_url = self.base_url + "/rest/2.0/xpan/file"
        block_list = json.dumps(md5_list)
        payload = {'path': cloud_path, 'size': file_size, 'uploadid': upload_id, 'block_list': block_list, 'rtype': '3', 'isdir': '0'}
        params = {"method": "create"}
        res = self.http_request_json(create_url, "POST", self.headers, params, payload)
        fs_id = res["fs_id"]
        return fs_id

    def upload_file(self, file_local_real_path, target_absolute_real_path):
        file_size = os.path.getsize(file_local_real_path)
        file_block = []
        md5_list = []
        with open(file_local_real_path, 'rb') as f:
            while True:
                chunk = f.read(self.split_size)
                if not chunk:
                    break
                file_block.append(chunk)
            f.close()
        for c in file_block:
            md5_list.append(BaiduWangPan.get_md5(c))
        upload_id = self.pre_upload(target_absolute_real_path, file_size, md5_list)
        i = 0
        for c in file_block:
            chunk_content = c
            chunk_id = i
            self.upload_chunk(upload_id, chunk_content, chunk_id, target_absolute_real_path)
            i += 1
        return self.create_file(target_absolute_real_path, upload_id, md5_list, file_size)

    # file operation - download
    # ---------------------------------------------------------------------------------------
    def download_file_with_path(self, cloud_download_absolute_real_path, local_download_absolute_real_path):
        res = self.get_file_base_info(cloud_download_absolute_real_path)
        fs_id = res['fs_id']
        res = self.get_file_meta(fs_id)
        dlink = res['list'][0]['dlink']
        BaiduWangPan.real_write_file_byte(local_download_absolute_real_path, self.http_request_content(dlink))

    # file/folder operation - deltete
    # ---------------------------------------------------------------------------------------
    def create_folder(self, cloud_absolute_path):
        cloud_absolute_path = BaiduWangPan.convert_to_unix_path(cloud_absolute_path)
        url = self.base_url + "/rest/2.0/xpan/file"
        params = {"method": "create"}
        payload = {'path': cloud_absolute_path, 'rtype': '1', 'isdir': '1'}
        return self.http_request_json(url, "POST", self.headers, params, payload)

    def delete_file_folder(self, cloud_absolute_path):
        cloud_absolute_path = BaiduWangPan.convert_to_unix_path(cloud_absolute_path)
        url = self.base_url + "/rest/2.0/xpan/file"
        params = {"method": "filemanager", "opera": "delete"}
        payload = {"async": "0", "filelist": json.dumps([{'path': cloud_absolute_path}])}
        return self.http_request_json(url, "POST", self.headers, params, payload)

    def move_file_folder(self, cloud_source_file_real_path, cloud_target_folder_real_path, file_name=None):
        if file_name is None:
            file_name = cloud_source_file_real_path.split("/")[-1]
        url = self.base_url + "/rest/2.0/xpan/file"
        params = {"method": "filemanager", "opera": "move"}
        payload = {"async": "0", "filelist": json.dumps([{'path': cloud_source_file_real_path, 'dest': cloud_target_folder_real_path, 'newname': file_name, 'ondup': 'fail'}])}  # ondup: fail, overwrite
        return self.http_request_json(url, "POST", self.headers, params, payload)

    # search operation - get
    # ---------------------------------------------------------------------------------------
    def list_folder(self, target_path):
        target_path = BaiduWangPan.convert_to_unix_path(target_path)
        url = self.base_url + "/rest/2.0/xpan/file"
        params = {"method": "list", "dir": target_path}
        return self.http_request_json(url, "GET", self.headers, params)
    
    def get_file_base_info(self, file_path):
        target_ffile_path = BaiduWangPan.convert_to_unix_path(file_path)
        cloud_file_name, cloud_file_parent_path = BaiduWangPan.get_file_name_and_parent_vpath(target_ffile_path)
        res = self.list_folder(cloud_file_parent_path)
        file_list = res['list']
        for file in file_list:
            if file['server_filename'] == cloud_file_name:
                return file
        raise FileNotFoundError("File not found: ", file_path)


    # search operation - get extend
    # ---------------------------------------------------------------------------------------
    def get_file_meta(self, file_fsid):
        url = self.base_url + "/rest/2.0/xpan/multimedia"
        params = {"fsids": json.dumps([file_fsid]), "method": "filemetas", "dlink": 1, "extra": 1, "needmedia": 0}
        return self.http_request_json(url, "GET", self.headers, params)
    
    def check_folder_exists(self, search_key, search_in):
        json_data = self.list_folder(search_in)
        for item in json_data['list']:
            if item['server_filename'] == search_key:
                return True
        return False

    def get_multimedia_listall(self, target_cloud_absolute_path, start=0, limit=1000):
        target_cloud_absolute_path = BaiduWangPan.convert_to_unix_path(target_cloud_absolute_path)
        url = self.base_url + "/rest/2.0/xpan/multimedia"
        params = {"method": "listall", "path": target_cloud_absolute_path, "web": 0, "recursion": 1, "start": start, "limit": limit}
        return self.http_request_json(url, "GET", self.headers, params)
    

    # TODO need further pressure test
    def list_file_recursion(self, cloud_rpath, chunk_folder_path=".fgit/chunks", cloud_index_output_path = ".fgit/cloud_index.json"):
        start_index = 0
        chunk_size = 10000
        current_index = start_index

        file_support.create_local_folder(chunk_folder_path)
        chunk_file_path_list = []

        while True:
            res = bdwp_instance.get_multimedia_listall(cloud_rpath, start=current_index, limit=chunk_size)
            print(res)
            has_more = res['has_more']
            file_folder_list = res['list']

            current_chunk_files_list = []
            current_chunk_folder_list = []

            for file_folder in file_folder_list:
                if file_folder["isdir"]:
                    current_chunk_folder_list.append(file_folder)
                else:
                    current_chunk_files_list.append(file_folder)

            chunk_file_index = current_index // chunk_size
            current_chunk_file_path = os.path.join(chunk_folder_path, f"chunk_{chunk_file_index}.json")
            chunk_file_path_list.append(current_chunk_file_path)

            file_support.real_write_json_file(current_chunk_file_path, current_chunk_files_list)
            current_index += chunk_size
            print(GET_INDEX_SUCCESS_MESSAGE.format(chunk_index=chunk_file_index, chunk_size=len(current_chunk_files_list)))
            if has_more == 0:
                break
        # merge chunk files
        all_files = []
        for current_chunk_file_path in chunk_file_path_list:
            all_files.extend(file_support.real_read_json_file(current_chunk_file_path))

        print(f"Total files: {len(all_files)}")

        clean_files_data = []
        for a_file in all_files:
            clean_files_data.append({
                "path": a_file["path"], 
                "size": a_file["size"],
                "filename": a_file["server_filename"]
            })

        file_support.real_write_json_file(cloud_index_output_path, clean_files_data)
        file_support.real_delete_local_path(chunk_folder_path)
        return all_files

    
    # static method
    # ---------------------------------------------------------------------------------------
    @staticmethod
    def convert_to_unix_path(a_path:str):
        path_list = re.split(r'[\\/]', a_path)
        path_list = [p for p in path_list if p]
        res = "/" + "/".join(path_list)
        return res

    @staticmethod
    def get_md5(data_string):
        md5 = hashlib.md5()
        md5.update(data_string)
        return md5.hexdigest()
    
    @staticmethod
    def real_write_file_byte(unix_path:str, content):
        rpath = BaiduWangPan.unix_path_to_os_path(unix_path)
        with open(rpath, 'wb+') as f:
            f.write(content)
        f.close()

    @staticmethod
    def unix_path_to_os_path(unix_path):
        path_list = unix_path.split("/")
        a = os.path.sep.join(path_list)
        if a[0] == "/":
            return a
        if a[0] == "\\":
            return a[1:]
        return a
    
    @staticmethod
    def get_file_name_and_parent_vpath(vpath):
        vpath_part_list = vpath.split("/")
        vpath_part_list = [p for p in vpath_part_list if p]
        virtual_file_name = vpath_part_list[-1]
        virtual_file_parent_path = "/" + "/".join(vpath_part_list[:-1])
        return virtual_file_name, virtual_file_parent_path

bdwp_instance = BaiduWangPan()
