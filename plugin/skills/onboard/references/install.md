# Connect Alludium Brain

The default setup is the remote MCP connection at https://app.brain.alludium.ai/mcp with OAuth. Brain supplies core
operating skills and the firm's own skills through `configure(skill="<name>")`, including
reference files. No separate plugin or skills installation is needed. Reuse an existing working
connection to this address, including a plugin connection; do not add duplicates or silently
change environments.

## Claude Web, Desktop and Cowork

Customize → Connectors → Add custom connector: name Alludium Brain, URL https://app.brain.alludium.ai/mcp, detected
OAuth settings, Connect. On Team or Enterprise an Owner or authorized administrator first adds
it under Organization settings → Connectors → Add → Custom → Web. Every member signs in with
their own account. Remote connectors connect from Anthropic's cloud, including in Desktop:
a loopback or private-network server is not reachable directly.

## Claude Code

Reuse an existing connection, including a synced one. Otherwise add
`claude mcp add --transport http --scope user alludium-brain https://app.brain.alludium.ai/mcp` and let the user
authenticate through `/mcp`. Preserve other configuration.

## ChatGPT Web and desktop

Plugins → Add → Add custom MCP server. Name Alludium Brain, URL https://app.brain.alludium.ai/mcp, OAuth. The user
reviews the warning, selects Create as a plugin, installs it when prompted and signs in.
This is a custom MCP connection, not a ZIP upload. Organization permissions can require an admin.
Respect Desktop only labels on imported packages; they are not the default web route.

## Codex desktop, CLI and IDE

Settings → MCP servers → Add server: Streamable HTTP, URL https://app.brain.alludium.ai/mcp. Save, restart when
prompted and Authenticate. Or `codex mcp add alludium-brain --url https://app.brain.alludium.ai/mcp`, then
`codex mcp login alludium-brain`. Explain the settings change first and preserve other entries.
These local Codex surfaces share configuration on the same host.

## Hermes and other assistants

Use the host's remote MCP settings and OAuth. In Hermes, merge the alludium-brain entry with
`url: "https://app.brain.alludium.ai/mcp"` and `auth: oauth` into the active profile, then run
`hermes mcp login alludium-brain` in that profile. Keep the gateway in the same profile. Never
copy tokens from another host or paste credentials into Discord. For Discord trials use a private
DM/test server restricted to the user; channel readers can still see replies.

## Verify before onboarding

Let the user sign in; never claim success from a download or a sign-in page alone. Start a fresh
session if tools are missing. Read `configure(account={})` and verify person, workspace and the
intended endpoint. Keep the returned workspace_context on subsequent calls. Read `configure`
to discover skills, load `configure(skill="core:onboard")`, then `configure(onboarding=true)` and
follow the live state and permissions. Do not file, import or share during a connection check.

Other services such as calendar, mail and meeting tools need their own connections. The Brain CLI
for bulk/scripted imports also has separate installation and sign-in: https://app.brain.alludium.ai/help/feed/cli.md.
Use `brain --server https://app.brain.alludium.ai/mcp login` and pass that same `--server https://app.brain.alludium.ai/mcp` on subsequent
CLI commands, including imports. Never silently substitute the default hosted server for this environment.

## Optional plugin

For native skill discovery, the package remains available at https://github.com/alludium/brain-plugin and
https://github.com/alludium/brain-plugin/raw/refs/heads/main/downloads/brain.zip. Marketplace source: alludium/brain-plugin. Plugins are optional distribution;
public approval is distinct from custom installation. A working plugin connection should be reused.
