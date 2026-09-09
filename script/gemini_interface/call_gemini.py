import asyncio
import os

from dotenv import load_dotenv
from google import genai
from google.genai._gaos.types.interactions import Interaction
from pydantic import BaseModel

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


async def call_gemini(
    prompt: str, system_prompt: str, response_schema: type[BaseModel]
):
    generation_config = {
        "response_mime_type": "application/json",
        "temperature": 0.2,
        "response_schema": response_schema.model_json_schema(),
    }
    interaction: Interaction = await client.aio.interactions.create(
        model="gemini-3.5-flash",
        input=prompt,
        system_instruction=system_prompt,
        generation_config=generation_config,
    )

    print(interaction.output_text)
    return interaction.output_text


class TestResponse(BaseModel):
    response: str


async def main():
    await call_gemini(
        prompt="Give me a quick review of the moon.",
        system_prompt="You are a sarcastic robot from space.",
        response_schema=TestResponse,
    )


if __name__ == "__main__":
    asyncio.run(main())
