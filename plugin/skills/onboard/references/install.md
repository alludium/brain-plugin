# Connect the right assistant

Use the host already known; ask which app only when necessary. These instructions help the
person connect themselves or prepare a message for colleagues. Drafting a message does not
permit sending it. The current customer guide is
https://app.brain.alludium.ai/help/start/connect-your-ai.md.

## Claude app

Under Customize → Plugins, add marketplace `alludium/brain-plugin` and install Alludium Brain.
Open its Connectors tab, choose Connect and sign in with the work account. On Team or Enterprise,
a Claude Owner must allow the connector first; use the firm's existing installation if provided.
Do not add a second custom connector to the same server.

## Claude Code

Run `claude plugin marketplace add alludium/brain-plugin`, then
`claude plugin install brain@alludium-brain --scope user`.
Use `/mcp`, select `plugin:brain:alludium-brain` and Authenticate. Reload plugins or start a new
session if needed. Keep the plugin connection rather than creating a duplicate.

## Codex desktop

For current onboarding before directory availability, use the downloadable plugin ZIP:
https://github.com/alludium/brain-plugin/raw/refs/heads/main/downloads/brain.zip

Ask the person to download it without unpacking, open Plugins in Codex desktop and select the
ZIP through the manual installation option. Do not invent a precise button label if their app
uses different wording. If the option is missing, ask them to contact hello@alludium.ai with
their app version. Connect the plugin's MCP server, complete browser sign-in, and start a new
chat. The ZIP brings both skills and tools. Do not route a desktop user through standalone
`codex mcp add` as though it installs the plugin, or tell them marketplace approval is needed
to use the ZIP. For updates, use the latest ZIP with the app's update or replacement flow.

## Codex CLI or IDE without the desktop plugin

`codex mcp add alludium-brain --url https://app.brain.alludium.ai/mcp`, then
`codex mcp login alludium-brain`, connects the tools. It does not install the plugin skills.
Skip this if the plugin already supplies the connection. Start a new session after connecting.

## Check sign-in, then onboard

The person signs in with their work account and chooses the intended firm. Once the tools are
available, `configure` with `account: {}` returns their identity and workspace. Resolve a wrong
account before filing anything. Then they can say "Onboard me to Alludium Brain". Downloading,
installing, signing in and confirming the account are separate steps; report only what was verified.

## Existing files and custom integrations

The separate Brain CLI calls the same tools from code, keeping bulk source text out of chat.
Installation and preview steps: https://app.brain.alludium.ai/help/feed/cli.md.
Download its wheel from https://github.com/alludium/brain-plugin/tree/main/downloads,
install with `uv tool install ./alludium_brain_cli-<version>-py3-none-any.whl`, and run `brain login`.
It needs Python 3.12+ and an OS keyring. CLI sign-in is separate from the assistant's plugin.

For an Obsidian folder, begin with `brain upload /path/to/vault --namespace research-vault --dry-run`.
Uploads default private. Keep namespace stable; changed files are additional snapshots, not
replacement or deletion sync. A success receipt isn't proof processing finished: check `brain jobs`.
For Notion or a tailored integration, hello@alludium.ai can arrange access to the private starter
repository. Do not present it as a public download. Confirm source selection and audience before
writing; never copy another host's OAuth credentials or put original source contents in chat.
