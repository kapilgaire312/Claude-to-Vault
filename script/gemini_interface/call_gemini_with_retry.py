import asyncio
import logging

from google.genai._gaos.lib.compat_errors import APIError
from pydantic import BaseModel

from script.gemini_interface import call_gemini

logger = logging.getLogger("__name__")


async def call_gemini_with_retry(
    user_prompt: str,
    system_prompt: str,
    response_schema: type[BaseModel] | None = None,
):
    delay = 15
    max_tries = 3

    for i in range(max_tries):
        try:
            response = await call_gemini(
                prompt=user_prompt,
                system_prompt=system_prompt,
                response_schema=response_schema,
            )

            return response

        except APIError as e:
            err_msg = (
                "429 Rate Limit Triggered!"
                if e.status_code == 429
                else "API error occured."
            )
            logger.warning(err_msg)
            logger.warning("Error Message: %s", e.message)

            if i < max_tries - 1:
                logger.info("Retrying after API error...")

                await asyncio.sleep(delay)
            # using exponential delay to wait for limit to expire.
            delay *= 2

    raise Exception("Retries were exhausted. API errors still occured.")


async def main():
    # unit test for call_gemini_with_retry
    await call_gemini_with_retry(
        user_prompt="What is the weather like today?",
        system_prompt="You are a helpful assistant.",
    )
    print("call_gemini_with_retry test passed.")


if "__name__" == "__main__":
    asyncio.run(main())
