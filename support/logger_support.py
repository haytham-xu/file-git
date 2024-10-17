
import os
from datetime import datetime
from support import file_support

class LoggerManager:
    def __init__(self):
        self.log_success_file_name = "success.log"
        self.log_error_file_name = "error.log"
        self.log_success_file = None
        self.log_error_file = None

    def init_log_file(self, log_file_path):
        self.log_success_file = file_support.merge_path(log_file_path, self.log_success_file_name)
        self.log_error_file = file_support.merge_path(log_file_path, self.log_error_file_name)

    def log_success(self, action, local_path, remote_path):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        log_message = f"success {current_time} {action} {local_path} {remote_path}\n"
        with open(self.log_success_file, 'a') as log_file:
            log_file.write(log_message)

    def log_error(self, action, local_path, remote_path, error_track):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        log_message = f"error {current_time} {action} {local_path} {remote_path}\n {error_track}\n\n"
        with open(self.log_error_file, 'a') as log_file:
            log_file.write(log_message)

logger_instance = LoggerManager()
