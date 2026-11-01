---
name: profile
description: 'Keep the user''s own private profile in Alludium Brain: how they like their briefs, meeting prep and digests, standing instructions, and their writing style. Use when the user talks about themselves rather than a company, for example "remember that I…", "I prefer…", "always cc Priya on portfolio updates", "never…", "I don''t do intros for crypto", "learn my writing style from these emails", "what do you know about me?", "show my profile", "forget that", "change my brief preference". Not for notes about companies or people (use note) or for firm conventions such as memo headings and deal stages (use onboard).'
---

# Your profile

The profile is the user's own memory in Alludium Brain: their preferences, remembered instructions and
writing style. Only they can see it; it is never searched, summarised or shared with the firm, and
it follows them to any host connected to the brain (Claude, ChatGPT, the nightly run). Use the
connector's `configure` tool with `me`, always on its own (no firm sections in the same call).

## Rules

- **About the user, not about others.** "Remember that I sit on Ferrolith's board" goes here.
  "Remember that Acme's CFO left" is a note about a company: use `note`. A firm-wide rule ("our
  memos use these headings", "deal stages are…") is firm configuration: use `onboard`.
- **Only what the user said or approved.** Never infer a preference from their behaviour and save
  it without asking. If they correct you mid-task ("shorter, please"), you may offer once: "Shall
  I remember that you like shorter briefs?"
- **Nothing learned is used until the user approves it.** A writing style is saved pending; the
  server uses it only after `approve_style`, which you call only on the user's yes.
- **The profile never changes who can see what.** An instruction such as "share my notes on
  portfolio companies" makes skills offer to share; they never share without a yes at the time.
- **Never store secrets.** No passwords, keys, personal data about others beyond a name, or
  anything the user asks you not to keep.
- **Role and focus come from the team.** The profile shows the user's role and focus areas from
  their member entry in the firm configuration. To change those, use `onboard` (the team is
  visible to the firm). A private note about their role ("I lead our climate deals") can be an
  `about` item.

## Remember something

1. Turn what the user said into one or more items, each short and in the second person:
   - `preference`: how they like work done, with a `topic`: `briefs`, `meeting_prep`, `digest`
     (what's new), `notes`, `writing`, `never` (what never to do) or `general`. For example
     "Briefs: lead with the decision needed, then the numbers; at most 10 lines."
   - `instruction`: a standing rule, for example "Always cc Priya Raman on portfolio updates",
     "Don't offer intros for crypto companies". Give it a `topic` if it is about one kind of task.
   - `about`: their role or focus in their own words.
2. Call `configure` with `me: {"add": [{"kind": …, "topic": …, "text": …, "said": "<their words>"}]}`.
   Put their exact words in `said` when you rephrased them.
3. Reply in one line with what was saved and its ID, for example "Remembered: always cc Priya on
   portfolio updates [prf_…]. Only you can see this."

## Show, change or forget

- **Show**: `configure` with `me: {}`. Show the profile grouped as it comes back, with each item's
  ID, where it came from and when. Do not add anything of your own.
- **Change**: `me: {"edit": [{"id": "prf_…", "text": "…", "topic": "…"}]}`.
- **Forget**: `me: {"forget": ["prf_…"]}`; forgetting the writing style's ID also removes its
  examples. "Forget everything about me" is `me: {"forget": ["all"]}`: confirm once first.
- When the user names an item by its words rather than its ID, read the profile first and pick
  the item; if two could match, ask which.

## Learn my writing style

Only when the user asks, and only from text they wrote themselves.

1. **Ask which text**, if they have not said: their sent emails (through the mail connector, for
   example "my last 10 emails to founders"), memos or documents they wrote (through Drive or
   another connector), or notes they wrote in the brain (`search`, then only sources whose author is
   them: the server refuses anyone else's). Skip forwarded or quoted text and other people's
   replies. Six to twelve pieces are enough.
2. **Describe the style** in five to eight short lines: tone, typical length, structure (bullets
   or prose, what comes first), how they open and sign off, words or habits they use, and what
   they avoid. Pick two or three short excerpts (a few sentences each, word for word) that show it
   best and hold nothing they would not want kept in their profile.
3. **Save it pending** with `me: {"style": {"description": …, "learned_from": "<what, as they
   chose it, e.g. 10 sent emails to founders, October 2026>", "sources": [{"system": "gmail",
   "external_id": …, "title": "<subject>"}, …], "examples": [{"text": "<excerpt>", "system": …,
   "external_id": …, "title": …}]}}`. For a brain note, give `{"source_id": "src_…"}`, and for its
   excerpt `{"source_id": "src_…", "text": "<exact words from it>"}`: the server keeps only its
   place in the note, so the excerpt goes if the note is deleted. A new pending style replaces an
   earlier pending one; the current style stays in use meanwhile.
4. **Show it to the user** exactly as the result gives it (description and examples) and ask: "Save
   this as your writing style?" For changes, save it again (step 3). On a no, `forget` its ID.
5. **On their yes**, call `me: {"approve_style": "prf_…"}` with the pending style's ID. It replaces
   the current style. Reply in one line: "Saved your writing style (learned from …) [prf_…]."

## How other skills use it

`brief`, `prepare-meeting`, `whats-new` and `note` read the profile first (`configure` with `me:
{}`) and follow it: it changes length, order, emphasis and voice, never citations, what is cited, or
who can see what. Only the approved style (`style`) is used, never `pending_style`. A request in the
moment overrides the profile for that task. Drafts in the user's name (the `ic-prep` memo, an email)
use the writing style; firm documents keep the firm's own conventions (headings, sections) from the
firm configuration.
