import json
from pathlib import Path

import aiofiles


async def save_response_to_temp_file(response):
    response_contents = json.dumps(response)
    try:
        async with aiofiles.open("./response.json.tmp") as f:
            await f.write(response_contents)

    except Exception:
        # don't block the file write if this fails.
        print("Failed to save backup. Continuing...")
        pass


def delete_response_temp_file():
    file_path = Path("./response.json.tmp")
    file_path.unlink(missing_ok=True)
