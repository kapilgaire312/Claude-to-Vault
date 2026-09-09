import json

from pydantic import BaseModel

from script.gemini_interface.call_gemini import call_gemini
from script.gemini_interface.system_instructions import (
    system_instructions_for_new_note,
    system_instructions_for_note_update,
)
from script.gemini_interface.user_prompt import (
    get_user_prompt_for_new_note,
    get_user_prompt_for_note_update,
)
from script.gemini_interface.utils import remove_json_markdown


class NoteResponse(BaseModel):
    markdown: str


async def get_md_note(
    note_update: bool,
    vault_files_to_be_modified: str,
    current_file_path: str,
    chat_messsages: str,
):
    system_instructions = (
        system_instructions_for_note_update
        if note_update
        else system_instructions_for_new_note
    )

    user_prompt = (
        get_user_prompt_for_note_update(
            vault_files_to_be_modified, current_file_path, chat_messsages
        )
        if note_update
        else get_user_prompt_for_new_note(
            vault_files_to_be_modified, current_file_path, chat_messsages
        )
    )

    response = await call_gemini(
        prompt=user_prompt,
        system_prompt=system_instructions,
        response_schema=NoteResponse,
    )
    print(response)

    if response:
        if response.startswith(("```json", "```")):
            response = remove_json_markdown(response)
        parsed_response = json.loads(response)
        print(parsed_response)
        return parsed_response
