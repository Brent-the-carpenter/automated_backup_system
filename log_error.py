from datetime import datetime
import os
import inspect
import traceback


def log_error(error: Exception):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    month = datetime.now().strftime("%y%m")
    log_dir = f"logs/errors/{month}"
    caller_name = inspect.stack()[1].function
    os.makedirs(log_dir, exist_ok=True)
    error_name = os.path.join(log_dir, f"{timestamp}.txt")
    with open(error_name, "a") as file:
        file.write(
            f"---\n[{timestamp}] Error in function: {caller_name}\n{str(error)}\n{traceback.format_exc()}\n---\n"
        )
    print(f"Error logged from {caller_name}: {error}")
