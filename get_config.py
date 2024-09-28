import os
import yaml
from log_error import log_error
from typing import TypedDict, List, Any


class BackupConfig(TypedDict):
    source_directories: List[str]
    local_backup_directory: str
    remote_backup_directory: str


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
