import asyncio
import os
from pathlib import Path
from typing import Coroutine

import frontmatter
from dotenv import load_dotenv
from google.genai import errors


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
    post.metadata.update(metadata)
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


async def call_task_with_retry(task: Coroutine, max_tries: int):
    delay = 10
    for i in range(max_tries):
        try:
            response: dict[str, str] = await task
            return response

        except errors.APIError as e:
            err_msg = (
                "429 Rate Limit Triggered!" if e.code == 429 else "API error occured."
            )
            print(err_msg)
            print(f"Error Message: {e.message}")

            if i < max_tries - 1:
                print("Retrying...")

            await asyncio.sleep(delay)
            # using exponential delay to wait for limit to expire.
            delay *= 2

    raise Exception("Retries were exhausted. Rate Limit still occured.")
