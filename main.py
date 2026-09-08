import asyncio

from script.note_context import NoteContext


async def main():
    print("Hello from note-taking!")
    note_context = NoteContext(
        "https://claude.ai/share/49eddefd-3a84-4ca9-81af-b9637ad7a3b6"
    )
    await note_context.set_chat_context()
    print(note_context)


if __name__ == "__main__":
    asyncio.run(main())
