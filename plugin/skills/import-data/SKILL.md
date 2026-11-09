---
name: import-data
description: Alludium-owned import guidance, available through the plugin or configure(skill="core:import-data") over MCP. Explain how to bring existing data into Alludium Brain and choose an import route, including local folders, Obsidian, Notion, unsupported systems, custom readers and recurring exports. Use for "how do I get my existing data in?" or "can my coding assistant connect our system?". If the user explicitly requests the Brain onboarding skill, load onboard first, including for import-only advice. For an agreed CRM import, use import-from-crm; for firm or personal setup, use onboard.
---

# Choose an import route

If the user explicitly named another available skill, load it first, even if it delegates import
advice here. Help the person find the simplest supported path. Advice is not an import or an onboarding
interview. Read `search(source_id="help:feed/import-existing-data")`. Finish a broad overview by asking where the data lives and whether they need a one-off import
or updates, unless already stated. Mentioning these choices is not the same as asking.

For a broad question, explain the four routes briefly:

- **Direct connections and supported imports:** supported accounts where enabled, CRM import,
  and firm-managed drives. Availability is unknown until checked: say “where enabled,” not that accounts are enabled or disabled.
- **Assistant filing:** email, meetings and selected Slack threads the assistant can read but
  Brain does not already sync. Manual filing needs the connections; scheduled filing also needs
  a host that supports it. Running with the computer off is optional, not a prerequisite.
- **A few files:** drop documents or use email-in. Email-in shares with the firm.
- **Folders and custom sources:** the separate Brain CLI and private import starter.

For advice about import options, give a short comparison and one relevant follow-up question.
Keep it under about 300 words; link to setup instructions instead of reproducing them. Do not ask
again for a source or one-off/recurring preference the user already supplied.

For a specific source, compare only applicable routes; for Obsidian, compare CLI folder upload
and the starter wizard, after reading the Obsidian guide below. Keep preview and audience rules
inside each route's description. Do not apply one route's sharing, deletion or setup
rules to another. In particular, CRM and direct-account imports do not require installing the CLI.

## Keep the explanation grounded

Answer the question asked, using the maintained guide's stated facts. Leave optional settings,
credential-handling and setup details for a setup request. Do not invent extra steps or menu
locations, and do not turn a documented limit into a guess about workspace availability.
The source-evidence mapping limit applies to CLI/starter imports, not assistant filing of emails
and meetings, which can extract structured facts. For a broad overview, the four routes and the
source/recurrence question are enough; explain details after the person chooses a route.

## CLI and custom-reader handoff

Read `search(source_id="help:feed/cli")`; for Obsidian also read
`search(source_id="help:feed/import-obsidian")`. Keep each route's controls separate: CLI folder
upload has a local dry run and a sharing flag; the Obsidian wizard has audience selection and a
matching preview that sends the selected snapshot to Brain without filing it. The wizard is Obsidian-only; Notion and custom readers use command-line plans and
configured audiences, not wizard controls. Explain this handoff, without executing it for an advice-only question:

1. Download the CLI from the public Brain downloads page, then install and sign in separately from
   the plugin. Private repository access is not needed for the CLI download. A coding assistant may help with
   installation; the user completes authentication. Do not invent a blanket inability to help. The starter is private: ask
   hello@alludium.ai for access, separately from Brain sign-in.
2. For an unsupported system, a coding assistant can adapt a small reader using the CLI and
   starter. Code sends selected original contents directly to Brain; the collection stays out
   of chat. CLI/starter imports preserve source evidence, not automatic structured mappings. Separate Brain
   tools can create structured records; do not call that work manual-only.
3. Use separate steps: preview a small selection; stop to review the files, workspace and
   audience and approve the plan; only then upload. After uploading, check the returned jobs and inspect sources: receipts mean accepted
   transfer, not finished processing. Keep collection/source IDs stable on repeat runs.
4. Recurring scripts need the person's scheduler. CLI/starter imports do not mirror permissions
   or deletions; their private default is not a rule for other import routes.

## Supported CRM or account

Read the relevant help page. In CRM advice, explicitly say the import starts with a reviewed
preview and never writes back. If discussing stages, conflicts need review; there is no automatic rule that an existing later
Brain stage wins. The user's own private CRM notes remain private; colleagues' private notes are
skipped, not imported under a newly chosen audience.
For email/calendar, prefer direct Brain connections where enabled. Assistant filing can also cover
email/calendar when direct sync is unavailable, as well as selected Slack threads and meeting notes.
Scheduled filing needs host support; do not invent host-specific restrictions. Do not inspect configuration or load operational filing instructions just to explain
these options. When the user asks to start or troubleshoot setup, hand off to the corresponding
procedure with their existing choices and authorization; do not repeat an answered question.

## Existing sync and recurring exports

Keep working direct sync and avoid duplicate assistant filing. A scheduled CSV export does not
schedule its upload: the CLI upload needs its own scheduler. Include a small preview, audience
approval and processing-job checks, keeping source identities stable. Ask where the export lands
before assuming its system lacks a supported connection.
