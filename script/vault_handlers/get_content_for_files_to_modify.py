import asyncio
import json
import os
from pathlib import Path

import aiofiles
from dotenv import load_dotenv

from script.gemini_interface import get_md_note
from script.vault_handlers.utils import (
    add_metadata_to_md,
    split_main_content_and_manual_notes,
)

load_dotenv()
MANUAL_NOTES_DELIMITER = "# Manual Notes"
VAULT_FOLDER = os.getenv("VAULT_FOLDER")


async def _get_file_to_update(
    file_path,
    is_update,
    vault_file_paths_str,
    chat_messages,
    meta_data,
):
    if not VAULT_FOLDER:
        raise Exception("Vault Folder not set in .env")

    full_file_path = Path(VAULT_FOLDER) / file_path
    async with aiofiles.open(full_file_path) as file:
        contents = await file.read()

    main_content, manual_notes = split_main_content_and_manual_notes(
        contents, MANUAL_NOTES_DELIMITER
    )
    # call gemini with main_content
    response = await get_md_note(
        note_update=is_update,
        vault_files_to_be_modified=vault_file_paths_str,
        current_file_path=file_path,
        chat_messages=chat_messages,
        existing_note_content=main_content,
    )
    print("got response")

    if not response:
        raise Exception("Response is none.")

    # get the markdown response and append back manual_notes
    # add the title of manual notes
    response += "\n\n"
    response += MANUAL_NOTES_DELIMITER

    # add back previous notes
    response += manual_notes

    # add metadata
    md_with_metadata = add_metadata_to_md(response, metadata=meta_data)
    return {"file_path": file_path, "note": md_with_metadata}


async def _get_file_to_create(
    file_path,
    is_update,
    vault_file_paths_str,
    chat_messages,
    meta_data,
):
    response = await get_md_note(
        note_update=is_update,
        vault_files_to_be_modified=vault_file_paths_str,
        current_file_path=file_path,
        chat_messages=chat_messages,
    )

    if not response:
        raise Exception("Response is none.")

    # add manual notes title at last

    response += "\n\n"
    response += MANUAL_NOTES_DELIMITER
    md_with_metadata = add_metadata_to_md(response, metadata=meta_data)
    return {"file_path": file_path, "note": md_with_metadata}


async def get_content_for_files_to_modify(
    file_paths: dict[str, list[str]],
    is_update: bool,
    chat_messages: str,
    meta_data: dict[str, str | int],
):
    if not file_paths:
        raise Exception("No file paths present.")

    vault_file_paths_str = json.dumps(file_paths)

    update_note_tasks = []
    create_new_note_tasks = []

    # get the file content of files to update
    files_to_update = file_paths.get("existing_files_to_update")
    print("files to update are", files_to_update)

    if files_to_update:
        update_note_tasks.extend(
            [
                _get_file_to_update(
                    file_path,
                    is_update=is_update,
                    vault_file_paths_str=vault_file_paths_str,
                    chat_messages=chat_messages,
                    meta_data=meta_data,
                )
                for file_path in files_to_update
            ]
        )

    files_to_create = file_paths.get("new_files_to_create")
    if files_to_create:
        create_new_note_tasks.extend(
            _get_file_to_create(
                file_path,
                is_update=is_update,
                vault_file_paths_str=vault_file_paths_str,
                chat_messages=chat_messages,
                meta_data=meta_data,
            )
            for file_path in files_to_create
        )
    if not update_note_tasks and not create_new_note_tasks:
        raise Exception("No notes needs to be created/updated.")

    # TODO: add optimizations here for the free teir of gemini, maybe call gemini one at a time with delay inbetween instead of gathering.
    # impelemt all or nothing strategy here, if a single gemini call fails, retry it or abort all.
    notes_response = await asyncio.gather(*create_new_note_tasks, *update_note_tasks)
    print(notes_response[0].get("note")[:100])
    return notes_response
