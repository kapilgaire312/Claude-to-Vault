import asyncio
from pathlib import Path

import aiofiles
import frontmatter


async def get_exiting_note(file_path, chat_id, existing_files, message_length_list):
    async with aiofiles.open(file=file_path, mode="r") as f:
        contents = await f.read()

    # the frontmatter only lets to load synchronously

    try:
        note = frontmatter.loads(contents)
        if note["chat_id"] == chat_id:
            existing_file = f"file path:{file_path}\n Contents:\n{contents}"
            existing_files.append(existing_file)
            message_length_list.append(note["message_length"])
    except Exception:
        print(contents)


async def get_exiting_notes(chat_id):
    root_folder = Path("./Vault")
    existing_files = []
    message_length_list = []

    tasks = [
        get_exiting_note(file_path, chat_id, existing_files, message_length_list)
        for file_path in root_folder.rglob("*.md")
    ]

    await asyncio.gather(*tasks)

    return {
        "files": "\n\n".join(existing_files),
        "max_message_length": max(message_length_list, default=None),
    }
