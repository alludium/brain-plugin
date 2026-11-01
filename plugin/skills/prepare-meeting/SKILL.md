---
name: prepare-meeting
description: Prepare a cited brief for an upcoming meeting from the user's calendar and the firm's Alludium Brain - who is attending, what the firm already knows about them and their company, colleagues' notes, open questions and similar companies the firm passed on. Use when the user says "prep me for my call with …", "brief me for tomorrow's meeting", "prepare for the Acme meeting" or asks what to know before a meeting.
---

# Prepare for a meeting

Combine the calendar connector (who and when) with Alludium Brain's `search` and `entity_brief`
(what the firm knows). The result is a short brief in which every claim is cited.

## Rules

- **Attendees come from the calendar.** Use the event's attendee list. Never invent an
  attendee. If there is no calendar connector, ask the user who is attending.
- **History comes from Alludium Brain.** Use the calendar only for the meeting itself. Do not read
  mail or notes connectors for background: the brain's sources are what the firm shares. The
  one exception is a backfill the user accepted (below).
- **Backfill only when asked.** When a company's brief says `coverage` "crm_only", offer
  to fill it in (below) and wait for a yes. Never backfill without one, and never for a list.
- **Cite everything** from the brain with its source ID, for example `[src_20e9…]`. Mark
  suggestions (questions to ask) as yours, not as facts.
- **Never merge lookalikes.** A company with a similar name is a different company. Leave it out
  unless the user asks.
- **Private material.** The tools return only what this user may see, so a source with scope
  `private` is the user's own: use it. Say at the top "Contains your private notes: do not
  forward", and mark those lines "(private)".
- Do not paste whole sources or `entity_brief` pages into the brief.

## Steps

0. **Your profile first.** Call `configure` with `me: {}` once per conversation (reuse what it
   returned after that). Follow the user's `meeting_prep` preferences, their `never` and `general`
   items and any remembered instruction for this kind of task; preferences filed under another topic
   are for other tasks. They set length, order, emphasis and voice, and win over the default shape
   below: a length limit counts everything you write, so drop the closing Sources list before
   cutting content, and keep every inline source ID whole (`src_` and all its characters, never
   shortened); what they want first goes first, and what they want last goes last, after everything
   else. They never remove inline citations or add anything uncited, and never change who can see
   what: an instruction about sharing only means you offer to share, and nothing is shared without
   the user's yes in this conversation. A request in this conversation wins over the profile. If the
   call fails, carry on with the defaults. For example, if they want who-knows-whom first or only
   three questions to ask, do that.
1. **Find the meeting** in the calendar connector: the one the user named (company, person or
   time), else the next meeting that matches. Take its title, start time with time zone,
   attendees (names and emails) and description. If several could match, ask which.
2. **Sort the attendees** into colleagues (the user's own email domain) and external people.
   The company is the external attendees' email domain (ignore webmail such as gmail.com) or the
   title.
3. **Look them up.** Once a person or company is resolved, call `entity_brief` with `entity`
   set to its ID (`org_…`, `per_…`).
   - Each external attendee: `search` their email address. It finds the person and their
     company by email and domain. If it finds no person, `search` the name. Then
     `entity_brief` for each person found. Note roles and past companies (`former_employee_of`).
   - The company: the organization those searches found (its domain matches the attendees'
     email domain); else `search` its name or domain. Then `entity_brief` with
     `thesis_check: true`, which adds how it fits the firm's thesis (cached). Its `met_by` and
     `interactions` say which colleagues have met them and when. If its `coverage` is
     "crm_only" (CRM record only), offer the backfill below before writing the brief.
   - Related companies that matter: `similar_to`, a founder's past company, and the lead
     investor. For any with status `passed`, get the reason with `search` for "<name> pass".
   - Open threads: `search` "<company>" with `limit: 20` and read the snippets of the latest
     emails and meetings for requests that have not been answered.
4. **Write the brief**, short and scannable:
   - **Meeting**: title, time, attendees with their role, and which colleagues have met them.
   - **Where we are**: the deal stage and since when (the brief's `process.stage`), status,
     round, and the last interaction. [src] Then the stage's checklist progress ("2 of 4
     done"), the open items, and what the next stage needs (`process.next`): these are what
     the meeting can move forward. Turn an open item into a question to ask.
   - **Against our thesis**: the fit and its reason, the parts met or not met with their quotes
     [src], and the unknowns, which make good questions to ask.
   - **Key numbers**: value, as-of date and label, latest first; show changes. [src]
   - **What colleagues said**: notes quoted with author. [src]
   - **Open questions**: what the firm asked for and has not received. [src]
   - **Your follow-ups**: the user's own open ones from `entity_brief`'s `follow_ups` (what they
     owe and what they are waiting on), overdue first. Only theirs; leave out when there are none.
   - **Relevant history**: similar companies, past passes and their reasons, and why they are
     relevant here. [src]
   - **Questions to ask** (suggested): three to five, each tied to a gap above or a thesis part
     that is unknown.
   - **Sources**: the cited sources only, as `src_… title (system) <url>`.

## Backfill: a company the brain knows only from its CRM

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
