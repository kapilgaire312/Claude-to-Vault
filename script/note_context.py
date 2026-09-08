from dataclasses import dataclass, field

from script.check_read_existing_notes import get_exiting_notes
from script.claude_chat_scraper import scrape_claude_chat
from script.get_vault_files_data import get_vault_files_info


@dataclass()
class NoteContext:
    chat_url: str
    chat_id: str | None = None
    chat_messages: list[dict[str, str]] = field(default_factory=lambda: [])
    total_message_length: int = 0

    # contains all the note files path and first 15 lines of each file.
    # to prevent same topic creating multiple notes.
    vault_files_info: str = ""

    # if the same chat has been processed previously, then we may need to update
    # the existing notes along.
    # flags for update
    update_flag: bool = False
    # concatenate all the notes having the same chat_id
    existing_notes_of_chat: str = ""
    # the max message length in the metadata of already created notes.
    max_cutoff_message_length: int = 0

    async def set_chat_context(self):
        messages = await scrape_claude_chat(self.chat_url)

        if not messages:
            raise Exception("No chat retrieved from the scraper.")

        self.chat_messages = messages
        self.total_message_length = len(messages)
        self.chat_id = self.chat_url.split("/").pop()

    async def set_vault_files_info(self):
        files_data = await get_vault_files_info()
        self.vault_files_info = files_data

    async def check_and_set_update_attributes(self):
        result = await get_exiting_notes(self.chat_id)

        if result.get("max_message_length") is None:
            # no files found to update.
            return

        if result.get("max_message_length",0) > self.total_message_length:
            raise Exception("The cutoff range can't be greater than total message. Maybe the scraping is partial.")

        # set update attributes
        self.update_flag = True
        self.max_cutoff_message_length = result.get("max_message_length", 0)
        self.existing_notes_of_chat = result.get("files", "")
