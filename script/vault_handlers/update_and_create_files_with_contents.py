import asyncio
from pathlib import Path

import aiofiles

from script.vault_handlers.utils import get_vault_folder_path

VAULT_FOLDER = get_vault_folder_path()

# for testing
# VAULT_FOLDER = Path("./Vault")


async def _update_create_file(file_content: dict[str, str]):
    file_path = file_content.get("file_path")
    content = file_content.get("note")

    if not file_path or not content:
        raise Exception("File path or content is none.", file_content)

    # get .tmp file to wite first
    temp_file_path = file_path + ".tmp"

    file_path = Path(file_path)
    full_file_path = VAULT_FOLDER / temp_file_path

    # create new parent folders if required
    full_file_path.parent.mkdir(parents=True, exist_ok=True)

    async with aiofiles.open(file=full_file_path, mode="w") as f:
        print("working for path", full_file_path)
        await f.write(content)
        return full_file_path  # temp file paths


def _delete_temp_files(temp_file_paths: list[Path]):
    for temp_file in temp_file_paths:
        temp_file.unlink(missing_ok=True)


def _rename_temp_to_note(temp_file_paths: list[Path]):
    for temp_file in temp_file_paths:
        parent_dir = temp_file.parent
        temp_file_name = temp_file.name
        file_name_parts = temp_file_name.split(".")

        # remove the .tmp
        file_name_parts.pop()

        file_name = ".".join(file_name_parts)

        full_file_path = parent_dir / file_name

        temp_file.rename(full_file_path)


async def update_and_create_files_with_content(file_content_list: list[dict[str, str]]):
    file_update_create_tasks = [
        _update_create_file(file_content) for file_content in file_content_list
    ]

    results = await asyncio.gather(*file_update_create_tasks, return_exceptions=True)
    errors = []
    temp_file_paths = []

    for result in results:
        if isinstance(result, Exception):
            errors.append(result)

        else:
            temp_file_paths.append(result)

    if errors:
        # remove the temp files
        _delete_temp_files(temp_file_paths)

        # raise exception
        raise Exception("Error occured when updating/creating files.", errors)

    # change the .tmp files to valid files by removing .tmp
    _rename_temp_to_note(temp_file_paths)
    print("Notes added successfully!")


# for testing
async def main():
    file_content_list = [
        {
            "file_path": "Languages/csharp/clr-execution-model.md",
            "note": "this is my little talk on execution-model.",
        },
        {
            "file_path": "Languages/csharp/value-vs-reference-types.md",
            "note": "this is my little talk on value vs reference types.",
        },
    ]

    await update_and_create_files_with_content(file_content_list)


if __name__ == "__main__":
    asyncio.run(main())
