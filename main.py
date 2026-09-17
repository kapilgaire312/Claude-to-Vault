import asyncio
import os
import sys

from dotenv import load_dotenv

from script.config.logger import initialize_root_logger
from script.note_context import NoteContext
from script.vault_handlers.utils import get_vault_folder_path

load_dotenv()


async def main(chat_url: str):
    logger = initialize_root_logger()

    # check valdity of chat_url
    if not chat_url or not chat_url.startswith("https://claude.ai/share/"):
        logger.critical("Enter a valid claude chat share url.")
        return

    # check if gemini api key is set.
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise Exception("Gemini Api key not set in .env!")
    # check if the vault folder path is set.
    get_vault_folder_path()

    note_context = NoteContext(chat_url)
    try:
        await note_context.scrape_and_set_message_context()
        await note_context.check_and_set_update_attributes()
        await note_context.set_vault_files_info()
        await note_context.set_files_to_modify()
        await note_context.create_notes()

    except Exception as e:
        logger.critical(str(e))


if __name__ == "__main__":
    chat_url = ""
    if len(sys.argv) > 1:
        chat_url = sys.argv[1]

    asyncio.run(main(chat_url))
