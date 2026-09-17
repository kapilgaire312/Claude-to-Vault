import logging

from script.gemini_interface import call_gemini_with_retry
from script.gemini_interface.system_instructions import (
    system_instructions_for_new_note,
    system_instructions_for_note_update,
)
from script.gemini_interface.user_prompt import (
    get_user_prompt_for_new_note,
    get_user_prompt_for_note_update,
)

logger = logging.getLogger(__name__)


async def get_md_note(
    note_update: bool,
    vault_files_to_be_modified: str,
    current_file_path: str,
    chat_messages: str,
    existing_note_content: str = "",
):
    system_instructions = (
        system_instructions_for_note_update
        if note_update
        else system_instructions_for_new_note
    )

    user_prompt = (
        get_user_prompt_for_note_update(
            vault_files_to_be_modified,
            current_file_path,
            chat_messages,
            existing_note_content,
        )
        if note_update
        else get_user_prompt_for_new_note(
            vault_files_to_be_modified, current_file_path, chat_messages
        )
    )

    response = await call_gemini_with_retry(
        user_prompt=user_prompt,
        system_prompt=system_instructions,
    )
    logger.debug("Markdown note response for %s: %s", current_file_path, response)

    if not response:
        raise Exception("Failed to get Markdown note from Gemini.")

    return response.strip()
