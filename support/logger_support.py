
from datetime import datetime
from support import file_support
from support import constant_support
from support.queue_support import queue_instance

class LoggerManager:
    def __init__(self):
        self.log_success_file_name = "success.log"
        self.log_error_file_name = "error.log"
        self.log_success_file_virtual_path = None
        self.log_error_file_virtual_path = None
        self.buffer = 0
        self.buffer_message = ""

    def init_log_file(self, log_file_virtual_path):
        self.log_success_file_virtual_path = file_support.virtual_merge_path(log_file_virtual_path, self.log_success_file_name)
        self.log_error_file_virtual_path = file_support.virtual_merge_path(log_file_virtual_path, self.log_error_file_name)

    def log_success(self, action, local_virtual_path, remote_virtual_path):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"success {current_time} {action} {local_virtual_path} {remote_virtual_path}\n"
        print(log_message)
        
        if queue_instance.is_queue_empty() or (not queue_instance.is_queue_empty() and self.buffer >= constant_support.buffer_size):
            if not file_support.real_is_local_exist(self.log_success_file_virtual_path):
                file_support.real_create_local_file(self.log_success_file_virtual_path)
            self.buffer_message += log_message
            file_support.real_append_file(self.log_success_file_virtual_path, self.buffer_message)
            self.buffer_message = ""
        else:
            self.buffer += 1
            self.buffer_message += log_message

    def log_error(self, action, local_virtual_path, remote_virtual_path, error_track):
        if not file_support.real_is_local_exist(self.log_error_file_virtual_path):
            file_support.real_create_local_file(self.log_error_file_virtual_path)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")    
        log_message = f"error {current_time} {action} {local_virtual_path} {remote_virtual_path}\n {error_track}\n\n"
        print(log_message)
        file_support.real_append_file(self.log_error_file_virtual_path, log_message)

logger_instance = LoggerManager()
