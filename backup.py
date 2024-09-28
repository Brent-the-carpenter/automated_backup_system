import os
import shutil
import boto3
from datetime import datetime
from log_error import log_error

from typing import List


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
    def upload_backup(remote_backup: str, backup_path: str):
        s3_client = boto3.client("s3")
        bucket_name = remote_backup  # Set this based on your config
        file_name = os.path.basename(backup_path)
        s3_client.upload_file(backup_path, bucket_name, file_name)
        print(f"Successfully uploaded {backup_path} to {remote_backup}")
