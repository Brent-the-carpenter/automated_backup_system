import os
from log_error import log_error
import time
from remove_dir_r import remove_dir_r


def clean_up_local_backup(local_backup: str) -> None:
    try:
        list_of_dirs = os.listdir(local_backup)
        thirty_days_ago = time.time() - 30 * 86400
        for dir in list_of_dirs:
            dir_path = os.path.join(local_backup, dir)
            if os.path.getmtime(dir_path) < thirty_days_ago:
                # check if it is a directory
                if os.path.isdir(dir_path):
                    remove_dir_r(dir_path)
                else:
                    # Must be a file
                    os.remove(dir_path)
    except Exception as e:
        print(f"An Error occurred while cleaning local backup : {e}")
        log_error(e)
