from dataclasses import dataclass, field

from script.claude_chat_scraper import scrape_claude_chat
from script.get_vault_files_data import get_vault_files_info


@dataclass()
class NoteContext:
    chat_url: str
    chat_id: str | None = None
    chat_messages: list[dict[str, str]] = field(default_factory=lambda: [])
    total_message_length: int = 0

    # contains all the note files path and first 15 lines of each file.
    vault_files_info: str = ""

    async def set_chat_context(self):
        messages = await scrape_claude_chat(self.chat_url)

        if not messages:
            raise Exception("No chat retrieved from the scrapet.")

        self.chat_messages = messages
        self.total_message_length = len(messages)
        self.chat_id = self.chat_url.split("/").pop()

    async def set_vault_files_info(self):
        files_data = await get_vault_files_info()
        self.vault_files_info = files_data
