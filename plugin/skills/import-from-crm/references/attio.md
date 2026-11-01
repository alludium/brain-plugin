# Attio (untested)

For Attio's hosted connector (`https://mcp.attio.com/mcp`; tools such as `whoami`,
`list-lists`, `list-records-in-list`, `search-notes-by-metadata`, `search-meetings`). Written
from Attio's MCP documentation (docs.attio.com/mcp, October 2026); never run against a real
workspace. Attio documents tool names but not their parameters or output fields, so check
each call's result against this file. If a tool named here is missing or a field cannot be
found, stop and say which, rather than guess.

Read tools run without confirmation; write tools ask. Never call one: no `create-`,
`update-`, `delete-` or `merge-` tool, whatever the user says during an import.

`system: "attio"`. Source ID prefixes: `company:`, `person:`, `deal:`, `note:`, `meeting:`.
Attio record IDs are UUIDs and are not unique across objects, so the prefix matters.

## Setup, links and firm members

- `whoami` gives the user and workspace. Use the record's `web_url` as its page when a
  result includes one. Otherwise build `https://app.attio.com/<workspace slug>/<object
  slug>/<record id>` (the pattern is documented; the `company` and `deal` object slugs are
  inferred) if `whoami` returns the workspace slug, and leave `url` out if it does not.
  Notes and meetings use the page of the record they were fetched for.
- Firm members: `list-workspace-members` (their emails), with the skill's email-domain rule.

## Choosing the records

- A list: `list-lists`, filtered by name; its entry attributes from
  `list-list-attribute-definitions` (the status attribute and its options); the entries with
  `list-records-in-list`, which returns each entry with its parent record. A list the user
  cannot see in Attio is invisible here too.
- The deals object (an admin may have turned it on): `list-attribute-definitions` for deals
  gives the `stage` status options (default Lead, In Progress, Won, Lost); `list-records` with
  a filter on `stage`. A deal names its company through a record-reference attribute; capture
  the deal as the record (`deal:<id>`) and link its company by name and domain.
- Named companies: `search-records` on companies.

Attio does not document the order of status options. Show them in the order returned and
confirm the mapping with the user, without assuming that order is the pipeline's.

## Counting (dry run)

No count call is documented. Count notes with `search-notes-by-metadata` on the parent
record (metadata only, never `get-note-body`), and meetings with `search-meetings` on the
related record over the window. Stop counting a record at 50 of either and show "50+".

## Fetching (import)

- Notes: `search-notes-by-metadata` for the record (newest first if the tool can sort),
  then `get-note-body` for each note just before capturing it. Pass the body as returned
  (Attio stores markdown and plain text; prefer the markdown if both come back). The date is
  `created_at`. The author is `created_by_actor`: when it is a workspace member, take the
  name and email from `list-workspace-members`; for an API token, app or system actor, write
  `Author: unknown (<actor type>)`. A note with a `meeting_id` names it in the header.
- Meetings: `search-meetings` by related record and time range. Use `title`, `start`, `end`
  and `participants` (name, `email_address`). Attio gives no calendar event ID: leave the
  `Calendar event:` line out and find duplicates by title, start and attendees alone. An
  all-day meeting has dates, not times; use the date as `occurred_at`.
- People: participants that Attio linked to a person record (`linked_records` with the person
  object) are captured as people with their record ID. A participant with no person record is
  linked by email only and gets no `person:` capture.
- Call recordings and transcripts (`search-call-recordings-by-metadata`,
  `get-call-recording`) and emails are not imported by this skill. Say so if the user asks.
- **Private notes.** If a note comes back marked private or visible only to its creator, follow
  the skill's rule for private notes; if the connector shows no visibility field, say so in the
  dry run.

## Limits

Rate limits are per workspace (read 100 a second, search 300 a minute). Page sizes for the MCP
tools are not documented; ask for 25 where a limit can be set.
