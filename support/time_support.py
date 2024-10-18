
from datetime import datetime

def get_time_with_ymd():
    now = datetime.now()
    # return now.strftime("%Y%m%d%H%M")
    return now.strftime("%Y%m%d")

def get_action_folder_name(action_name):
    return "{}_{}".format(get_time_with_ymd(), action_name)
