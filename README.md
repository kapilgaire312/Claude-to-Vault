# Note Taking

This project turns shared Claude conversations into organized Markdown notes for a personal knowledge vault.

It uses Playwright to read the conversation, Gemini to identify the important technical concepts and decide where they belong, and Python to create or update the corresponding notes in the vault.

The workflow is:

1. Read a shared Claude conversation.
2. Check the vault for related notes or notes created from the same conversation.
3. Ask Gemini which notes should be created or updated.
4. Generate structured Markdown notes from the conversation.
5. Save the notes to the vault while preserving existing manual notes.

Notes are organized into three categories:

```text
Languages/<language>/<topic>.md
Frameworks/<framework>/<topic>.md
Concepts/<topic>.md
```

The goal is to build a personal, searchable knowledge base from conversations and learning sessions without manually restructuring every discussion into notes.
