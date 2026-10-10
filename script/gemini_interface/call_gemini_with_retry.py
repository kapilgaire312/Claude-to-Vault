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

        except (APIError, asyncio.TimeoutError) as e:
            if isinstance(e, asyncio.TimeoutError):
                err_msg = "Gemini request timed out."
                error_message = str(e)
            else:
                err_msg = (
                    "429 Rate Limit Triggered!"
                    if e.status_code == 429
                    else "API error occured."
                )
                error_message = e.message

            logger.warning(err_msg)
            logger.warning("Error Message: %s", error_message)

            if i < max_tries - 1:
                logger.info("Retrying after Gemini error...")
                await asyncio.sleep(delay)
            delay *= 2

    raise Exception("Retries were exhausted. Gemini requests still failed.")


async def main():
    # unit test for call_gemini_with_retry
    await call_gemini_with_retry(
        user_prompt="What is the weather like today?",
        system_prompt="You are a helpful assistant.",
    )
    print("call_gemini_with_retry test passed.")


if "__name__" == "__main__":
    asyncio.run(main())
