# Claude to Vault

Claude to Vault converts shared Claude conversations into organized Markdown notes for a personal knowledge vault.

It uses Playwright to read a Claude conversation, Gemini to identify the important technical concepts and decide where they belong, and Python to create or update the corresponding notes.

## Features

- Scrapes user and Claude messages from a shared conversation
- Detects whether a conversation has already been processed
- Routes concepts to existing notes or new notes
- Generates structured Markdown notes with Gemini
- Preserves existing content under `# Manual Notes`
- Organizes notes into language, framework, and general concept categories
- Connects related notes with Markdown wikilinks

## Workflow

1. Open a shared Claude conversation in a browser.
2. Extract the conversation messages in order.
3. Check the vault for notes generated from the same conversation.
4. Build an index of the existing Markdown notes.
5. Ask Gemini which notes should be updated or created.
6. Generate the Markdown content for each selected note.
7. Write the notes to the configured vault directory.

## Requirements

- Python 3.13 or newer
- [uv](https://docs.astral.sh/uv/)
- A Google Gemini API key
- A local Markdown vault
- Chromium for Playwright

## Installation

Install the project dependencies:

```bash
uv sync
uv run playwright install chromium
```

## Configuration

Create a `.env` file in the project root:

```dotenv
GEMINI_API_KEY=your_gemini_api_key
VAULT_FOLDER=/absolute/path/to/your/vault
```

`GEMINI_API_KEY` is used for note routing and Markdown generation. `VAULT_FOLDER` points to the local directory where notes are read and written.

The `.env` file and the `Vault/` directory are excluded from Git because they may contain secrets or private notes.

## Usage

Run the application with a Claude share URL:

```bash
uv run python main.py https://claude.ai/share/your-conversation-id
```

The browser runs visibly. If Claude presents a security verification step, complete it in the browser and continue when prompted in the terminal.

## Vault Structure

Claude to Vault breaks a single long conversation into smaller, focused concept notes instead of saving the entire conversation as one document. Related notes are connected with Markdown wikilinks, creating a navigable knowledge graph across the vault.

The generated Markdown notes can be opened locally in [Obsidian](https://obsidian.md/) or published as a website with [Quartz](https://quartz.jzhao.xyz/).

Gemini organizes notes into three categories:

```text
Languages/<language>/<topic>.md
Frameworks/<framework>/<topic>.md
Concepts/<topic>.md
```

Generated notes include metadata describing the source conversation:

```yaml
---
chat_id: "..."
chat_url: "https://claude.ai/share/..."
message_length: 12
---
```

New notes include a `# Manual Notes` section. When an existing note is updated, content in that section is preserved.

## Project Structure

```text
.
├── main.py
├── pyproject.toml
├── script/
│   ├── note_context.py
│   ├── scraper/
│   │   └── claude_chat_scraper.py
│   ├── gemini_interface/
│   │   ├── call_gemini.py
│   │   ├── get_file_paths_to_modify_from_gemini.py
│   │   └── get_markdown_note.py
│   ├── vault_handlers/
│   │   ├── check_read_existing_notes.py
│   │   ├── get_vault_files_data.py
│   │   ├── get_content_for_files_to_modify.py
│   │   └── update_and_create_files_with_contents.py
│   └── tests/
└── Vault/
```

## Testing

Run the tests with:

```bash
PYTHONPATH=. uv run pytest
```

## Development Status

This project is under active development. The current workflow is focused on Claude share pages, Gemini-powered note routing, and Markdown vault management.
