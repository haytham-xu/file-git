
from datetime import datetime
from support import file_support
from model.constant import FilegitConstant
from model.config import config_instance
import inspect
import os
import threading

class LoggerManager:
    def __init__(self):
        self.log_success_file_vpath = None
        self.log_error_file_vpath = None
        self.buffer = 0
        self.buffer_message = ""

    def get_log_success_file_vpath(self):
        return self.log_success_file_vpath
    def get_log_error_file_vpath(self):
        return self.log_error_file_vpath

    def init_log_file(self, log_file_vpath):
        self.log_success_file_vpath = file_support.merge_vpath(log_file_vpath, FilegitConstant.LOG_SUCCESS_FILE_NAME)
        self.log_error_file_vpath = file_support.merge_vpath(log_file_vpath, FilegitConstant.LOG_ERROR_FILE_NAME)

    def log_success(self, action, local_vpath:str, remote_vpath:str):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"success {current_time} {action} {local_vpath.removeprefix(config_instance.get_local_vpath())} {remote_vpath.removeprefix(config_instance.get_remote_vpath())}\n"
        if not file_support.is_local_exist(self.log_success_file_vpath):
            file_support.real_create_local_file(self.log_success_file_vpath)
        file_support.real_append_file(self.log_success_file_vpath, log_message)

    def log_error(self, action, local_vpath, remote_vpath, error_track):
        if not file_support.is_local_exist(self.log_error_file_vpath):
            file_support.real_create_local_file(self.log_error_file_vpath)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")    
        log_message = f"error {current_time} {action} {local_vpath} {remote_vpath}\n {error_track}\n\n"
        file_support.real_append_file(self.log_error_file_vpath, log_message)

        frame = inspect.currentframe().f_back
        caller_file = os.path.basename(frame.f_globals["__file__"])
        caller_function = frame.f_code.co_name

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        thread_id = threading.get_ident()
        message = '  '.join([local_vpath, error_track])
        print(f"[ERROR] {current_time} {caller_file}.{caller_function} || {thread_id} || {message}")

    def log_debug(self, *args):
        frame = inspect.currentframe().f_back
        caller_file = os.path.basename(frame.f_globals["__file__"])
        caller_function = frame.f_code.co_name

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = '  '.join(map(str, args))
        thread_id = threading.get_ident()
        print(f"[DEBUG] {current_time} {caller_file}.{caller_function} || {thread_id} || {message}")

logger_instance = LoggerManager()
