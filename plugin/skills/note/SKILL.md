---
name: note
description: 'Save a short note, judgement or correction about a company, person, fund or deal to the firm''s VC Brain. Use when the user says "note on Acme: …", "note that …", "remember that …", "add to the brain: …", or gives a quick take after a call. Also use it to offer, never silently, when the user voices a view on one without asking to save it. Links the note to the right entities, keeps it private by default and offers to share it with the firm. Also comments on a document in the brain ("comment on the Acme memo''s Risks: …", "review this memo and comment"), replies, and resolving a thread.'

description: 'Save a short note, judgement or correction about a company, person, fund or deal to the firm''s VC Brain. Use when the user says "note on Acme: …", "note that …", "remember that …" about a company or person, "add to the brain: …", or gives a quick take after a call. Links the note to the right entities, keeps it private by default and offers to share it with the firm. Not for the user''s own preferences or standing instructions ("remember that I…", "always…"), which go to the profile skill.'
---

# Note

A note is a few lines a person wrote, stored in their own words and linked to the entities it is
about. Use the VC Brain connector's `search` and `capture` tools.

## Rules

- **The user's words, unchanged.** The note text is what the user said after "note on X:" (or
  the whole remark if there is no prefix). Do not rewrite, expand, summarise or correct it.
- **Link to the right entity.** Never pass a short or shared name such as "Acme" to `capture`:
  it can link to the wrong company or create a duplicate. Resolve it with `search` first.
- **Private by default.** Use `scope: "private"` unless the user asked to share it ("for the
  team", "share with the firm", "firm note"), then use `scope: "firm"`.
- **Source IDs.** If the note came from another system (a Slack message, an email, a CRM note),
  pass that record's `system`, `external_id` and `url` exactly as the connector gave them. A note
  typed in this chat has none; leave them out. Never invent an ID or link.
- **Offer, don't file silently.** If the user gave the view without asking to save it, offer
  once in one line ("Note this in VC Brain, private to you?") and file only after a yes. Offer
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
   - Link people the note names (a founder, a co-investor) only when they resolve clearly.
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
4. Check the result. If it created an entity you expected to be linked, tell the user that a
   new entity was created and name it. If it reports a tag as suggested, or warns about one,
   say so in a few words. If it returned a note that was already stored (the same
   text from the same author), say it was already saved; it was not stored twice.
5. Reply in one or two lines: what it was linked to, the source ID, and the scope. If it is
   private, offer to share it in the same reply, for example: "Saved to Acme AI Ltd
   (src_…), private to you. Share it with the firm?"
6. If the user says yes, call `share` with the source ID and `scope: "firm"`, and reply in one
   line: "Shared with the firm (src_…)." Do not capture it a second time as a firm note. To make
   a note private again, call `share` with `scope: "private"`. Only the note's author can
   change its scope; if `share` says so, tell the user.

## A draft Claude wrote

When the user asks to file something Claude drafted from the brain (an IC memo, an LP update, a
deal summary), it is the author's document, not a note. File it only on their say-so, with
`capture`:

- `kind: "document"`, a title naming what it is, and `text`: the draft exactly as the author last
  saw it, markdown included, with no reply text around it;
- `scope: "private"` unless they say to share it, and `entities` linked by `id`;
- `system: "claude"` and `external_id` `<doc-type>/<entity id>/<author email>` (for example
  `lp-update/fund_…/clara@northwind.vc`), always; an artifact's link goes in `url`;
- no `facts`: its figures are already in the brain under their own sources.

Filing an edited draft again with the same `system` and `external_id` stores a new version of it,
keeping its scope, and briefs show only the latest. A `.docx` or `.pdf` export is a file: use
`drop`. Then offer to share it, as for a note. The `ic-prep` skill does this for IC memos.

## Comments on a document

A comment sits on a passage of a document in the brain (a filed draft, an upload) and is shown
there to everyone who can see it, in VC Brain's viewer too. Use `capture` with `comment`:

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
