import asyncio
from pathlib import Path

import aiofiles

from script.vault_handlers.utils import get_vault_folder_path

VAULT_FOLDER = get_vault_folder_path()


async def _update_create_file(file_content: dict[str, str]):
    if not VAULT_FOLDER:
        raise Exception("Vault Folder not set in .env")

    file_path = file_content.get("file_path")
    content = file_content.get("note")

    if not file_path or not content:
        raise Exception("File path or content is none.", file_content)

    file_path = Path(file_path)
    full_file_path = VAULT_FOLDER/ file_path

    # create new parent folders if required
    full_file_path.parent.mkdir(parents=True, exist_ok=True)

    async with aiofiles.open(file=full_file_path, mode="w") as f:
        print("working for path", full_file_path)
        await f.write(content)

        return "success"


async def update_and_create_files_with_content(file_content_list: list[dict[str, str]]):
    file_update_create_tasks = [
        _update_create_file(file_content) for file_content in file_content_list
    ]

    results = await asyncio.gather(*file_update_create_tasks, return_exceptions=True)
    errors = []
    for result in results:
        if isinstance(result, Exception):
            errors.append(result)

    if errors:
        raise Exception("Error occured when updating/creating files.", errors)


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
