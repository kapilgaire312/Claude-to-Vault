# Claude to Vault

Claude to Vault turns a shared Claude conversation into a small, organized set of technical Markdown notes. It is a personal knowledge-capture pipeline for developers: instead of leaving useful explanations buried in chat history, it distills them into a searchable vault that can be edited in Obsidian or published with Quartz.

The project combines:

- Playwright to read a shared Claude conversation in a real browser.
- Gemini to identify substantive concepts, choose existing notes or new note paths, and write the Markdown.
- Python to inspect the vault, detect previous imports, preserve personal annotations, and safely write the results.

## What Problem It Solves

Technical conversations often contain valuable explanations, examples, corrections, and mental models, but chat transcripts are difficult to revisit. Claude to Vault converts that learning into durable notes while keeping related concepts connected.

For each conversation, the application:

1. Scrapes Developer and AI Tutor messages in their original order.
2. Checks note frontmatter to see whether this conversation was imported before.
3. Reads the existing vault index so related topics can be consolidated rather than duplicated.
4. Asks Gemini which notes to update, create, or link to without changing.
5. Generates one focused Markdown note per selected path.
6. Updates existing notes or creates new ones in the configured vault.

If a conversation has grown since its last import, only the newly available messages are sent for the update. If the conversation is already fully imported, the run stops instead of duplicating content. If the scraper appears to have missed messages, the update is rejected rather than overwriting notes with incomplete information.

## Note Organization

The vault uses three allowed note categories:

```text
Languages/<language>/<topic>.md
Frameworks/<framework>/<topic>.md
Concepts/<topic>.md
```

Paths use kebab-case and are validated before anything is written. Gemini is instructed to consolidate closely related details into one useful concept note. For example, several related C# language features should become one coherent note when they belong together, rather than many tiny files.

Generated notes contain frontmatter identifying their source conversation:

```yaml
---
topic: "..."
tags: [generate, relevant, tags]
chat_id: "..."
chat_url: "https://claude.ai/share/..."
message_length: 12
---
```

Every generated note ends with a `# Manual Notes` section. When a note is updated, the existing content in that section is kept intact, so personal edits are not lost. Related notes are connected with Obsidian-compatible wikilinks such as `[[value-vs-reference-types]]`.

## Requirements

- Python 3.13 or newer
- [uv](https://docs.astral.sh/uv/)
- A Google Gemini API key with access to the configured Gemini model
- A local Markdown vault
- Chromium installed for Playwright
- A shared Claude conversation URL beginning with `https://claude.ai/share/`

## Installation

From the project directory, install the Python dependencies and Playwright browser:

```bash
uv sync
uv run playwright install chromium
```

## Configuration

Create a `.env` file in the project root:

```dotenv
GEMINI_API_KEY=your_gemini_api_key
VAULT_FOLDER=/absolute/path/to/your/markdown-vault
```

`GEMINI_API_KEY` is used for concept routing and note generation. `VAULT_FOLDER` must point to an existing directory. It may be this repository's `Vault/` directory or, more commonly, a separate vault managed by Obsidian.

Keep `.env` private. The repository also ignores `Vault/` because a vault may contain private notes.

## Running the Importer

Pass a Claude share URL as the first argument:

```bash
uv run python main.py https://claude.ai/share/your-conversation-id
```

The browser is intentionally visible. This makes the scraper easier to use with Claude's security checks. If a human-verification page appears, complete it in the browser, return to the terminal, and press Enter when prompted.

The application logs each stage of the pipeline: scraping, duplicate detection, vault indexing, Gemini routing, note generation, and file replacement.

## Safe File Updates and Recovery

Notes are written to temporary `.tmp` files first. They are renamed to their final Markdown paths only after all requested note generations succeed. This prevents a partial batch from leaving a half-updated vault.

Before writing notes, the generated response is also saved as `response.json.tmp` in the project root. If note generation or file replacement fails, inspect that file before retrying. It is deleted after a successful update.

## Using the Vault with Obsidian

1. Open Obsidian and choose **Open folder as vault**.
2. Select the directory configured by `VAULT_FOLDER`.
3. Open any generated note in the editor or graph view.
4. Follow `[[wikilinks]]` to move between related language, framework, and concept notes.
5. Add personal explanations, examples, and reminders below `# Manual Notes`.

Obsidian understands the generated Markdown frontmatter and wikilinks directly. Keep the `# Manual Notes` heading in place so future imports continue to preserve your additions.

## Publishing with Quartz

[Quartz](https://quartz.jzhao.xyz/) can turn the same Markdown vault into a browsable website. A typical setup is:

1. Create or clone a Quartz site.
2. Copy the vault's Markdown folders into the Quartz `content/` directory, or configure Quartz to use the vault as its content source.
3. Build and preview the site with Quartz's documented commands.
4. Deploy the generated site using a supported host such as GitHub Pages, Cloudflare Pages, or another static hosting provider.

Quartz supports Markdown wikilinks, so links such as `[[clr-execution-model]]` become navigation between published notes. Review your vault before publishing: the importer is designed for personal notes and does not remove secrets or private content from a Markdown file.

## Project Layout

```text
.
├── main.py                         # CLI entry point
├── pyproject.toml                  # Dependencies and Python version
├── script/
│   ├── note_context.py             # End-to-end import orchestration
│   ├── scraper/
│   │   └── claude_chat_scraper.py  # Playwright-based Claude scraper
│   ├── gemini_interface/           # Routing and Markdown generation
│   ├── vault_handlers/             # Vault reads, validation, and writes
│   ├── config/                     # Logging setup
│   └── tests/                      # Automated tests
└── Vault/                          # Optional local vault, ignored by Git
```

## Current Scope and Limitations

- The importer currently supports shared Claude conversation pages, not arbitrary chat exports.
- It depends on Claude's current page selectors and may need maintenance if the site changes.
- Gemini decides how to summarize and route content, so generated notes should be reviewed in Obsidian.
- This project creates and updates Markdown files; it does not itself host a website or synchronize a vault.
