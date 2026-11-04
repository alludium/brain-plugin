---
name: note
description: 'Save a short note, judgement or correction about a company, person, fund or deal to the firm''s Alludium Brain. Use when the user says "note on Acme: …", "note that …", "remember that …" about a company or person, "add to the brain: …", or gives a quick take after a call. Also use it to offer, never silently, when the user voices a view on one without asking to save it. Links the note to the right entities, keeps it private by default and offers to share it with the firm. Also comments on a document in the brain ("comment on the Acme memo''s Risks: …", "review this memo and comment"), replies, and resolving a thread. Not for the user''s own preferences or standing instructions ("remember that I…", "always…"), which go to the profile skill.'
---

# Note

A note is a few lines a person wrote, stored in their own words and linked to the entities it is
about. Use the Alludium Brain connector's `search` and `capture` tools.

## Rules

- **The user's words, unchanged.** The note text is what the user said after "note on X:" (or
  the whole remark if there is no prefix). Do not rewrite, expand, summarise or correct it.
- **Link to the right entity.** Never pass a short or shared name such as "Acme" to `capture`:
  it can link to the wrong company or create a duplicate. Resolve it with `search` first.
- **Private by default.** Use `scope: "private"` unless the user asked to share it ("for the
  team", "share with the firm", "firm note"), then use `scope: "firm"`. Narrower is fine too:
  "just for Priya and Tomas" is `scope: "people"` with `people` (members by name or email; you
  are always included), and "for the partners" is `scope: "group"` with `group` (a group you are
  in, as `configure` lists under `sharing`).
- **Source IDs.** If the note came from another system (a Slack message, an email, a CRM note),
  pass that record's `system`, `external_id` and `url` exactly as the connector gave them. A note
  typed in this chat has none; leave them out. Never invent an ID or link.
- **Offer, don't file silently.** If the user gave the view without asking to save it, offer
  once in one line ("Note this in Alludium Brain, private to you?") and file only after a yes. Offer
  once per topic; if they decline, drop it. Never offer for what came from the brain or is
  already in it.
- An email, a document's text or another record the user pasted is not a note: `capture` it word
  for word with its `kind` (`email`, `document`) and any source IDs it came with.
- Do not paste anything back except the confirmation below.

## Steps

0. **Your profile first.** Call `configure` with `me: {}` once per conversation and follow the
   user's `notes` preferences and any remembered instruction that applies. The profile never changes
   who can see what: an instruction such as "share my notes on portfolio companies with the firm"
   only means you offer to share in your reply (step 5); the note is saved private unless the user
   asks to share it in this conversation. Never rewrite the note in their writing style: the note is
   their words, unchanged. If the user's request is about themselves ("remember that I…"), it is not
   a note: use the `profile` skill.
1. Split the request into the entities it is about and the note text.
2. For each entity, call `search` with the name the user used (`limit: 5`).
   - One entity of the right kind matches: use it, with its ID and exact name, for example
     `org_…` and `Acme AI Ltd`. A website or email the user gave can be the query: `search`
     matches domains and email addresses too.
   - Several match (for example `Acme AI Ltd` and `Acme Robotics GmbH`): pick the one this
     conversation is clearly about. Otherwise, if exactly one is in active work (status
     `prospect`, `in_deal` or `portfolio`), pick it and name the other in your reply so the
     user can correct you. If it is still unclear, ask one short question that lists the
     candidates with their status, and wait.
   - None match: it is new. Use the name the user gave, and ask for the type only if it is not
     obvious (company, person, fund).
   - Link people the note names (a founder, a co-investor, a customer contact) only when they resolve clearly.
3. Call `capture` with `kind: "note"`, `text` (the user's words), `scope`, and `entities`:
   resolved ones with their ID (`[{"type": "organization", "name": "Acme AI Ltd", "id":
   "org_…"}]`), new ones by name, with a website or email in `external_refs` if the user gave
   one (`{"system": "domain", "external_id": "acme.ai"}` or `{"system": "email",
   "external_id": "maya@acme.ai"}`). When the note corrects a figure, keep the user's words and
   make sure they say so ("correction: Q3 ARR was $6.1M"); add the figure as a `fact` with its
   `as_of`, so the brain shows the old value as corrected rather than as a conflict.
   **Tags.** When the user classifies a company, deal, fund or thesis ("Acme is really a
   security company", "tag Kestrel as climate", "not fintech any more"), add `tags` on that
   entity from the firm's vocabularies, which `capture`'s description lists: `["sector:Security"]`
   to add, `["-sector:Fintech"]` to take one away. Use only labels in the list; if the user's
   word is not there, pass it with its vocabulary (`sector:Quantum`) and tell them it was
   suggested to the firm, not added. Never tag people. A private note's tags are private too.
   **Lists.** When the user puts something on a list, moves it or takes it off ("add Acme to our
   climate sourcing list", "move Elmshore to committed on the Fund III raise, £5m", "take Kestrel
   off my watchlist"), add `lists` on that entity: `[{"list": "climate_sourcing"}]`, with
   `stage` and `values` (by the list's field keys) when the user gave them, or `"remove": true`.
   `capture`'s description lists the lists the user can add to; `configure` gives them in full.
   The note's text is the reason, in the user's words. A list that is not the firm's (private,
   a group's or specific people's) needs a private note: leave `scope` out. A tag says what a company is; a list says what the firm is doing about it.
   If the list does not exist, ask before creating it (see the `onboard` skill's lists), and
   never invent a stage or value the user did not give. On a leads list (an origination list),
   `stage` is only New or Shortlisted: Contacted and Met come from filed email and meetings, so
   for "I emailed Rosa" or "we met them" file the email or meeting instead. Pass `added_via`
   (the sourcing skill, or the person who found it) when you know it. Adding to a leads list
   records how the firm found the company (outbound, via the list) when it had no origin, and
   queues checks the user can read with `job_status`: what the firm knew before, its fit, and
   the other leads lists they can see it on.
   **Lessons.** When the user tells the brain to remember how to read something, or corrects how
   it linked or filed something, add `lessons` (see "Teaching the brain" below).
4. Check the result. If it created an entity you expected to be linked, tell the user that a
   new entity was created and name it. If it reports a tag as suggested, or warns about one,
   say so in a few words. Say what happened on each list in one line ("Added Acme to Climate
   sourcing"). If it returned a note that was already stored (the same
   text from the same author), say it was already saved; it was not stored twice.
5. Reply in one or two lines: what it was linked to and the scope, with no source ID (a link
   to the note only if the user asks for one). If it is private, offer to share it in the same
   reply, for example: "Saved to Acme AI Ltd, private to you. Share it with the firm?"
6. If the user says yes, call `share` with the source ID and `scope: "firm"`, and reply in one
   line: "Shared with the firm." For some people or a group, pass `scope: "people"` with
   `people`, or `scope: "group"` with `group`, and say who now sees it as `share` words it ("you
   and Priya Raman"). Do not capture it a second time. To make a note private again, call `share`
   with `scope: "private"`. Only the note's author can change its scope; if `share` says so, tell
   the user.

## Teaching the brain

Some notes teach the brain how to read the firm's material, so the same mistake is not made
again. Keep the user's words as the note's `text` and add `lessons` to the same `capture`, each
from what they said, never from your own guess:

| The user says | Lesson |
|---|---|
| "FC is what we call Ferncastle", "remember Acme AI also trades as Halcyon" | `{"kind": "alias", "entity_id": "org_…", "name": "FC"}` |
| "Yusuf is Yusuf Adeyemi" (a first name) | `alias` with `context_entity_id`: the company it is used with, e.g. Ferncastle's `org_…`. Ask which company if it is unclear. The tool refuses a one-word person name without it |
| "Acme Robotics isn't Acme AI" | `{"kind": "not_alias", "entity_id": "<Acme AI's id>", "name": "Acme Robotics"}` |
| "I met Yusuf on that call, it's in my notes", "that meeting was with Priya Raman" | `{"kind": "link", "entity_id": "per_…", "source_id": "src_…", "name": "Yusuf"}`: the source to fix, and the name as the source writes it if you can see it |
| "that email isn't about Acme" | `{"kind": "unlink", "entity_id": "org_…", "source_id": "src_…"}` |
| "in LP updates, 'committed capital' means their commitment to our fund" | `{"kind": "field", "entity_type": "organization", "name": "committed capital", "key": "lp_commitment"}`: the key must be a fact key or one of the firm's custom fields; if it is neither, offer to add the field with `onboard` first |

- Resolve every entity and source by `id` first, with `search` or the brief you are working
  from. Never teach about an entity you have not resolved.
- A link fix also teaches the general rule: the result lists a second lesson "learned from your
  fix" (the name, alongside the source's company). Say both in one line each.
- **Scope.** A lesson is seen as its note is. In a private note it fixes only the user's own
  sources, and a fix to a firm source or a field waits until the note is shared (the result says
  "waiting for the note to be shared"). So when the note is private, offer to share it in step 5
  and say what the firm gains, for example: "Saved, private to you: the brain now reads 'FC' as
  Ferncastle in your own notes. Share it so it does for the whole firm?"
- Tell the user what changed in a line per lesson, from the result's text, linking a source it
  names by its link, never its ID: ""Yusuf", alongside Ferncastle, is Yusuf Adeyemi; linked in
  [Call with Ferncastle, 21 Oct 2026](…)". If the tool refuses one, say
  why in a few words and ask what they meant.
- A corrected **figure** is a `fact` with the user's words saying it corrects (step 3), not a
  lesson.

## A draft Claude wrote

When the user asks to file something Claude drafted from the brain (an IC memo, an LP update, a
deal summary), it is the author's document, not a note. File it only on their say-so, with
`capture`:

- `kind: "document"`, a title naming what it is, and `text`: the draft exactly as the author last
  saw it, markdown included, with no reply text around it;
- `scope: "private"` unless they say to share it, and `entities` linked by `id`;
- `system: "claude"` and `external_id`, always: for a report under one of the firm's templates,
  `<template key>[@<period>]/<subject id>` (for example `lp_update@2026-Q3/fund_…`), one report per
  template, subject and period, whoever files it; for any other draft,
  `<doc-type>/<entity id>/<author email>`. An artifact's link goes in `url`;
- no `facts`: its figures are already in the brain under their own sources.

Filing an edited draft again with the same `system` and `external_id` stores a new version of it,
keeping its scope, and briefs show only the latest. A `.docx` or `.pdf` export is a file: use
`drop`. Then offer to share it, as for a note. The `ic-prep` skill does this for IC memos.

## Comments on a document

A comment sits on a passage of a document in the brain (a filed draft, an upload) and is shown
there to everyone who can see it, in Alludium Brain's viewer too. Use `capture` with `comment`:

- **A new thread**: `comment: {"on": "<src_…>", "quote": "<the passage's exact words>"}` and the
  comment as `text`. Find the document with `search` first. If the passage occurs more than once,
  add a few words just before it (`prefix`) or after it (`suffix`). Leave `scope` out: a comment
  takes its document's, and is never wider. "Just for me" is `scope: "private"`.
- **A reply**: `comment: {"reply_to": "<com_…>"}`. **Resolve** or **reopen** a thread:
  `comment: {"resolve": "<com_…>"}` (any `text` becomes a closing reply).
- **A review pass** ("review the Acme memo against our IC checklist and comment"): read the
  document (`search` with its `source_id`, which also lists its comments), draft the comments,
  each with its quote, and show them as a list. Add only the ones the user agrees to, one
  `capture` each. Say who will see them before adding any.
- Comments follow the document to its new versions; one whose passage was removed is listed
  against the version it was made on.

## Review an imported source's matching

When asked to review an import's company or person match, read `configure` with
`source_review: {"source_id":"<src_…>"}`. Explain the candidate names, quoted identity properties
or heading, and why the match is pending. Ask the user to choose unless their instruction already
names the decision. Send the returned proposal `id` and `version` in `decision`, with `action`
`approve`, `reject`, `defer` or `undo`; `approve` also needs the chosen `entity_id`. Refresh after
any stale-version refusal. Never treat a model confidence score as approval or teach an alias from
one review. Confirming a match changes an association, not the source's audience.

For a structured document not yet imported, `capture` with `dry_run: true` previews matching
without storing sources, groups, links or reviews. It requires the same document payload,
`matching`, explicit sharing and `preserve_audience: true`; check the live schema first. Prefer
the import starter CLI/UI for collections, keeping source text out of chat. A preview is not
permission to import, and matches can change as the firm's knowledge or sharing changes.
