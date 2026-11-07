# Ahoy: bounded conversational trial

Verified against the connected Ahoy MCP tool definitions and bounded read-only responses on
6 November 2026. A complete live Brain import has **not** been accepted yet. This reference
replaces the workflow's VC mappings, firm-wide default, meeting import and people selection.
Read the actual tool schemas before using them; stop on a mismatch, never substitute guessed APIs.

Use the user's existing Ahoy connector. Brain's automatic Ahoy connection/backfill is disabled:
the live tools have no verified current-user endpoint. Do not pass `crm_backfill`, offer an Ahoy
Connect button, infer the signed-in Ahoy user from the Brain login, or guess from a visible owner.
Never call Ahoy write/proposal/approval/merge tools.

## Setup and the dry run

1. Read Brain `configure(account={})`, select only the user's intended workspace through the
   product's workspace approval flow, and carry its `workspace_context` on subsequent calls.
   Then read `configure` for members, packs, lists and stages. Local testing uses synthetic data
   and a local Brain connection; a hosted workspace selection does not select a local server.
2. `get_crm_schema(object_type=...)` gives properties and associations. Read `ahoy_company`,
   `ahoy_contact`, `ahoy_deal`, `ahoy_note`, `ahoy_meeting_notes`, `ahoy_meeting` and `ahoy_user`
   only as needed. Input names such as `ahoy_content` differ from output display labels such as
   `Content`; map through the schema, not guesses. Duplicate labels are an error.
3. Choose named companies or one pipeline with the user. `get_crm_pipelines(object_type="ahoy_deal")`
   gives pipeline/stage names and stage IDs; it does not mean all pipelines are sales pipelines.
   Use `search_crm` to find named records. Use `query_crm_objects` for exact property or association
   filters, and `aggregate_crm_objects(aggregation_function="count", ...)` for counts.
4. Propose a small first trial: two or three companies/deals, at most 20 captures, subject to the
   user's dry-run approval. Count company/deal/contact records, notes and meeting summaries
   separately. Every source capture counts toward the limit, including an unchanged retry.
   Select linked contacts explicitly; do not invent "met" relationships from CRM associations.
   Query `ahoy_user` for the member list, using name/email fields only. These are members, not proof
   of which account is signed in. Apply the workflow's internal-member exclusions.
5. Show the exact selection, source types, counts, dates, proposed audience, missing evidence,
   stage/field mapping and skipped items before asking "Import these?". Never capture on a dry run.
   Source reads can return colleagues' org-visible records; do not describe them as the user's own.

## Pages, full text and relationships

- Query pages: `query_crm_objects(object_type=..., filters=[...], properties=[...], limit=25,
  offset=0, sort_property="ahoy_created_at", sort_order="asc")`. Advance offset by the returned
  count and stop at `total_count`. A changing total, repeated ID, empty intermediate page or
  offset over 10000 requires a narrower/restarted dry run. Filters set either `property` or
  `association`, never a null placeholder for the other. Datetime filters require ISO timestamps
  with an offset.
- `get_crm_object(entity_ids=[id], properties=[field], truncate=false,
  include_associations=false)` fetches one full text field. This untruncated mode works only for
  **one object and one field**. Notes use `ahoy_content`; meeting summaries use `ahoy_summary`.
  Keep the current body word for word. Skip text over the workflow's 20,000-character limit,
  any output flagged shortened/omitted, or any value at the connector's 45,000-character ceiling.
  A preview is not a complete note, even if the call succeeded. Do not rebuild text from history.
- `get_associations(entity_id=id, association_type=..., limit=100)` returns groups with
  `targets`, `total`, and each target's `entity_id`/`entity_type_name`. It has no paging argument.
  If returned targets do not equal the total, stop that item; do not treat partial links as complete.
  The empty result can be the text `No <association> associations found for this object.`
- Discover association names from the schema. Notes link through `ahoy_note_to_company`,
  `ahoy_note_to_contact`, `ahoy_note_to_deal` and `ahoy_note_to_meeting`. Meeting summaries use
  `ahoy_meeting_notes_to_company`, `ahoy_meeting_notes_to_contact`,
  `ahoy_meeting_notes_to_case` (deals) and `ahoy_meeting_notes_to_meeting`.

## Dates and authors

Ordinary record tools return display dates such as `2026-10-02 10:00 IST`, rounded to minutes.
Do not guess the timezone abbreviation, add missing seconds or use the time of import.

- Call `get_timeline_events(entity_id=id, event_group="ahoy_property_value", limit=50)`.
  Follow `pagination.next_cursor` while `has_more` is true. Check the entity ID on each event.
  The `ahoy_object_created` event's exact ISO `occurred_at` is the note creation date. Property
  updates give their own exact times. Missing creation, repeated cursor/sequence, hidden or
  shortened values, deletion/merge or unsupported event types mean stop and report the item.
- A meeting summary's `ahoy_created_at` is when it was **synced**. Use the linked meeting's current
  `ahoy_start_time` for `occurred_at`, not that sync time. Obtain the exact value by reading its
  complete property history: creation and `ahoy_property_updated` events carry `payload.properties`;
  apply them in `seq` order. A cleared or missing start time, all-day-only event, hidden history or
  multiple linked meetings is unresolved: skip the summary instead of inventing a datetime.
- A note's human author comes from `ahoy_note_to_creator`, or `ahoy_entity_to_creator` when the
  former is empty. Verify a single target is `ahoy_user`, then retrieve its name/email. Owner,
  last editor, automation actor and the importing user are not substitutes. If the author cannot
  be resolved, use `Author: unknown` and omit `author` and the author entity. AI/provider meeting
  summaries have no invented human author.

## Audience

Default the trial to private. Offer firm sharing only in the dry run and only when the item has
an explicit `<object>_visible_to_org` association to an `ahoy_org`. For notes this is
`ahoy_note_visible_to_org`; summaries use `ahoy_meeting_notes_visible_to_org`. Readability alone
is not permission to widen sharing. A parent company's visibility does not establish a note's.

A private note by someone else is skipped. Because the connector lacks a verified current-user
read, do not assume a private author is the connected user: ask the user to identify their Ahoy
account when needed and match its exact user ID/email before including their private notes.
Unclear access/ownership is a skipped item in the manifest. Private captures omit `author`.

## Sales, fundraising and source identity

- Keep sales deals as `deal` entities linked to separate company entities. Two opportunities for
  one company remain two opportunities. Map sales stages to the target's sales pipeline only
  after reviewing its configuration; never translate a sales win into a VC investment.
  A fundraising pipeline describes investment **into the user's business**, not investments it
  made. Preserve the original pipeline/stage as source text and leave structured stage/status
  unset when no matching destination exists. Never create/change pipelines as part of import.
- Preserve fields in a deterministic source template and order. Map a deal value only to an
  agreed deal `amount`, never company `arr`. Copy amounts/currencies exactly. Ambiguous custom
  fields remain source text; do not create firm settings. Do not date a stage move from record
  creation: use exact stage-entry evidence or leave the structured stage unset.
- `system: "ahoy"`; source IDs `company:<entity_id>`, `contact:<entity_id>`, `deal:<entity_id>`,
  `note:<entity_id>`. A summary uses `note:summary-<meeting_notes entity_id>` and, when its one
  linked meeting is verified, `refs: [{system: "ahoy", external_id: "meeting:<meeting_id>"}]`.
  Entity refs use bare Ahoy IDs plus verified domains/emails. Never guess URLs: omit them when
  the connector gives no record page. Do not use the video-call URL as a CRM source page.
- Capture notes/summaries with `kind: "note"`, the standard author/date header, and the exact
  body. Do not prepend the summary title into its body.
- One capture per Ahoy note or summary across the whole manifest, not one per record. The same
  note or summary often appears under both a selected company and its deal; capturing it per
  record would make the second capture a revision of the first that points only at the second
  record. Deduplicate by source ID before the dry run and count it once. Give it every verified
  company, deal and contact association (complete groups only, as above), in this order, then
  by Ahoy ID, including records outside the selection: the header line reads
  `Ahoy note <id>, on <name>, <name>[, meeting <meeting id>]` and `entities` holds each of
  them, with the author entity as usual. The text then stays the same whichever record or
  selection reaches it, so a rerun is unchanged. The dry run lists the item once, with all its
  records. Do not import email or calendar events;
  those come from Brain's own connectors. Reading meeting metadata solely to date a summary
  does not import a meeting or establish attendees.
- Files have `ahoy_created_at` (uploaded time), name/type/size metadata, but the available tools
  expose no verified original-file download. Report documents as unsupported for this trial;
  never upload metadata as though it were the file. A separately authorized original-file
  transfer would use `request_upload` with `system: "ahoy"`, `external_id: "file:<entity_id>"`
  and an exact source timestamp as `occurred_at` when available. It is not proven by this trial.

## Verify the trial

After approved captures, read their Brain sources back: exact body, source IDs, original dates,
author and intended audience. Check a representative company/deal page, and that a note shared
by a company and a deal is one source linked to both. Rerun the same approved
selection and confirm unchanged records are not duplicated. Report new/updated/unchanged/skipped/
failed counts and the stopping point. Keep fixture tests, local import and hosted import evidence
separate; passing synthetic tests does not establish a live Ahoy import.
