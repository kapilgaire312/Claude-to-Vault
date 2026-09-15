from pathlib import Path

from script.vault_handlers.utils import (
    get_vault_folder_path,
    is_file_path_structure_valid,
)

VAULT_FOLDER = get_vault_folder_path()


def check_and_get_valid_file_paths(files_paths_dict: dict[str, list[str]]):
    files_to_update = files_paths_dict.get("existing_files_to_update")
    files_to_link = files_paths_dict.get("existing_files_to_link_only")
    files_to_create = files_paths_dict.get("new_files_to_create")

    missing_files_in_update: list[str] = []
    valid_files_to_update: list[str] = []
    valid_files_to_link: list[str] = []
    valid_files_to_create = []

    if files_to_update:
        for file_path in files_to_update:
            # check structure of file_path string
            is_valid = is_file_path_structure_valid(file_path)
            if not is_valid:
                print("Invalid file path for update.", file_path)
                print("skipping...")
                continue

            relative_file_path = Path(file_path)
            absolute_file_path = VAULT_FOLDER / relative_file_path

            # here not adding the absolute file path directly since this needs to be sent to the gemini generator.
            if not absolute_file_path.is_file():
                # if the file to update is missing, add it to new_files_to_create list.
                missing_files_in_update.append(file_path)

            else:
                valid_files_to_update.append(file_path)

    if files_to_link:
        for file_path in files_to_link:
            is_valid = is_file_path_structure_valid(file_path)
            if not is_valid:
                print("Invalid file path for link.", file_path)
                print("skipping...")
                continue

            relative_file_path = Path(file_path)
            absolute_file_path = VAULT_FOLDER / relative_file_path

            if absolute_file_path.is_file():
                valid_files_to_link.append(file_path)

    if files_to_create:
        for file_path in files_to_create:
            is_valid = is_file_path_structure_valid(file_path)
            if not is_valid:
                print("Invalid file path for create.", file_path)
                print("skipping...")
                continue

            valid_files_to_create.append(file_path)

    total_files_to_create = valid_files_to_create + missing_files_in_update

    return {
        "existing_files_to_update": valid_files_to_update,
        "new_files_to_create": total_files_to_create,
        "existing_files_to_link_only": valid_files_to_link,
    }
