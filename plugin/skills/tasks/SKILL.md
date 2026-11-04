---
name: tasks
description: 'Ask a colleague at the firm to do something through Alludium Brain, collate what everyone at the firm knows about a company, work on a task someone asked of you, and see what you asked for. Use when the user says "ask Priya to call Acme''s references before Thursday", "get Tomas to send the DPA", "collate what everyone knows about Acme AI before IC", "ask whoever covers security to look at Acme", "ask everyone for their Q4 travel", "work on Alludium Brain task T-42" (or any "T-" number from Alludium Brain), "what''s on my plate?", "what have people asked me for?", "what did I ask Tomas for?", "I''ve done T-42", "cancel what I asked Jonah for", "decline T-42, I never met them", "ask Tomas for access to that meeting" or "share it with Clara" (an access request).'
---

# Tasks

A task is something a firm member asked a colleague to do: what, why (in the asker's words), by
when, the companies or people it is about and what to read first. It shows up for the assignee in
Alludium Brain, and their answer goes back to the person who asked. Use the Alludium Brain connector's
`follow_ups`, `search` and `entity_brief` tools. Tasks are referred to by ref, like `T-42`.

## Rules

- **Firm members only.** Tasks go to members of the firm, by email or full name. A first name is
  fine only when one member has it; if the tool says someone is not a member, ask the user.
- **Confirm before asking.** Show the user who, what, why, when and what it is about in two or
  three lines, and call `follow_ups` with `ask` only after a yes.
- **Asking shares nothing.** A source the user links in `context` is shown only to colleagues who
  can already see it. If the tool warns that someone can't see one, tell the user and offer to
  share it (`share`) or to say what matters in `why`. Never share without their yes.
- **The answer is the user's.** When finishing a task, draft the outcome from the work done in
  this chat, show it, and send it only once the user agrees it. It goes to the person who asked.
- **Nothing is shared without a yes.** Notes and documents made for a task are private to the user
  until they approve them in the review step below. Never pass `share` before that yes, and pass
  only the ids they approved; there is no "share all".
- **A collation shares only what each person approves.** Nobody else's material is read: each
  colleague's own Claude looks through their own email and notes, and the person who asked sees
  only where each stands until that colleague approves what they share.
- **No content in the reference.** "Work on Alludium Brain task T-42" is all a hand-over needs; load the
  rest with the tool.

## Ask a colleague

1. Resolve each company, person or deal the request is about with `search` (pass ids, not short
   names), and any source the user points to ("the deck", "my note from Tuesday").
2. Confirm, then call `follow_ups` with `ask`: `to` (emails or full names; "me" for the user's own
   task; `"everyone"` for every member but the user; `{"responsibility": "security"}` or
   `{"focus": "fintech"}` for whoever covers it in the firm's playbook), `action` (a short imperative, at most 200 characters), `why` (the user's own words),
   `about` (entity ids), `context` (source ids), `due_on` when they gave a deadline. Leave
   `audience` as `people` (answers go back to the user only) unless they want answers shared with
   the firm.
3. Reply with the ref(s) the tool gives and any warning, in one or two lines. When `to` was
   everyone or a responsibility, name who it went to: if someone was not meant to be asked, offer to
   cancel their task.

## Ask for access to a meeting or email

A brief, the network or meeting prep may say a colleague met someone in a meeting or email that
is not shared with the user ("not shared with you", with its ids). Only who, which company, when
and which kind show; never guess what it said.

1. Confirm: "Ask whoever filed it to share it with you? They decide, and you're told either way."
2. On a yes, call `follow_ups` with `ask: {kind: "access", access: ["src_…"], why: "…"}` (the
   user's words, optional). Leave out `to` and `action`: each item's author gets the task.
3. Reply with who was asked and the ref. Something already asked for is not asked again (the
   tool says so). Once shared, the user can open it like any other source.

## Answer an access request

When the task loaded with `follow_ups` is an access request (`request.kind: "access"`), a colleague
asked to see meetings or emails the user filed. The task lists them; the user can open each.

1. Tell the user who asked, which meetings or emails (kind, date, who was on them) and why.
2. It is the user's call. Share: `follow_ups(update=[{id: "T-42", status: "done"}])`, which lets
   the colleague open them as the user can (and the other records of the same meeting the user
   filed). Decline: `status: "dismissed"`, with a `reason` only if the user gives one.
3. Never share without the user's yes.

## Collate what the firm knows

For "collate everything everyone knows about Acme AI before Thursday's IC":

1. Resolve the company (or person, fund or deal) with `search`.
2. Confirm in two lines: who will be asked (everyone, named people, or whoever covers something),
   what about, by when, and that each person's notes are shared **with the firm** once they
   approve them (unless the user wants them to come back to the user only: `audience: "people"`).
3. Call `follow_ups` with `ask`: `kind: "collate"`, `to`, `action` ("Tell me what you know about
   Acme AI"), `why` in the user's words, `about` (the entity id), `due_on`. Each person gets their
   own task and email. Reply with the request's ref (`T-40`).
4. Later, `follow_ups` with `task: "T-40"` gives who has opened, has a draft ready, is done or
   declined, and `combined`: the notes and documents shared so far, each with its author. A draft
   is never shown; don't guess what is in it.
5. To write it up, brief from the shared sources (cite their ids, as with any source); the brain
   stores no combined summary. A summary of the user's own is their note (the `note` skill), citing
   the contributions.

## Work on a collation

When the task loaded with `follow_ups` has a `collation`, someone is gathering what the firm knows.
The tool's text lists the steps; in short:

1. Tell the user who is collating, about what, and by when, and that nothing they have is shared
   until they approve it.
2. Start from what the firm already knows: `entity_brief` for each entity in `collation.about`.
   Don't re-file anything already there.
3. With the user's own connectors in this chat, look for email threads with the company's people,
   meeting notes (Granola, Fireflies and others) and documents in their drive; `search` also
   returns the user's own private notes. Read; don't file yet.
4. Draft **one note**: what the user knows that the firm does not, each claim citing where it came
   from (a source id, or the email or meeting by date and subject). Pick a short list of documents
   worth adding, skipping any `search` finds by title already. Nothing found is a fine answer.
5. File the draft with `capture` (`kind: "note"`, `task: "T-41"`, no `scope`) and documents with
   `request_upload` (`task: "T-41"`). They are private drafts. If you capture an email or meeting so
   the note can cite it, it stays private too: don't offer it for sharing unless the user asks.
6. Review as below: show the note word for word and each document's title, and say who will see
   them once approved (`collation.shared_with`, usually the firm). The user may edit the note
   first (capture the edited text again and offer that one), untick documents, send it to the
   person who asked alone (`audience: "people"`), or say there is nothing to add. Share only on
   their yes, only the ids they approved.
7. "Nothing to add" is an answer too: show the user the outcome the person who asked will read, and
   complete the task (`status: "done"`, no `share`) only once they agree.

## Work on a task

When the user says "work on Alludium Brain task T-42", clicks "Action this in Claude", or picks one from
their list:

1. Call `follow_ups` with `task: "T-42"`. Tell the user in two lines who asked, what and why, and
   the due date.
2. Read what it is about (`entity_brief` for each entity in `about`) and the `context` sources,
   then do the work with the user, using their own connectors (email, calendar, notes, drive) as
   the task needs.
3. To keep a note for the task (call notes, a write-up), file it with `capture` and `task: "T-42"`;
   to add documents, `request_upload` with `task: "T-42"` (as the `drop` skill does). Leave
   `scope` out: they are stored private to the user and linked to the task as drafts. The person
   who asked sees only that a draft is ready, never what is in it.
4. When the work is done, draft the outcome in a few sentences: what was done and what was found,
   with any figures cited to their sources.
5. **Review before sharing.** Show the user, exactly:
   - the outcome text, word for word;
   - each note or document made for the task (`follow_ups` with `task` lists them under
     `outcomes`), each as its link with its title;
   - who will see what they approve: the person who asked and the user ("only you and Clara"),
     or the firm when the request says `audience: firm`. They can choose instead: `audience:
     "firm"`, or a group's name when both they and the person who asked are in it (the person who
     asked always sees an approved answer, so a group without them is refused).
   Ask which to share. Approve only on a yes: anything they leave out stays private and stays
   linked to the task.
6. Call `follow_ups` with `update: [{id: "T-42", status: "done", outcome: "…", share: ["src_…"]}]`,
   adding `audience` only when the user chose one. Leave `share` out to complete without sharing
   anything. Report what the tool says was shared, and with whom. If it refuses a source (not the
   user's, synced from a drive, an old version), say why and ask again.
7. If the user can't or won't do it, `update` with `status: "dismissed"` and a `reason` they
   agree; the person who asked sees it.

## Your lists

- **Asked of you**: `follow_ups` (default view) lists the user's follow-ups and the tasks
  colleagues asked of them; a row with `request` is a task, `request.requested_by` asked for it.
  Overdue first.
- **You asked**: `follow_ups` with `view: "asked"` lists what the user asked others for and where
  each stands (open, draft ready, done with its outcome, declined with a reason, cancelled). A
  done task's `outcomes` are the notes and documents shared back: cite their ids.
- **A request to several people**: `view: "asked"` lists each one under `requests` with how many
  stand where; its own ref (`follow_ups` with `task`) gives who has opened, done or declined
  theirs, and `combined` (what was shared, by whom). It never shows a draft.
- **Cancel**: only for a task the user asked for: `update` with `status: "cancelled"` (the request's
  ref cancels every open task in it).
