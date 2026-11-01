# HubSpot (untested)

For HubSpot's remote MCP server, the connector in Claude's directory (tools such as
`get_user_details`, `search_crm_objects`, `get_crm_objects`, `search_owners`). Not HubSpot's
local developer MCP server, which is for building apps. Written from HubSpot's developer and
knowledge-base documentation (October 2026, the server is in public beta); never run against a
real account. HubSpot documents tool names but not all of their parameters, so check each
call's result against this file. If a tool named here is missing or a field cannot be found,
stop and say which, rather than guess.

The connector can create and update records. Never call a write tool or a write operation.

`system: "hubspot"`. Source ID prefixes: `company:`, `person:` (a HubSpot contact), `deal:`,
`note:`, `meeting:`. HubSpot IDs are numbers, kept as strings, and unique only within an
object type, so the prefix matters.

## Setup, links and firm members

- Call `get_user_details` first: HubSpot says the tools available vary by account, and it
  reports which objects the user can read. If notes or meetings are not readable, say why in
  the dry run: activities need a Super Admin to allow them for the connector, and an account
  with Sensitive Data turned on blocks them entirely. Records can still be counted.
- Pages are `https://app.hubspot.com/contacts/<Hub ID>/record/<object type>/<id>`, with object
  types `0-1` contact, `0-2` company, `0-3` deal (the pattern is documented by example; the
  company and deal values follow it). Take the Hub ID (portal ID) from `get_user_details` or
  `get_organization_details`; if neither returns it, leave `url` out. Notes and meetings use
  the page of the record they were fetched for.
- Firm members: HubSpot users, from `search_owners` (names and emails), with the skill's
  email-domain rule.
- Before reading associations (a deal's company, a record's notes, meetings and contacts),
  call `tool_guidance` once and follow what it says; HubSpot asks for this and documents no
  separate association tool. If associations cannot be read, stop and say so.

## Choosing the records

- A deal pipeline: the deal properties `pipeline` and `dealstage` hold internal IDs. Get the
  pipelines and stage labels, with their `displayOrder`, from `get_properties` or
  `search_properties` on deals (inferred: each option should carry a label and a display
  order); map by label, in that order. Stages marked closed won or closed lost usually map to `portfolio` and `passed`.
  Then `search_crm_objects` on deals with filters on `pipeline` and `dealstage`, 25 a page.
  Each deal is a record: capture the deal (`deal:<id>`, `deal` entity) and its associated
  company (`company:<id>`, `organization` entity with the mapped status), two captures per
  record, and link them. A deal with no company is captured on its own.
- Named companies: `search_crm_objects` on companies with a text query.
- HubSpot lists (segments) are not documented in the connector; offer a pipeline, a property
  filter or named companies instead.

Request only the properties you need: `name`, `domain`, `dealname`, `pipeline`, `dealstage`,
`hubspot_owner_id`, and any property you will map to a fact.

## Counting (dry run)

Use `search_crm_objects` on notes and on meetings, filtered to the record's associations as
`tool_guidance` describes, with the smallest page, reading only the total. If no total comes
back, count IDs only and stop at 50 ("50+").

## Fetching (import)

- Notes (object `0-46`): `hs_note_body` as returned (its format is not documented; pass it
  unchanged), `hs_timestamp` as `occurred_at` and the `Date:` line, and `hubspot_owner_id` as
  the author, resolved to a name and email with `search_owners`. No owner: `Author: unknown`.
- Meetings (object `0-47`): `hs_meeting_title`, `hs_meeting_start_time`,
  `hs_meeting_end_time`. Attendees are not a property: they are the meeting's associated
  contacts (external people) and owners (firm members). There is no calendar event ID: leave
  the `Calendar event:` line out and find duplicates by title, start and attendees.
  `hs_meeting_external_url` is a link to the calendar event; add it as `Calendar link:` when
  present. Unlike Affinity, a HubSpot meeting can carry notes: after the header lines and a
  blank line, add `hs_meeting_body` and then `Internal notes:` with `hs_internal_meeting_notes`,
  each exactly as returned, under the same 20,000-character cap.
- People: the meetings' associated contacts, with `firstname`, `lastname`, `email` and their
  contact ID.
- Calls (object `0-48`), emails and tasks are not imported by this skill.
- **Private notes.** A note an owner restricted to themselves (or to a team) is private; follow
  the skill's rule for private notes. If the connector shows no visibility field, say so in the
  dry run.

## Limits

`search_crm_objects` returns up to 200 a page (ask for 25) and at most 10,000 results per
query; `get_crm_objects` takes up to 100 IDs. HubSpot's search API allows about 5 requests a
second per account. One HubSpot account per Claude account.
