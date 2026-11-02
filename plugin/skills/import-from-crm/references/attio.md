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
  a filter on `stage`. A deal names its company through a record-reference attribute
  (`associated_company`) and its people through `associated_people`; capture the deal as the
  record (`deal:<id>`) and link its company by name and domain. For a sales team the deal is an
  entity of its own (below); for a venture firm it is the company's deal record.
- Named companies: `search-records` on companies.

Attio does not document the order of status options. Show them in the order returned and
confirm the mapping with the user, without assuming that order is the pipeline's.

## Sales teams (the sales pack)

A firm whose `configure` shows the sales pack first in its packs (its words say "Sales pipeline",
"Accounts", "Closed won") sells to the companies in Attio rather than investing in them. Attio is
then usually the source of truth for the pipeline, and these rules replace the skill's VC
mappings:

- **Stages map onto the sales pipeline, not onto VC statuses.** Map Attio's deal `stage` options
  onto the team's `pipeline` list stages from `configure` (the sales pack's template is Lead,
  Qualified, Discovery, Proposal, Closed won; the ways out are Closed lost, Disqualified and On
  hold). Attio's defaults: Lead to Lead, Won to Closed won, Lost to Closed lost; In Progress has
  no single match, so ask which stage it means (often Discovery) or leave it unmapped. Pass
  `"stage"` on the deal entity, never a VC status (`in_deal`, `portfolio`, `passed`).
- **Status comes from the stage.** An account's status (prospect, opportunity, customer,
  churned) follows its deals' stages: Closed won makes it a customer. Leave `status` out of
  the company entity, except for a company-level status attribute an admin added (often "Account
  status"): map Customer to `customer`, Churned or Former customer to `churned`, Prospect to
  `prospect`, and confirm the mapping in the dry run. A churned account cannot be worked out from
  its deals, so this attribute is the only way the import knows it.
- **Each deal is an opportunity entity**: `{"type": "deal", "name": "<deal name>",
  "external_refs": [the Attio ref], "stage": "<mapped stage>"}`, with the company as a separate
  organization entity. Two deals for one company (a new contract and a later expansion, or two
  renewals) are two deals; match them by Attio ID, never by name alone.
- **Contract and deal figures are the team's own.** Attio is their record, so they are imported
  as facts with `label: "retrieved"`: the deal's `value` as `amount`, its seats as `seats`, its
  close date as `close_date`, a term in months as `term_months`, a discount as `discount`; on
  the company, a contract value or ARR attribute as `contract_arr` (what the account pays the
  team, never `arr`, which is a company's own revenue), seats, `renewal_date` and
  `contract_start`. A currency field gives `currency_value` and `currency_code`: copy both. Date
  each fact with the attribute's `active_from` when the connector returns it, else the export
  date.
- **Lost reasons are categories.** A `lost_reason` select ("No budget", "Competitor") is copied
  with the record, word for word, but it is not a decision: never call `log_decision` from it.
  In the dry run, list the lost and won deals and offer `log-decision` afterwards, with the
  reasons in the account's and the team's words from the deal's notes and emails.
- **Pricing approvals and discounts** may be sensitive for the team. A note the CRM marks private
  follows the private-note rule as always; say in the dry run which deals carry a discount.

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
