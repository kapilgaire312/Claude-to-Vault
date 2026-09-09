import json

from pydantic import BaseModel

from script.gemini_interface.call_gemini import call_gemini
from script.gemini_interface.system_instructions import (
    system_instructions_for_file_paths,
)
from script.gemini_interface.user_prompt import get_user_prompt_for_file_paths
from script.gemini_interface.utils import remove_json_markdown


class FilePathResponse(BaseModel):
    existing_files_to_update: list[str]
    new_files_to_create: list[str]


async def get_files_to_modify_from_gemini(
    vault_files_info: str, messages: str
) -> dict[str, list[str]]:
    system_instructions = system_instructions_for_file_paths
    user_prompt = get_user_prompt_for_file_paths(vault_files_info, messages)

    response = await call_gemini(
        prompt=user_prompt,
        system_prompt=system_instructions,
        response_schema=FilePathResponse,
    )

    if response:
        if response.startswith(("```json", "```")):
            response = remove_json_markdown(response)
        parsed_response = json.loads(response)
        print(parsed_response)
        return parsed_response

    raise Exception("Faield to get response from gemini.")
