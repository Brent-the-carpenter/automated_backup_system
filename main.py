from get_config import get_config
from backup import create_backup
from clean_local_backup import clean_up_local_backup
from log_error import log_error


def main():
    try:
        config = get_config()
        if config:
            source_directories = config["source_directories"]
            local_backup = config["local_backup_directory"]
            # remote_backup = config["remote_backup_directory"]
            clean_up_local_backup(local_backup)
            create_backup(source_directories, local_backup)
            # Placeholder for potential remote upload
            # upload_backup(remote_backup,local_backup)
        else:
            log_error(Exception("Failed to load configuration."))
            print("Failed to load configuration. Exiting.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        log_error(e)


if __name__ == "__main__":
    main()
