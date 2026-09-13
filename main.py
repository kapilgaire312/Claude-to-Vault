import asyncio
import os
import sys

from dotenv import load_dotenv

from script.note_context import NoteContext
from script.vault_handlers.utils import get_vault_folder_path

DEFAULT_CHAT_URL_FOR_TEST = (
    "https://claude.ai/share/49eddefd-3a84-4ca9-81af-b9637ad7a3b6"
)

load_dotenv()


async def main(chat_url: str):
    # check if gemini api key is set.
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise Exception("Gemini Api key not set in .env!")
    # check if the vault folder path is set.
    get_vault_folder_path()

    note_context = NoteContext(chat_url)
    await note_context.scrape_and_set_message_context()
    await note_context.check_and_set_update_attributes()
    await note_context.set_vault_files_info()
    await note_context.set_files_to_modify()
    await note_context.create_notes()


if __name__ == "__main__":
    chat_url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CHAT_URL_FOR_TEST
    asyncio.run(main(chat_url))
