import asyncio
import os

from dotenv import load_dotenv
from google import genai
from google.genai._gaos.types.interactions import Interaction

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

generation_config = {"response_mime_type": "application/json", "temperature": 0.3}


async def call_gemini(prompt: str, system_prompt: str):
    interaction: Interaction = await client.aio.interactions.create(
        model="gemini-3.5-flash",
        input=prompt,
        system_instruction=system_prompt,
        generation_config=generation_config,
    )

    print(interaction.output_text)
    return interaction.output_text


async def main():
    await call_gemini(
        prompt="Give me a quick review of the moon.",
        system_prompt="You are a sarcastic robot from space.",
    )


if __name__ == "__main__":
    asyncio.run(main())
