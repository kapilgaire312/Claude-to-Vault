import pytest

from script.check_read_existing_notes import get_exiting_notes


@pytest.mark.asyncio
async def test_get_existing_notes():
    result = await get_exiting_notes(123)
    print(result)
    assert result.get("max_message_length") == 4
    pass
