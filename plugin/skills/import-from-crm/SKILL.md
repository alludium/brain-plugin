---
name: import-from-crm
description: Fill the firm's VC Brain from its CRM (Affinity, Attio or HubSpot) - the companies, people and deals on a chosen list, saved view, pipeline or set of named companies, with their notes and recent meetings - through the CRM's hosted connector. Always dry-runs first, works in batches with progress, is safe to re-run (changed records are updated) and stops at a size limit. Also backfills one company the brain knows only from its CRM record, when brief, prepare-meeting or seen-before offer it. Use when the user says "import our Affinity pipeline", "import from Affinity", "load our deal list from the CRM into the brain", "backfill the brain from HubSpot", "import our Attio deals" or "dry-run a CRM import". Not for checking a sourcing list against the brain (use seen-before) or filing one meeting (use capture-meeting).
---

# Import from a CRM

You copy CRM records from the user's CRM connector into VC Brain with the connector's `capture`
tool. Each CRM record becomes one source with its CRM ID, so a re-run finds it already stored:
an unchanged record comes back "Already captured", and a record or note whose text changed in
the CRM comes back "Updated" and is stored as a new version, whose stage, status, fields and
facts replace the old ones. VC Brain links and resolves entities; your job is a faithful,
bounded copy.

This file is the workflow. How to call a particular CRM's connector (tool names, IDs, links,
fields, known traps) is in a reference file you read once you know which CRM it is.

## Which CRM

Look at the tools you have and match them to a reference:

| CRM | Its connector's tools include | Read | `system` |
|---|---|---|---|
| Affinity | `get_current_user`, `get_lists`, `get_saved_views`, `get_notes_for_entity`, `get_meetings_for_entity` | `references/affinity.md` | `affinity` |
| Attio (untested) | `whoami`, `list-lists`, `list-records-in-list`, `search-notes-by-metadata`, `search-meetings` | `references/attio.md` | `attio` |
| HubSpot (untested) | `get_user_details`, `search_crm_objects`, `get_crm_objects`, `search_owners` | `references/hubspot.md` | `hubspot` |

Tool names carry a connector prefix that varies by host (`mcp__<connector>__get_lists`); match
on the name after it. Read only the reference for the CRM in use, before any CRM call. If the
user named a CRM, use that one. If more than one CRM is connected and the user named none, ask
which. If none is connected, say which connectors this skill supports and stop. For any other
CRM, say it is not supported yet and stop; do not improvise an import.

For Attio and HubSpot, say once at the start that this skill has not been tested against that
CRM yet, and treat any tool name or field that does not match the reference as a reason to
stop and report it rather than guess.

## Rules

- **Dry run first.** Unless the user has just approved a dry run's plan in this conversation,
  run the dry run (below) and stop. A dry run reads the CRM only and never calls `capture`.
  Never call a CRM tool that writes (create, update, delete, merge, add note).
- **A size limit.** Ask for the most captures this run may make if the user gave none, and
  stop before starting the next record once it is reached. Count every `capture` call,
  including ones that return "Already captured".
- **Word for word.** Pass the CRM's text exactly as the connector returned it, HTML or
  markdown included. No summarising, shortening, reformatting or fixing. Never compute or
  round a figure.
- **Nothing in bulk through the conversation.** Fetch small pages (notes 5 at a time,
  meetings 10 at a time), capture each item as soon as you have it, and keep only IDs and
  counts. Never repeat, quote or describe note or record text in your messages, including a
  note a counting call returned in full; progress lines carry counts only.
  Skip a note longer than 20,000 characters and list it as too long, rather than risk a
  truncated copy. Ask the connector only for the fields you need.
- **The same text for the same record.** Write a record's text from the template below with
  the same fields, in the same order, on every run, so a record that did not change in the CRM
  is recognised as unchanged. A changed value is what makes a new version.
- **An ID collision is an error, not a skip.** If `capture` refuses a record because its ID is
  already stored under another company's title, do not change the ID or retry. Count it as
  failed, carry on, and list it at the end with both names so the user can check the CRM. If
  the company was renamed in the CRM, capture it again with the old name in the entity's
  `aliases`.
- **Source IDs on every capture.** `system`: the CRM's value from the table above.
  `external_id` as `<object>:<id>` (`company:`, `person:`, `deal:`, `note:`, `meeting:`, or the
  object names the reference gives), because a CRM's ID spaces can overlap and VC Brain keys a
  source by system and ID alone. `url`: the record's page, built as the reference says. Never
  invent an ID or a link; leave `url` out if the reference gives no way to build it.
- **Entity refs use the bare ID**: `{"system": "<system>", "external_id": "<id>", "url":
  "<page>"}`, plus `{"system": "domain", "external_id": "<domain>"}` for a company's domains
  and `{"system": "email", "external_id": "<email>"}` for a person's emails.
- **Firm scope**, with one exception. Pass `scope: "firm"` on every capture: CRM records belong
  to the firm. A note the CRM marks private (Affinity, Attio and HubSpot all let a user keep a
  note to themselves; the reference says which field) stays private: if the user running the
  import wrote it, capture it with `scope: "private"`; if someone else did, skip it and count it
  as skipped (private). Never file a private CRM note firm-wide.
- **Firm members are not imported as people.** They come from `onboard`. Link them by email
  as authors and attendees only. A person is a firm member if the CRM marks them as a user or
  internal, or one of their emails is on the user's own email domain or on a domain of a
  member's email in `configure`. CRMs mark colleagues as external and firms change domains, so
  also flag, in the dry run, any external person whose name matches a member's: ask whether it
  is the member under an old address.
- **No merging.** Two CRM records that look like one person or one company (the same name
  under different emails, a renamed company with two domains) are captured as they are, each
  with its own refs. List them in the dry run as possible duplicates; VC Brain resolves them,
  and a wrong merge is worse than a split.
- **Notes carry their author and date**: the author's name and email in an `Author:` line and
  as a person entity (not an attendee), and `occurred_at` set to when the note was written.
  VC Brain records you as the capturer; the `Author:` line says who wrote it.
- **Meetings carry their attendees and time**: every attendee as a person entity with
  `attendee: true` and an email ref, and `occurred_at` set to the start time.

## Steps

1. **Setup.** Call `configure` with no arguments. If it lists no members, stop and suggest
   running `onboard` first: without members, VC Brain cannot say who at the firm met whom.
   If VC Brain is not connected, a dry run can still go ahead (it reads only the CRM); an
   import cannot. Then do the reference's setup (the current user and the base for links).
2. **Choose the records.** From the user's words: a list, a saved view on it, a pipeline, a
   filter on stage or another field, or named companies. The reference says which tools do
   each. Page with 25 at a time and stop paging once you have the requested number of
   records. If the choice is ambiguous, show the candidates (name and entry count only) and
   ask.
3. **Agree the mappings once, in the dry run.**
   - **Stage.** Map the list's or pipeline's stages, in their order, onto the firm's own deal
     process (`configure` with no arguments lists its stages, and the ways out Passed, Lost and
     On hold): for example "Intro call" to First call, "Diligence" to Due diligence, "Declined"
     to Passed, "Lost to competitor" to Lost, "Nurture" to On hold, "Won" or "Invested" to
     Portfolio. Show the mapping as one table (CRM stage → firm stage) in the dry run. Two CRM
     stages may map to one firm stage; a CRM stage with no clear match stays unmapped and its
     records are imported without a stage. Never add a stage to the firm's process from an
     import: suggest `onboard` if the CRM has a stage the firm's process lacks.
   - **Status.** The firm stage sets the status (screening: `prospect`; evaluation through
     closing: `in_deal`; portfolio: `portfolio`; Passed and Lost: `passed`; On hold:
     `tracking`), so a record with a mapped stage needs no status. For a CRM stage with no
     firm stage, map it to VC Brain's organization statuses (`tracking`, `prospect`,
     `in_deal`, `passed`, `portfolio`, `exited`) instead, or leave it unmapped when unsure.
   - **The brain's stage wins.** A company the brain already has at a stage keeps it: VC
     Brain ignores the stage on an undated CRM record for it, because decisions logged in the
     brain are newer than the CRM. In the dry run, compare each record's mapped stage with the
     brain's (the lookup's `stage`, below) and mark "check" wherever they differ, saying both
     ("CRM: First call; brain: Due diligence since 2026-10-20"). A move the user confirms is
     recorded with `log-decision`, not by the import.
   - **Activity.** CRM stages lag reality, so check each record against its own activity: a record
     at an open deal stage with regular board meetings, a "passed" record with recent
     meetings, or a note that says the firm invested. Mark such a record "check" in the dry
     run, say what disagrees in a few words, and ask which stage to use. A record left
     "check" is imported without a stage or status.
   - **Facts.** Only fields whose meaning matches a key in `capture`'s `facts` description
     (for example an ARR field to `arr`), or one of the firm's custom fields. Ambiguous
     fields, such as a valuation that may be pre or post money, stay unmapped. Fact values are
     copied as the CRM returned them, with `label: "retrieved"`.
4. **Dry run.** For each chosen record, without capturing anything, count its notes, its
   meetings in the meeting window (default the last 90 days) and the distinct external people
   in those meetings, using the reference's counting calls.
   Then one VC Brain `search` with `queries` (name and domain per company, if VC Brain is
   connected) counts how many are already in the brain and gives each match's `stage`, to
   compare with the mapped stage.

   Show one table with a row per record: name, CRM stage, firm stage (or status, or "check"), notes,
   meetings in the window, external people. Under it: the totals as captures (records +
   people + notes + meetings), the limit, what would be left over, the mappings (stage and facts), the
   window, and three short lists: records marked "check" with the reason, possible duplicate
   people or companies, and possible firm members under another address. Say if notes look
   like call write-ups from a notes tool (they name it): VC Brain links them to the notes
   tool's copy of that meeting, so they are not counted twice. Ask "Import these?" and wait for a
   clear yes, with answers to any "check".
5. **Import**, one record at a time, in the dry run's order. The text formats below are the
   default; where the reference adds or drops a line, follow the reference.
   1. **The record.** `capture` with `kind: "external_record"`, `title`: the name exactly as
      in the CRM, `external_id: "company:<id>"` (or the deal object's prefix), `url`: its
      page, `scope: "firm"`, and `text` as these lines, leaving out empty ones:

      ```text
      <CRM> company: <name>
      Domains: <domain>, <domain>
      List: <list or pipeline name>
      <Field name>: <value as returned>      (one line per non-empty field fetched)
      ```

      `entities`: the company as `{"type": "organization", "name": "<name>", "status":
      "<mapped status>", "external_refs": [the CRM ref, a domain ref for each domain]}` (leave
      `status` out if unmapped or "check" unanswered); `facts`: the mapped fields. Keep the
      `id` VC Brain returns for the company. For a mapped stage, use `"stage": "<firm stage
      name>"` instead of `status`; the record's date (`occurred_at`, when the CRM gives the date
      it entered the stage, else leave it out) dates the move. A deal record is the same with `deal` as the
      entity type and the companies it names linked by name or `id`.
   2. **Its notes**, newest first, pages of 5. One `capture` per note: `kind: "note"`,
      `scope: "firm"`, `occurred_at`: when the note was written, `external_id: "note:<id>"`,
      `url`: the record's page, and `text`:

      ```text
      Author: <First Last> (<email>)
      Date: <created time>
      <CRM> note <id>, on <record name>[, meeting <meeting id>]

      <note body exactly as returned>
      ```

      `entities`: the record by its VC Brain `id`, and the author as a person with their
      email ref. If the CRM gives no author, write `Author: unknown` and leave the person out.
      A note attached to a CRM meeting also gets `refs: [{"system": "<crm system>",
      "external_id": "meeting:<meeting id>"}]`, so VC Brain files it as notes of that meeting.
   3. **Its meetings** in the window, pages of 10. One `capture` per meeting, including one
      that seems to arrive twice: VC Brain matches records of one meeting by the calendar
      event ID together with the start (a recurring meeting reuses the ID for every
      occurrence), else by the start and attendees, and links them rather than counting
      twice. `kind: "meeting"`, `title`: the title if it has one, `occurred_at`: the start
      time, `external_id: "meeting:<id>"`, `refs: [{"system": "ical", "external_id": "<calendar
      event ID>"}]` when it has one, `url`: the record's page, `scope: "firm"`, and `text`:

      ```text
      Title: <title>
      Date: <start> to <end>
      Attendees: <First Last> (<email>), …
      Calendar event: <calendar event ID>
      <CRM> meeting <id>, on <record name>
      ```

      `entities`: every attendee with `attendee: true`, an email ref and, for external
      people, the CRM ref; and the record by its `id`.
   4. **Its people**: each distinct external person met in those meetings, once per run. One
      `capture` with `kind: "external_record"`, `title`: their full name, `external_id:
      "person:<id>"`, `url`: their page, `scope: "firm"`, and `text`:

      ```text
      <CRM> person: <First Last>
      Emails: <primary email>[, other emails on the record's domains]
      Met in <CRM> meetings on: <record name>
      ```

      `entities`: the person with the CRM ref and an email ref for each email listed, and the
      record by its `id`. Leave out emails on other domains: CRMs' merged email lists can hold
      old employers and personal addresses.
   5. **Progress.** After each record, one line: `3/10 <name>: record, 4 notes, 6 meetings,
      3 people (2 already there, 1 updated, 1 duplicate)`. After every 5 records, add the captures used
      so far against the limit. Stop when the limit is reached.
6. **Finish** with one short table: records, people, notes, meetings; each with captured,
   updated (a new version of a changed record), already there, skipped (too long, duplicate,
   no ID, private to someone else) and failed (with any ID collisions named). Then the captures used against the limit,
   where it stopped, and that running it again picks up from there: unchanged records come back
   as "Already captured", and records changed in the CRM since are updated.

## One company (a backfill)

When `brief`, `prepare-meeting` or `seen-before` found a company with `coverage` "crm_only"
(CRM record only) and the user said yes to filling it in, import that one company. Never do this for a
list, and never unless the user said yes.

- **The record is already chosen**: the entity's `crm_record` gives the CRM `system`,
  the record's ID (`company:<id>`: the CRM ID is the part after the colon) and its page.
- **Firm scope**, as for any import: these are the firm's CRM notes and meetings (a note the
  CRM marks private stays private, as above).
- **Dry run, in one line.** Count its notes, its meetings and their external people, as in
  step 4, over its whole history. Say "<name>: N notes, N meetings, N people: import them?" and
  wait for a yes. If that is more than 60 captures, offer the newest 60 (notes and meetings in
  the last 12 months first) and say what would be left.
- **Import** as in step 5: the record again (unchanged comes back "Already captured"), then
  its notes, meetings and people. Finish with one progress line, not the table.
- Then hand back to the skill that asked, which answers from the brain.

If a `capture` fails, count it, carry on with the next item and name the failures at the end.
If the CRM connector says the user's seat lacks a permission or a scope, say which and stop.
