
from datetime import datetime

def get_time_with_ymd():
    now = datetime.now()
    return now.strftime("%Y%m%d")

