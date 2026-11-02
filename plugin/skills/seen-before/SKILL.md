---
name: seen-before
description: Check a list of sourced companies against the firm's Alludium Brain and say for each whether it is new, seen, met or passed, with the reason and who at the firm knows them. Use when the user shares a sourcing or prospect list, CSV, spreadsheet, newsletter or pasted list of startups or accounts and asks "have we seen these?", "which of these are new?", "check this list against the brain" or "dedupe this list".
---

# Seen before?

Look the whole list up in Alludium Brain with one batch `search`, then give each company one verdict:

| Verdict | Means |
|---|---|
| `passed` | The firm decided not to go ahead, for a venture firm not to invest (entity status `passed`, or a pass decision). |
| `met` | Someone at the firm has had a meeting with them. |
| `seen` | The firm has something on them (a deck, an email, a note, a CRM record) but no meeting. |
| `new` | Nothing in the brain matches. |

## Rules

- **Read the list, not more.** Take only the company name and website (domain) from each row,
  and a one-line description or sector column if the list has one. For a file, print just those
  columns with a short script rather than opening the whole file.
- **A lookalike is not a match.** `Acme Analytics` is not `Acme AI Ltd`. A website that
  differs from the entity's domains means a different company.
- **Cite every reason** with its source ID. Do not guess a reason the brain does not hold.
- Do not paste briefs or sources back. One line per company.
- **No backfill for the list.** A match with `coverage` "crm_only" (CRM record only) is `seen`, with "CRM
  record only" in the reason. Offer a backfill only when the user then asks about one of those
  companies in detail (below), never for the list.

## Steps

1. Call `search` with `query: ""` and `queries`: one `{"name": …, "domain": …, "description": …}`
   per row, in the list's order (up to 200 rows a call). `description` is the list's own one-line
   description or sector column for the row, word for word; leave it out when the list has none. Each row comes back with its best match (status,
   domains, the latest meeting or email, how it matched, `coverage`) and any other candidates.
   A match `also_named` other entities that share the name (a fund named like the company):
   the match is the one the firm is closest to; name the others only if the user asks.
2. **Is it the same company?**
   - `matched_by` is the domain: same company.
   - Matched by name, and the list's website differs from the match's domains: a different
     company. The verdict is `new`; name the lookalike in the reason.
   - Matched by name, with no website on one side: same company only if the names are the
     same once suffixes (Ltd, GmbH, B.V., Inc, Labs, AI) are removed. Otherwise `new`, "possible
     match: <entity>, not confirmed".
   - No match: `new`.
3. **Details for each match**: call `entity_brief` with the match's ID. For lists of more than
   25 matches, do this only for the rows the user asks about, and give the others a verdict
   from step 1 alone (`passed` from the status; otherwise `met` if the match says `met` (a
   meeting with attendees, with its `last_meeting`), else `seen`).
4. **Verdict** from the brief: `passed` if the status is `passed` or it lists a pass decision;
   otherwise `met` if the brief says `met: true` (an interaction that is a meeting); otherwise
   `seen`. An email exchange or a forwarded deck is `seen`, not `met`, even when a colleague
   was on the email.
5. **Reason**, one short clause with a citation:
   - passed: when and why, from the decision. If the brief has no decision reasons, one
     `search` for "<name> pass" finds the memo.
   - met: the status (`in_deal`, `portfolio`, `prospect`, `tracking`) and the latest meeting.
   - seen: what the firm has (for example, an inbound deck) and when. A meeting that has not
     happened yet (`upcoming_meeting`, or an interaction with `upcoming: true`) is not `met`:
     keep `seen` and add "meeting booked for <date>".
6. **Who knows them**: the members in `met_by` (they were in its meetings), then those in
   `in_touch_by` (on its emails only: say "in touch by email"), then the authors of its notes.
   If `met_by` is empty but there are meetings, add "attendees not recorded".
7. **Lists**: to check against one of the firm's lists instead of a pasted one ("which of the
   climate sourcing list have we met?"), read it with `search` and `list`, then go on from
   step 3 with its entries. When the user asks to save the new ones to a list, capture one
   short note naming them, with `lists` on each (`note` skill), and a private note for a private
   list.
8. **Tags**: a match's `tags` (sector, theme, geography from the firm's vocabularies) go in a
   Tags column, shortest form (`sector: Climate > Carbon removal`). Leave the column out when no
   match has any. For a `new` company the only tags are the row's `list_tags`, which the brain
   matched from the list's own description: show them with "(from the list)". Never add tags of
   your own.
9. **Comparable past cases**: a row with `past_cases` falls in the cohort of one of the firm's
   learning-run insights. Add each `line` to its reason, with the insight's ID
   ("comparable past passes: 6 of 8 cited retention [ins_…]"), and "not yet reviewed" for a
   `candidate`. Say once, under the table, that these describe past decisions and are not a reason
   to pass. If the result has a `past_cases_note`, say it in one line.

## Output

A table, in the list's order, then one line of totals:

| Company | Verdict | Reason | Who knows | Tags | Sources |
|---|---|---|---|---|---|
| ACME AI | met | Live deal (`in_deal`); partner meeting on 21 Oct | Jonah, Priya, Clara | sector: AI infrastructure | [Partner meeting, 21 Oct 2026](…), [Intro email, 2 Oct 2026](…) |

End with: "N new, N seen, N met, N passed." Offer to note the new ones only if the user asks.

**New companies and the thesis.** When the list has a description or sector column, call
`configure` once with no arguments and, for `new` rows only, add "outside thesis?" to the reason
when the list's own words plainly match the thesis's `out_of_scope` or name a stage or region it
excludes, as "(from the list)". Nothing else: the brain holds no evidence on a new company, so
there is no thesis check for it. For a company already in the brain, the user can ask for its
fit with `brief`.

## Backfill: one company the brain knows only from its CRM

Only when the user drills into one company from the list ("tell me more about Acme").

When `entity_brief` (or a lookup) gives `coverage` "crm_only", the brain has the
company's CRM record and nothing else: no notes, meetings, email or documents. Before answering,
offer in one line: "The brain has only <name>'s <CRM> record. Shall I pull its CRM notes and
meetings (filed for the firm) and look in your own email and Drive for it (filed private to
you)?" Do nothing more on it until the user says yes; if they say no, answer from the record.

On a yes, for this one company only:

1. **CRM notes and meetings**, firm-scoped: follow the `import-from-crm` skill's "One company"
   section with the record in `crm_record` (its system, ID and page). It shows the
   counts and asks once more before importing.
2. **The user's own email and Drive**, if those connectors are connected: search them for the
   company's name and domain (the newest 20 results each). File only items about this company,
   word for word, each with `capture` and `scope: "private"`: an email as `kind: "email"` with
   its `From:`, `To:`, `Date:` and `Subject:` lines and body, `system` (`gmail` or `outlook`),
   the message ID as `external_id` and the Message-ID as an `rfc822` ref; a Drive document as
   `kind: "document"` with its text, `system: "gdrive"`, the file ID and its link. Link the
   company by its `id`. Skip anything personal or unrelated; when in doubt, skip.
3. **Offer to share** the private items in one line ("Filed 4 emails and 1 document, private
   to you. Share them with the firm?"); on a yes, `share` each with `scope: "firm"`.
4. **Answer from the brain**: call `entity_brief` again and answer from it, as usual.
