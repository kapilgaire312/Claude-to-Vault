import asyncio
import os
from pathlib import Path

import aiofiles
from dotenv import load_dotenv

load_dotenv()

VAULT_FOLDER = os.getenv("VAULT_FOLDER")
if not VAULT_FOLDER:
    raise Exception("Vault Folder not set in .env")


root_folder_path = Path(VAULT_FOLDER)


async def get_file_path_and_lines(file_path: Path, lines_to_read):
    async with aiofiles.open(file=file_path, mode="r") as f:
        lines = []
        for _ in range(lines_to_read):
            line = await f.readline()

            if not line:
                break
            lines.append(line)

    file_path_to_send = file_path.relative_to(root_folder_path)
    return f" {str(file_path_to_send)} =>  \n{''.join(lines)}"


async def get_vault_files_info(lines_to_read):
    """
    Iterate over all the files in Vault folder ending with .md to extract the file pathe and first 15 lines.

    """

    tasks = [
        get_file_path_and_lines(file_path, lines_to_read)
        for file_path in root_folder_path.rglob("*.md")
    ]

    results = await asyncio.gather(*tasks)

    return "\n\n".join(results)


async def main():
    res = await get_vault_files_info(20)
    print(res)


if __name__ == "__main__":
    asyncio.run(main())
