import logging
import os
import re
from pathlib import Path

import frontmatter
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def split_main_content_and_manual_notes(contents: str, delimiter: str):
    if delimiter in contents:
        parts = contents.split(delimiter, 1)
        main_content = parts[0].strip()
        manual_notes = parts[1].strip()

    else:
        main_content = contents.strip()
        manual_notes = ""

    return main_content, manual_notes


def add_metadata_to_md(md_file: str, metadata: dict[str, str | int]):
    post = frontmatter.loads(md_file)
    #read the sources metadata and loop through it to check if the chat_id already exists, if it does then update the message_length, if not then append a new source with the chat_id and message_length
    sources = post.get("sources", [])
    chat_id = metadata.get("chat_id")
    message_length = metadata.get("message_length")
    if chat_id is not None and message_length is not None:
        for source in sources:
            if source.get("chat_id") == chat_id:
                source["message_length"] = message_length
                break
        else:
            sources.append({"chat_id": chat_id, "message_length": message_length})
            
    post["sources"] = sources
    return frontmatter.dumps(post)


def get_vault_folder_path() -> Path:
    load_dotenv()
    VAULT_FOLDER = os.getenv("VAULT_FOLDER")

    if not VAULT_FOLDER:
        raise Exception("Vault Folder not set in .env")

    vault_folder_path = Path(VAULT_FOLDER)

    if not vault_folder_path.is_dir():
        raise Exception("VAULT_FOLDER path is not valid! Add a valid folder path.")

    return vault_folder_path


def is_file_path_structure_valid(file_path):
    pattern = r"^(?:Languages/[^/]+/[^/]+|Frameworks/[^/]+/[^/]+|Concepts/[^/]+)\.md$"
    # allowed structure patterns:
    # Languages/<language>/<topic>.md
    # Frameworks/<framework>/<topic>.md
    # Concepts/<topic>.md
    #
    is_valid = re.match(pattern=pattern, string=file_path)

    if is_valid is None:
        return False

    else:
        return True
