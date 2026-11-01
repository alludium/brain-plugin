---
name: tasks
description: 'Ask a colleague at the firm to do something through VC Brain, work on a task someone asked of you, and see what you asked for. Use when the user says "ask Priya to call Acme''s references before Thursday", "get Tomas to send the DPA", "work on VC Brain task T-42" (or any "T-" number from VC Brain), "what''s on my plate?", "what have people asked me for?", "what did I ask Tomas for?", "I''ve done T-42", "cancel what I asked Jonah for" or "decline T-42, I never met them".'
---

# Tasks

A task is something a firm member asked a colleague to do: what, why (in the asker's words), by
when, the companies or people it is about and what to read first. It shows up for the assignee in
VC Brain, and their answer goes back to the person who asked. Use the VC Brain connector's
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
- **No content in the reference.** "Work on VC Brain task T-42" is all a hand-over needs; load the
  rest with the tool.

## Ask a colleague

1. Resolve each company, person or deal the request is about with `search` (pass ids, not short
   names), and any source the user points to ("the deck", "my note from Tuesday").
2. Confirm, then call `follow_ups` with `ask`: `to` (emails or full names; "me" for the user's own
   task), `action` (a short imperative, at most 200 characters), `why` (the user's own words),
   `about` (entity ids), `context` (source ids), `due_on` when they gave a deadline. Leave
   `audience` as `people` (answers go back to the user only) unless they want answers shared with
   the firm.
3. Reply with the ref(s) the tool gives and any warning, in one or two lines.

## Work on a task

When the user says "work on VC Brain task T-42", clicks "Action this in Claude", or picks one from
their list:

1. Call `follow_ups` with `task: "T-42"`. Tell the user in two lines who asked, what and why, and
   the due date.
2. Read what it is about (`entity_brief` for each entity in `about`) and the `context` sources,
   then do the work with the user, using their own connectors (email, calendar, notes, drive) as
   the task needs.
3. When the work is done, draft the outcome in a few sentences: what was done and what was found,
   with any figures cited to their sources. Show it to the user.
4. On their yes, call `follow_ups` with `update: [{id: "T-42", status: "done", outcome: "…"}]`.
   If they want to save a note or document for the firm too, use the `note` or `drop` skill as
   usual and say so.
5. If the user can't or won't do it, `update` with `status: "dismissed"` and a `reason` they
   agree; the person who asked sees it.

## Your lists

- **Asked of you**: `follow_ups` (default view) lists the user's follow-ups and the tasks
  colleagues asked of them; a row with `request` is a task, `request.requested_by` asked for it.
  Overdue first.
- **You asked**: `follow_ups` with `view: "asked"` lists what the user asked others for and where
  each stands (open, done with its outcome, declined with a reason, cancelled).
- **A request to several people**: its own ref (`follow_ups` with `task`) gives who has opened,
  done or declined theirs. It never shows a draft.
- **Cancel**: only for a task the user asked for: `update` with `status: "cancelled"` (the request's
  ref cancels every open task in it).
