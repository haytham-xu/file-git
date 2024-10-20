
from support import file_support

class Constant():
    
    def __init__(self, local_path="", file_git_foler_name=".fgit", trash_folder_name="trash", action_folder_name="action", buffer_folder_name="buffer", queue_file_name="queue.json", config_file_name="config.json"):
        self.virtual_local_path = local_path
        self.file_git_foler_name = file_git_foler_name
        self.trash_folder_name = trash_folder_name
        self.action_folder_name = action_folder_name
        self.buffer_folder_name = buffer_folder_name
        self.queue_file_name = queue_file_name
        self.config_file_name = config_file_name
    
    def get_virtual_local_path(self):
        if self.virtual_local_path == "":
            raise Exception("local_path is empty.")
        return self.virtual_local_path
    
    def get_virtual_file_git_folder_middle_path(self):
        return self.get_file_git_folder_name()
    def get_virtual_file_git_folder_path(self):
        return file_support.virtual_merge_path(self.get_virtual_local_path(), self.get_virtual_file_git_folder_middle_path())
    
    def get_virtual_trash_folder_middle_path(self):
        return file_support.virtual_merge_path(self.get_virtual_file_git_folder_middle_path(), self.get_trash_folder_name())
    def get_virtual_trash_folder_path(self):
        return file_support.virtual_merge_path(self.get_virtual_local_path(), self.get_virtual_trash_folder_middle_path())
    
    def get_virtual_action_folder_middle_path(self):
        return file_support.virtual_merge_path(self.get_virtual_file_git_folder_middle_path(), self.get_action_folder_name())
    def get_virtual_action_folder_path(self):
        return file_support.virtual_merge_path(self.get_virtual_local_path(), self.get_virtual_action_folder_middle_path())
    
    def get_virtual_buffer_folder_middle_path(self):
        return file_support.virtual_merge_path(self.get_virtual_file_git_folder_middle_path(), self.get_buffer_folder_name())
    def get_virtual_buffer_folder_path(self):
        return file_support.virtual_merge_path(self.get_virtual_local_path(), self.get_virtual_buffer_folder_middle_path())
    
    def get_virtual_queue_file_middle_path(self):
        return file_support.virtual_merge_path(self.get_virtual_file_git_folder_middle_path(), self.get_queue_file_name())
    def get_virtual_queue_file_path(self):
        return file_support.virtual_merge_path(self.get_virtual_local_path(), self.get_virtual_queue_file_middle_path())
    
    def get_virtual_config_file_middle_path(self):
        return file_support.virtual_merge_path(self.get_virtual_file_git_folder_middle_path(), self.get_config_file_name())
    def get_virtual_config_file_path(self):
        return file_support.virtual_merge_path(self.get_virtual_local_path(), self.get_virtual_config_file_middle_path())

    
    def set_virtual_local_path(self, local_path):
        self.virtual_local_path = local_path
        
    def get_file_git_folder_name(self):
        return self.file_git_foler_name
    def get_trash_folder_name(self):
        return self.trash_folder_name
    def get_action_folder_name(self):
        return self.action_folder_name
    def get_buffer_folder_name(self):
        return self.buffer_folder_name
    def get_queue_file_name(self):
        return self.queue_file_name
    def get_config_file_name(self):
        return self.config_file_name

constant_instance = Constant()
