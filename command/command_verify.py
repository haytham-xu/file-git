
from facade import index_facade
from facade import push_facade

from datetime import datetime
from support import file_support
from support.constant_support import constant_instance
from support.config_support import config_instance
from support import time_support

action_name = "verify"

def command_verify():

    current_action_folder_name = time_support.get_action_folder_name(action_name)
    current_action_folder_path = file_support.merge_path(constant_instance.get_action_folder_path(), current_action_folder_name)
    file_support.create_folder(current_action_folder_path)

    current_action_index_path = file_support.merge_path(current_action_folder_path, "index")
    file_support.create_folder(current_action_index_path)

    current_action_log_path = file_support.merge_path(current_action_folder_path, "log")
    file_support.create_folder(current_action_log_path)

    local_index_json_path = file_support.merge_path(current_action_index_path, "local.json")
    local_index_json = index_facade.get_local_index(config_instance.get_local_path())
    file_support.write_json_file(local_index_json_path, local_index_json)

    remote_index_json_path = file_support.merge_path(current_action_index_path, "remote.json")
    cloud_index_json = index_facade.get_cloud_index(config_instance.get_remote_path())
    file_support.write_json_file(remote_index_json_path, cloud_index_json)

    only_in_local_json = push_facade.get_only_in_local(local_index_json, cloud_index_json)
    only_in_cloud_json = push_facade.get_only_in_remote(local_index_json, cloud_index_json)
    local_cloud_diff_json = push_facade.get_local_remote_diff(local_index_json, cloud_index_json)

    report_file_path = file_support.merge_path(current_action_folder_path, "report.json")

    return generate_diff_report(only_in_local_json, only_in_cloud_json, local_cloud_diff_json, report_file_path)

    
def generate_diff_report(only_in_local_json, only_in_cloud_json, local_cloud_diff_json, report_file_path):

    if len(only_in_local_json) == 0 and len(only_in_cloud_json) == 0 and len(local_cloud_diff_json) == 0:
        print("No differences found.")
        return False

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(report_file_path, 'w') as report_file:
        report_file.write(f"Diff Report - {current_time}\n")
        report_file.write("=" * 40 + "\n\n")
        
        report_file.write("Only in Local:\n")
        report_file.write("-" * 40 + "\n")
        for _, value in only_in_local_json.items():
            report_file.write(f"LOCAL: {value['middle_path']}\n")
        report_file.write("\n")
        
        report_file.write("Only in Cloud:\n")
        report_file.write("-" * 40 + "\n")
        for _, value in only_in_cloud_json.items():
            report_file.write(f"CLOUD: {value['middle_path']}\n")
        report_file.write("\n")
        
        report_file.write("Local vs Cloud Differences:\n")
        report_file.write("-" * 40 + "\n")
        for _, value in local_cloud_diff_json.items():
            report_file.write(f"DIFF: local {value['local']['middle_path']} remote {value['remote']['middle_path']}\n")
        report_file.write("\n")

    return True
