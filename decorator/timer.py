
import time
from functools import wraps
from datetime import datetime

ERROR_MESSAGE_TEMPLATE = '''
{current_time}: Execution of '{func_name}' took {elapsed_time:.4f} seconds'''

def timer():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(ERROR_MESSAGE_TEMPLATE.format(current_time=current_time, func_name=func.__name__, elapsed_time=elapsed_time))
            return result
        return wrapper
    return decorator
