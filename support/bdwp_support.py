

# office doc: https://pan.baidu.com/union/doc/

from support import file_support
import requests
import json
import os
import time
import hashlib

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
    def http_request(self, url, method, headers, params={}, payload={}, files={}):
        res = requests.request(method, url, params=params, headers=headers, data = payload, files = files, timeout=360)
        time.sleep(3)
        if res.status_code == 200:
            return res
        raise Exception("Request failed, eror message: ", res.text)

    def bdwp_request_with_token(self, url, method, headers={}, params={}, payload={} ,files=[]):
        params["access_token"] = self.access_token
        res = self.http_request(url, method, headers, params, payload ,files)
        json_result = res.json()
        res.close()
        return json_result

    # token operation
    # ---------------------------------------------------------------------------------------
    def refresh_token(self, refresh_token, app_key, secret_key):
        params = {"grant_type": "refresh_token", "refresh_token":refresh_token, "client_id":app_key, "client_secret":secret_key}
        res = self.http_request(self.oauth_url, "GET", self.headers, params)
        json_result = res.json()
        res.close()
        return json_result

    # file operation - upload
    # ---------------------------------------------------------------------------------------
    def pre_upload(self, cloud_path, file_size, md5_list):
        cloud_path = file_support.convert_to_unix_path(cloud_path)
        pre_create_url = self.base_url + "/rest/2.0/xpan/file"
        block_list = json.dumps(md5_list)
        payload = {'path': cloud_path, 'size': file_size, 'block_list': block_list, 'isdir': '0', 'autoinit': '1', 'rtype': '3'}
        params = {"method": "precreate"}
        res = self.bdwp_request_with_token(pre_create_url, "POST", self.headers, params, payload)
        upload_id = res['uploadid']
        return upload_id

    def upload_chunk(self, upload_id, chunk_content, chunk_id, cloud_path):
        cloud_path = file_support.convert_to_unix_path(cloud_path)
        upload_url = "https://d.pcs.baidu.com/rest/2.0/pcs/superfile2"
        payload = {}
        files = [('file', chunk_content)]
        params = {"path": cloud_path, "uploadid": upload_id, "method": "upload", "type": "tmpfile", "partseq": chunk_id}
        self.bdwp_request_with_token(upload_url, "POST", self.headers, params, payload, files)

    def create_file(self, cloud_path, upload_id, md5_list, file_size):
        cloud_path = file_support.convert_to_unix_path(cloud_path)
        create_url = self.base_url + "/rest/2.0/xpan/file"
        block_list = json.dumps(md5_list)
        payload = {'path': cloud_path, 'size': file_size, 'uploadid': upload_id, 'block_list': block_list, 'rtype': '3', 'isdir': '0'}
        params = {"method": "create"}
        res = self.bdwp_request_with_token(create_url, "POST", self.headers, params, payload)
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
            md5_list.append(get_md5(c))
        upload_id = self.pre_upload(target_absolute_real_path, file_size, md5_list)
        i = 0
        for c in file_block:
            chunk_content = c
            chunk_id = i
            self.upload_chunk(upload_id, chunk_content, chunk_id, target_absolute_real_path)
            i += 1
        return self.create_file(target_absolute_real_path, upload_id, md5_list, file_size)

    # file operation - download   , 
    # ---------------------------------------------------------------------------------------
    def download_file_with_path(self, cloud_download_absolute_real_path, local_download_absolute_real_path):
        cloud_file_name, cloud_file_parent_path = file_support.virtual_get_file_name_and_parent_path(cloud_download_absolute_real_path)
        res = self.search_file(cloud_file_name, cloud_file_parent_path)
        fs_id = res['list'][0]['fs_id']
        res = self.get_file_meta(fs_id)
        dlink = res['list'][0]['dlink']
        self.download_file(dlink, local_download_absolute_real_path)

    def get_file_content(self, dlink):
        dlink += "&access_token=" + self.access_token
        res = self.http_request(dlink, "GET", self.headers)
        res.close()
        return res.content

    def download_file(self, dlink, local_download_absolute_path):
        file_support.real_write_file_byte(local_download_absolute_path, self.get_file_content(dlink))

    # file/folder operation - deltete
    # ---------------------------------------------------------------------------------------
    def create_folder(self, cloud_absolute_path):
        cloud_absolute_path = file_support.convert_to_unix_path(cloud_absolute_path)
        url = self.base_url + "/rest/2.0/xpan/file"
        params = {"method": "create"}
        payload = {'path': cloud_absolute_path, 'rtype': '1', 'isdir': '1'}
        return self.bdwp_request_with_token(url, "POST", self.headers, params, payload)

    def delete_file_folder(self, cloud_absolute_path):
        cloud_absolute_path = file_support.convert_to_unix_path(cloud_absolute_path)
        url = self.base_url + "/rest/2.0/xpan/file"
        params = {"method": "filemanager", "opera": "delete"}
        payload = {"async": "0", "filelist": json.dumps([{'path': cloud_absolute_path}])}
        return self.bdwp_request_with_token(url, "POST", self.headers, params, payload)

    def move_file_folder(self, cloud_source_file_real_path, cloud_target_folder_real_path, file_name=None):
        if file_name is None:
            file_name = cloud_source_file_real_path.split("/")[-1]
        url = self.base_url + "/rest/2.0/xpan/file"
        params = {"method": "filemanager", "opera": "move"}
        payload = {"async": "0", "filelist": json.dumps([{'path': cloud_source_file_real_path, 'dest': cloud_target_folder_real_path, 'newname': file_name, 'ondup': 'fail'}])}  # ondup: fail, overwrite
        return self.bdwp_request_with_token(url, "POST", self.headers, params, payload)

    # search operation
    # ---------------------------------------------------------------------------------------
    def search_file(self, search_key, search_in):
        url = self.base_url + "/rest/2.0/xpan/file"
        search_in = file_support.convert_to_unix_path(search_in)
        params = {"key": search_key, "dir": search_in, "method": "search", "recursion": 1}
        return self.bdwp_request_with_token(url, "GET", self.headers, params)

    def get_file_meta(self, file_fsid):
        url = self.base_url + "/rest/2.0/xpan/multimedia"
        params = {"fsids": json.dumps([file_fsid]), "method": "filemetas", "dlink": 1, "extra": 1, "needmedia": 1}
        return self.bdwp_request_with_token(url, "GET", self.headers, params)

    def list_folder_file_recursion(self, target_path):
        target_path = file_support.convert_to_unix_path(target_path)
        limitation = 10000
        current_index = 0
        folder_list = []
        file_list = []
        while True:
            res = self.get_multimedia_listall(target_path, current_index, limitation)
            current_file_folder_list = res['list']
            for file_folder in current_file_folder_list:
                if file_folder["isdir"]:
                    folder_list.append(file_folder)
                else:
                    file_list.append(file_folder)
            current_file_folder_list_length = len(current_file_folder_list)
            if current_file_folder_list_length == 0 or current_file_folder_list_length < limitation:
                break
            current_index += limitation
        return folder_list, file_list

    def get_multimedia_listall(self, target_cloud_absolute_path, start=0, limit=1000):
        target_cloud_absolute_path = file_support.convert_to_unix_path(target_cloud_absolute_path)
        url = self.base_url + "/rest/2.0/xpan/multimedia"
        params = {"method": "listall", "path": target_cloud_absolute_path, "web": 0, "recursion": 1, "start": start, "limit": limit}
        return self.bdwp_request_with_token(url, "GET", self.headers, params)

def get_md5(data_string):
    md5 = hashlib.md5()
    md5.update(data_string)
    return md5.hexdigest()

bdwp_instance = BaiduWangPan()
