import json
from dataclasses import dataclass, field

from script.check_read_existing_notes import get_exiting_notes
from script.claude_chat_scraper import scrape_claude_chat
from script.gemini_interface.get_file_paths_to_modify_from_gemini import (
    get_files_to_modify_from_gemini,
)
from script.get_content_for_files_to_modify import get_content_for_files_to_modify
from script.get_vault_files_data import get_vault_files_info
from script.update_and_create_files_with_contents import (
    update_and_create_files_with_content,
)


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

    ###
    # files that needs to be updated or created for the chat messages
    files_to_modify: dict[str, list[str]] = field(default_factory=lambda: {})

    # method which calls the scraper and sets the initial attributes of the class.
    async def set_chat_context(self):
        messages = await scrape_claude_chat(self.chat_url)

        if not messages:
            raise Exception("No chat retrieved from the scraper.")

        self.chat_messages = messages
        self.total_message_length = len(messages)
        self.chat_id = self.chat_url.split("/").pop()

    # method which extracts all file paths and first 15 lines inside them to store in vault_files_info
    async def set_vault_files_info(self):
        files_data = await get_vault_files_info()
        self.vault_files_info = files_data

    # method which checks if this chat has made notes in the vault and sets the update attributes if it has.
    async def check_and_set_update_attributes(self):
        result = await get_exiting_notes(self.chat_id)

        if result.get("max_message_length") is None:
            # no files found to update.
            return

        if result.get("max_message_length", 0) > self.total_message_length:
            print(result.get("max_message_length"), self.total_message_length)
            raise Exception(
                "The cutoff range can't be greater than total message. Maybe the scraping is partial."
            )

        # set update attributes
        self.update_flag = True
        self.max_cutoff_message_length = result.get("max_message_length", 0)
        self.existing_notes_of_chat = result.get("files", "")

    # router that calls gemini to get the files to update and create for this part of chat messages.
    async def set_files_to_modify(self):
        messages = (
            self.chat_messages[self.max_cutoff_message_length - 1 :]
            if self.update_flag
            else self.chat_messages
        )
        print(messages)
        messages_string = json.dumps(messages)
        response = await get_files_to_modify_from_gemini(
            vault_files_info=self.vault_files_info, messages=messages_string
        )

        self.files_to_modify = response
        # TODO check validity of file paths and create absolute path by merging with VAULT_PATH for update.

    async def create_notes(self):
        # loop through the files_to_modify and call gemini for each path to update the note.
        print("creating notes...")
        messages = (
            self.chat_messages[self.max_cutoff_message_length - 1 :]
            if self.update_flag
            else self.chat_messages
        )
        # convert messages to string
        messages_string = json.dumps(messages)
        # construct meta_data
        meta_data = {
            "chat_id": self.chat_id,
            "chat_url": self.chat_url,
            "message_length": self.total_message_length,
        }
        file_path_and_note: list[
            dict[str, str]
        ] = await get_content_for_files_to_modify(
            is_update=self.update_flag,
            file_paths=self.files_to_modify,
            chat_messages=messages_string,
            meta_data=meta_data,
        )

        # TODO: add a safetynet here to save all the content of file_path_and_note to a file
        # in case the below operation fails, which will make the above expnsive gemini call go waste.
        # the user can check what went wrong and manually add the md file to the notes.

        # Update/create files
        await update_and_create_files_with_content(file_path_and_note)
        # TODO if this throws exception, catch it and retry
        # else implement all or nothing model, if even a single file update/creat fails rollback.
