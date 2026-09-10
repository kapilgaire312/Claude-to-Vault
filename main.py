import asyncio
import sys

from script.note_context import NoteContext

DEFAULT_CHAT_URL = "https://claude.ai/share/49eddefd-3a84-4ca9-81af-b9637ad7a3b6"

async def main(chat_url: str):
    print("Hello from note-taking!")
    note_context = NoteContext(chat_url)
    await note_context.scrape_and_set_message_context()
    await note_context.check_and_set_update_attributes()
    await note_context.set_vault_files_info()
    await note_context.set_files_to_modify()
    await note_context.create_notes()
    print(note_context.vault_files_info)


if __name__ == "__main__":
    chat_url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CHAT_URL
    asyncio.run(main(chat_url))
