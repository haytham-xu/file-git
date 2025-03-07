
from enum import Enum

from datetime import datetime
from support import file_support
from support import fgit_support
from facade import index_facade

action_name = "diff"

class DIFF_STRATEGY(Enum):
    LOCAL = 'LOCAL'
    REMOTE = 'REMOTE'

    @classmethod
    def from_string(cls, string_value):
        try:
            return cls(string_value)
        except ValueError:
            raise ValueError(f"'{string_value}' is not a valid {cls.__name__}")
        
def command_diff(strategy, virtual_source_path, virtual_target_path):
    current_action_folder_name = fgit_support.get_action_folder_name(action_name)
    current_action_folder_path = file_support.merge_vpath(constant_support.ACTION_FOLDER_VPATH, current_action_folder_name)
    file_support.create_local_folder(current_action_folder_path)

    current_action_index_path = file_support.merge_vpath(current_action_folder_path, "index")
    file_support.create_local_folder(current_action_index_path)

    current_action_log_path = file_support.merge_vpath(current_action_folder_path, "log")
    file_support.create_local_folder(current_action_log_path)

    diff_strategy = DIFF_STRATEGY.from_string(strategy)
    if diff_strategy == DIFF_STRATEGY.LOCAL:
        source_index_json_path = file_support.merge_vpath(current_action_index_path, "source.json")
        source_index_json = index_facade.get_local_index(virtual_source_path)
        file_support.real_write_json_file(source_index_json_path, source_index_json)

        target_index_json_path = file_support.merge_vpath(current_action_index_path, "target.json")
        target_index_json = index_facade.get_local_index(virtual_target_path)
        file_support.real_write_json_file(target_index_json_path, target_index_json)

        only_in_source_json = index_facade.get_only_in_local(source_index_json, target_index_json)
        only_in_target_json = index_facade.get_only_in_remote(source_index_json, target_index_json)

        report_file_path = file_support.merge_vpath(current_action_folder_path, "report.json")
        return generate_diff_report(only_in_source_json, only_in_target_json, report_file_path)
    
    if diff_strategy == DIFF_STRATEGY.REMOTE:
        source_index_json_path = file_support.merge_vpath(current_action_index_path, "source.json")
        source_index_json = index_facade.get_cloud_index(virtual_source_path)
        file_support.real_write_json_file(source_index_json_path, source_index_json)

        target_index_json_path = file_support.merge_vpath(current_action_index_path, "target.json")
        target_index_json = index_facade.get_cloud_index(virtual_target_path)
        file_support.real_write_json_file(target_index_json_path, target_index_json)

        only_in_source_json = index_facade.get_only_in_local(source_index_json, target_index_json)
        only_in_target_json = index_facade.get_only_in_remote(source_index_json, target_index_json)

        report_file_path = file_support.merge_vpath(current_action_folder_path, "report.json")
        return generate_diff_report(only_in_source_json, only_in_target_json, report_file_path)
    
    raise ValueError(f"'{strategy}' is not a valid DIFF_STRATEGY")
        
def generate_diff_report(only_in_local_json, only_in_cloud_json, report_file_path):
    
    report_file_path = file_support.convert_to_rpath(report_file_path)

    if len(only_in_local_json) == 0 and len(only_in_cloud_json) == 0:
        print("No differences found.")
        return False

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(report_file_path, 'w') as report_file:
        report_file.write(f"Diff Report - {current_time}\n")
        report_file.write("=" * 40 + "\n\n")
        
        report_file.write("Only in Source:\n")
        report_file.write("-" * 40 + "\n")
        for _, value in only_in_local_json.items():
            report_file.write(f"LOCAL: {value['middle_path']}\n")
        report_file.write("\n")
        
        report_file.write("Only in Target:\n")
        report_file.write("-" * 40 + "\n")
        for _, value in only_in_cloud_json.items():
            report_file.write(f"CLOUD: {value['middle_path']}\n")
        report_file.write("\n")

    return True
