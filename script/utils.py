import json
import logging
from pathlib import Path

import aiofiles

logger = logging.getLogger(__name__)


async def save_response_to_temp_file(response):
    response_contents = json.dumps(response)
    try:
        async with aiofiles.open("./response.json.tmp", mode="w") as f:
            await f.write(response_contents)

    except Exception as e:
        # don't block the file write if this fails.
        logger.warning("Failed to save backup. Continuing...")
        logger.warning(e)
        pass


def delete_response_temp_file():
    file_path = Path("./response.json.tmp")
    file_path.unlink(missing_ok=True)
