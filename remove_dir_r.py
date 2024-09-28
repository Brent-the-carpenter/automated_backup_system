import os
from log_error import log_error


def remove_dir_r(dir_path):
    try:
        entries = os.listdir(dir_path)
        for entry in entries:
            entry_path = os.path.join(dir_path, entry)
            if os.path.isdir(os.path.join(dir_path, entry)):
                remove_dir_r(entry_path)
                os.rmdir(entry_path)
            else:
                os.remove(entry_path)
        os.rmdir(dir_path)
    except Exception as e:
        print(f"Error removing {dir_path}\n Error: {e}")
        log_error(e)
