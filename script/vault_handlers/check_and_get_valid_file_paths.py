import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
VAULT_FOLDER = os.getenv("VAULT_FOLDER")


def check_and_get_valid_file_paths(files_paths_dict: dict[str, list[str]]):
    files_to_update = files_paths_dict.get("existing_files_to_update")
    files_to_link = files_paths_dict.get("existing_files_to_link_only")
    files_to_create = files_paths_dict.get("new_files_to_create")

    missing_files_in_update: list[str] = []
    valid_files_to_update: list[str] = []
    valid_files_to_link: list[str] = []

    if not VAULT_FOLDER:
        raise Exception("Vault folder is not set in .env!")
    vault_path = Path(VAULT_FOLDER)

    if not vault_path.is_dir():
        raise Exception("VAULT_FOLDER path is not valid! Add a valid folder path.")

    if files_to_update:
        for file_path in files_to_update:
            relative_file_path = Path(file_path)
            absolute_file_path = vault_path / relative_file_path

            # here not adding the absolute file path directly since this needs to be sent to the gemini generator.
            if not absolute_file_path.is_file():
                #if the file to update is missing, add it to new_files_to_create list.
                missing_files_in_update.append(file_path)

            else:
                valid_files_to_update.append(file_path)

    if files_to_link:
        for file_path in files_to_link:
            relative_file_path = Path(file_path)
            absolute_file_path = vault_path / relative_file_path

            if absolute_file_path.is_file():
                valid_files_to_link.append(file_path)

    if not files_to_create:
        files_to_create = []
    total_files_to_create = files_to_create + missing_files_in_update

    return {
        "existing_files_to_update": valid_files_to_update,
        "new_files_to_create": total_files_to_create,
        "existing_files_to_link_only": valid_files_to_link,
    }
