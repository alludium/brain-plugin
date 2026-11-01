# Affinity

For Affinity's hosted connector (tools such as `get_current_user`, `get_lists`,
`get_notes_for_entity`). A different Affinity MCP server whose tools all start with
`affinity_` is not covered: say so and stop. Tested: the dry run, against a real Affinity on
30 October 2026. The import itself has not run yet.

`system: "affinity"`. Source ID prefixes: `company:`, `person:`, `opportunity:`, `note:`,
`meeting:`. An opportunity is the deal record (`deal` entity type, `opportunity:<id>`).

## Links and IDs

Call `get_current_user` once in setup; its tenant `subdomain` gives the base
`https://<subdomain>.affinity.co`. Pages are `/companies/<id>` (in Affinity's API
documentation), `/persons/<id>` and `/opportunities/<id>` (the same pattern, not yet confirmed:
open one from the brain after the first live import and correct this file if it is wrong).
Notes and meetings have no page of their own; use the page of the company or opportunity they
were fetched for.

Affinity entity types are 0 person, 1 company, 8 opportunity. Take the type from the tool that
produced the ID, never guess it, and never use a list entry ID as an entity ID. A person is
internal (a firm member) when Affinity marks them so; apply the skill's email-domain rule too.

## Choosing the records

- A list: `get_lists`, filtered by name.
- A saved view on it: `get_saved_views`, then `get_saved_view_list_entries`.
- A filter on the list's own fields: `get_list_fields`, `get_list_field_dropdown_options` for
  the status options and their order, then `search_list_entries` with `search_criteria`.
  Take each filter's `valueType` and operator from `get_list_fields` with the filterability
  include rather than guessing: a status field is often `ranked-dropdown`, not `dropdown`.
- Named companies: `search_companies_top_matches`.

Request only the fields you need (`field_ids`): status, owners, and any field you will map to
a fact. Page with `limit` 25. The status field's dropdown options give the stage names for the
status mapping.

## Counting (dry run)

- Notes: `get_notes_for_entity` with `limit: 1` and `total_count: true`; use only
  `pagination.totalCount` and do not show the note it returns.
- Meetings: `get_meetings_for_entity` over the window (at most 365 days per call) with
  `page_size: 10`, counting meetings and collecting the distinct external people's Affinity
  IDs.

## Fetching (import)

- Notes: `get_notes_for_entity` with the record's entity type, `limit` 5, newest first, and
  `filter_expr` on `createdAt` if the user set a notes window. The body is `content.html`
  (HTML; pass it as it is), the date `createdAt`, the author the note's creator. A note
  attached to an Affinity meeting names it: add `, meeting <interaction id>` to the header.
- Meetings: `get_meetings_for_entity`, `page_size: 10`. Use `title`, `start_time`,
  `end_time`, `ical_uid` (the calendar event ID: pass it in `refs` as `ical`, with
  `start_time` as `occurred_at`) and `persons` (each with `primary_email` and an Affinity
  person ID). Affinity meetings are calendar events: no notes. A note attached to a meeting
  gets `refs: [{"system": "affinity", "external_id": "meeting:<interaction id>"}]`.
- People: from the meetings' `persons`. Their email lists hold every address Affinity has seen
  for them (about 72% of a meeting payload); keep only `primary_email` and addresses on the
  record's domains.

If Affinity says the user's seat lacks a permission (for example list export), say so and stop.
- **Private notes.** A note has `is_private` (or its notes tool shows it as private to its
  creator); follow the skill's rule for private notes. Check the field name in the first note
  returned, and if the connector shows no such field, say so in the dry run.

## What to expect in a firm's Affinity

- **People with two records** under different emails, and colleagues marked external. Capture
  each record as it is and list them as possible duplicates or possible firm members.
- **Two firm email domains.** A firm that changed domain has members on both; `configure` may
  hold only the current one. Ask before treating the old domain's people as external.
- **A renamed company** under its old and new names with two domains. List it as a possible
  duplicate; do not merge.
- **Notes that copy a notes tool's write-up.** Some notes are generated post-call write-ups
  that name the Granola note they came from. Import them: Alludium Brain links each to the Granola
  note it wraps, so they will be linked, not counted twice. Say so in the dry run.
- **Duplicate and recurring calendar events.** Affinity can hold one event twice under two IDs
  (same title, start and attendees), and a recurring meeting shares one `ical_uid` across its
  occurrences. Capture each as it is with its `ical_uid` in `refs` and its start: Alludium Brain
  matches a meeting by the UID together with the start, else by start and attendees. Some
  meetings have no title.
- **Statuses that lag.** Several companies with regular board meetings were still at an open
  deal stage on the deal list. Mark them "check" and ask.
- **Size.** About 17 captures per company with a 90-day window, and meeting results are large
  (each attendee carries every email Affinity knows), which is why the window defaults to 90
  days and meetings come 10 at a time. Opportunity lists may hold fundraising rather than
  deals; ask which list holds the deal pipeline.
