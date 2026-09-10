import asyncio
from pathlib import Path

import aiofiles

LINES_TO_READ = 15


async def get_file_path_and_lines(file_path):
    print(file_path)
    async with aiofiles.open(file=file_path, mode="r") as f:
        lines = []
        for _ in range(LINES_TO_READ):
            line = await f.readline()

            if not line:
                break
            lines.append(line)

    return f" {str(file_path)} =>  \n{''.join(lines)}"


async def get_vault_files_info():
    """
    Iterate over all the files in Vault folder ending with .md to extract the file pathe and first 15 lines.

    """

    root_folder = Path("./Vault/")

    tasks = [
        get_file_path_and_lines(file_path) for file_path in root_folder.rglob("*.md")
    ]

    results = await asyncio.gather(*tasks)

    return "\n\n".join(results)
