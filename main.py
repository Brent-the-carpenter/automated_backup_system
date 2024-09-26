import yaml
import os
import shutil
from datetime import datetime
import inspect
from typing import TypedDict, List, Any
import traceback


class BackupConfig(TypedDict):
    source_directories: List[str]
    local_backup_directory: str
    remote_backup_directory: str


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


def get_config(config_file_path: str = "config.yaml") -> BackupConfig | None:
    try:
        if os.path.isfile(config_file_path):
            with open(config_file_path, "r") as file:
                config: dict[str, Any] = yaml.safe_load(file)
            source_directories = config.get("backup", {}).get("source_directories", [])
            local_backup = config.get("backup", {}).get("local_backup_directory", "")
            remote_backup = config.get("backup", {}).get("remote_backup_directory", "")
            if not source_directories or not local_backup:
                raise Exception(
                    "Invalid config: source directories or local backup locations missing."
                )
            return {
                "source_directories": source_directories,
                "local_backup_directory": local_backup,
                "remote_backup_directory": remote_backup,
            }
        else:
            raise Exception(f"{config_file_path} not found.")
    except Exception as e:
        print(f"Error getting config : {e}")
        log_error(e)
        return None


def create_backup(source_directories: List[str], local_backup: str):
    try:
        os.makedirs(local_backup, exist_ok=True)
        if len(source_directories) == 0:
            raise Exception("No source directories found.")
        for source in source_directories:
            if not os.path.isdir(source):
                log_error(f"Source directory not found : {source}")
                continue
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            # Make the path string where file will be stored
            dir_name = os.path.basename(os.path.normpath(source))
            archive_name = os.path.join(
                local_backup, f"{dir_name}_backup_{timestamp}.zip"
            )
            # zip the file and add it to the backup directory
            shutil.make_archive(archive_name.replace(".zip", ""), "zip", source)
    except Exception as e:
        print("An error occured while creating backup")
        log_error(e)


def upload_backup(remote_backup: str, backup_path: str):
    # This is a placeholder for uploading to remote storage
    print(f"uploading {backup_path} to {remote_backup} (Not yet implemented)")
    raise NotImplementedError("Remote upload functionality not implemented yet.")


def main():
    config = get_config()
    if config:
        source_directories = config["source_directories"]
        local_backup = config["local_backup_directory"]
        # remote_backup = config["remote_backup_directory"]
        create_backup(source_directories, local_backup)
        # Placeholder for potential remote upload
        # upload_backup(remote_backup,local_backup)
    else:
        print("Failed to load configuration. Exiting.")
    return


if __name__ == "__main__":
    main()
