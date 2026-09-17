import asyncio

import aiofiles
import frontmatter
import logging

from script.vault_handlers.utils import get_vault_folder_path

VAULT_FOLDER = get_vault_folder_path()

logger = logging.getLogger(__name__)

async def get_exiting_note(file_path, chat_id, existing_files, message_length_list):
    async with aiofiles.open(file=file_path, mode="r") as f:
        contents = await f.read()

    # the frontmatter only lets to load synchronously

    try:
        note = frontmatter.loads(contents)
        if note.get("chat_id") == chat_id:
            file_path_to_send = file_path.relative_to(VAULT_FOLDER)
            existing_file = f"file path:{file_path_to_send}\n Contents:\n{contents}"
            existing_files.append(existing_file)
            message_length_list.append(note["message_length"])
    except Exception as e:
        logger.warning("Error occurred while reading existing note: %s \n skipping file: %s", e, file_path)
        #TODO: handle exception properly, maybe exit the program or log the error and continue. For now, just logging and continuing.


async def get_exiting_notes(chat_id):
    existing_files = []
    message_length_list = []

    tasks = [
        get_exiting_note(file_path, chat_id, existing_files, message_length_list)
        for file_path in VAULT_FOLDER.rglob("*.md")
    ]

    await asyncio.gather(*tasks)

    return {
        "files": "\n\n".join(existing_files),
        "max_message_length": max(message_length_list, default=None),
    }
