---
name: profile
description: 'Save and manage the user''s own private memory in Alludium Brain. Use for requests to remember how the assistant should respond to or address the user (recurring format, language or tone), even without a named Brain task. Use for explicit remembering ("Remember: start every brief with risks", "remember that I…"), clearly stated ongoing preferences ("I like my briefs short", "I prefer…", "from now on…", "always…", "never…"), corrections, "forget that", "show my profile", or learning a writing style. Capture ongoing preferences even when mentioned during another task; do not merely promise to follow them in this chat. One-off requests and inferred preferences are not authorization to save. Not for company/person facts (use note) or firm-wide conventions (use onboard).'
---

# Your profile

The profile is the user's own memory in Alludium Brain: their preferences, remembered instructions and
writing style. Only they can see it; it is never searched, summarised or shared with the firm, and
it follows them to any host connected to the brain (Claude, ChatGPT, the nightly run). Use the
connector's `configure` tool with `me`, always on its own (no firm sections in the same call).
The connector lists `me` by name and one line; if a change below needs a field this skill does not
show, `configure(describe=["me"])` returns every field and allowed value before you write.

## Rules

- **About the user, not about others.** "Remember that I sit on Ferrolith's board" goes here.
  "Remember that Acme's CFO left" is a note about a company: use `note`. A firm-wide rule ("our
  memos use these headings", "deal stages are…") is firm configuration: use `onboard`.
- **Save clear ongoing preferences now.** An explicit "remember" request authorizes saving; do
  not ask again. Also save a clearly stated ongoing preference ("I like my briefs short") without
  requiring the word "remember", including when the user mentions it during another task. This is
  their private profile, not consent to file or share company material. A clear request to remember
  how you should respond requires a profile write before your final answer; applying it only in
  this chat is not completion. General response preferences (language, tone, forms of address or
  recurring format) belong to `general`, even when no Brain task is named. Tell them what you saved.
- **Do not turn a one-off request into memory.** "Shorten this answer" or "for this brief only"
  applies to the current task. Never infer and save a preference from behaviour or repeated edits
  without asking. You may offer once: "Shall I remember that you like shorter briefs?" Quoted
  examples, another person's preferences and hypothetical statements are not the user's preference.
- **Inferred writing styles need approval.** A writing style is saved pending; the server uses it
  only after `approve_style`, which you call only on the user's yes. This separate style approval
  does not apply to preferences the user directly stated.
- **The profile never changes who can see what.** An instruction such as "share my notes on
  portfolio companies" can inform a note audience recommendation, but is not consent. The note
  skill asks before filing unless explicit authorization during this conversation already covers
  the note and audience, including an earlier turn.
- **Never store secrets.** No passwords, keys, personal data about others beyond a name, or
  anything the user asks you not to keep.
- **Role and focus come from the team.** The profile shows the user's role and focus areas from
  their member entry in the firm configuration. To change those, use `onboard` (the team is
  visible to the firm). A private note about their role ("I lead our climate deals") can be an
  `about` item.

## Remember something

1. Read the current profile with `configure(me={})`. For an explicit correction, edit the matching
   item rather than leaving contradictory old and new items. If the same preference already exists
   for the same topic, keep it once; the same wording for different topics is separate guidance.
   If a save cannot be verified, say so; do not claim it was remembered.
2. Turn what the user said into one or more faithful, concise items. Preserve exact requested
   headings, limits, exceptions and scope; do not invent a broader rule or save conversational filler.
   Keep their exact original words in `said` when rephrasing:
   - `preference`: how they like work done, with a `topic`: `briefs`, `meeting_prep`, `digest`
     (what's new), `notes`, `writing`, `never` (what never to do) or `general`. For example
     "Briefs: lead with the decision needed, then the numbers; at most 10 lines."
   - `instruction`: a standing rule, for example "Always cc Priya Raman on portfolio updates",
     "Don't offer intros for crypto companies". Give it a `topic` if it is about one kind of task.
   - `about`: their role or focus in their own words.
   - **For one firm skill**: a preference or instruction with `topic: "skill:<name>"`, for example
     `skill:ic-prep` "Lead my IC memos with the risks", or `skill:reach-out` "Never mention our
     fund size". It is added to that skill each time they run it, and to nothing else. Use the
     skill's name as `configure`'s description lists it. If they want the procedure itself to
     differ, not just a line of guidance, offer their own version of the skill (the `playbook`
     skill).
3. Call `configure` with `me: {"add": [{"kind": …, "topic": …, "text": …, "said": "<their words>"}]}`,
   or `edit` for a matching correction. Use the returned saved item and its ID to verify the result.
   If the tool fails, do not promise future recall: explain that saving failed. A conversational
   acknowledgement by itself is not a save.
4. After success, briefly say what was saved, for example "Remembered: always cc Priya on portfolio
   updates [prf_…]. Only you can see this." When also producing requested work, lead with that work,
   not the save acknowledgement. Put the concise confirmation after the work when it fits, or keep
   it clearly separate from the deliverable. Never let administrative confirmation displace the
   requested opening or ending, or exceed an applicable length limit.

## Show, change or forget

- **Show**: `configure` with `me: {}`. Show the profile grouped as it comes back, with each item's
  ID, where it came from and when. Do not add anything of your own.
- **Change**: `me: {"edit": [{"id": "prf_…", "text": "…", "topic": "…"}]}`.
- **Forget**: `me: {"forget": ["prf_…"]}`; forgetting the writing style's ID also removes its
  examples. "Forget everything about me" is `me: {"forget": ["all"]}`: confirm once first,
  wait for the user's yes, then delete. Permission to save a preference does not waive this check.
- When the user names an item by its words rather than its ID, read the profile first and pick
  the item; if two could match, ask which.

## Learn my writing style

Only when the user asks, and only from text they wrote themselves.

A style is for one **purpose**. `general` is for anything drafted in their name. Five more are for
one kind of message each, and a draft of that kind uses that style in place of the general one:

| Purpose | Learn from their own… | They might say |
|---|---|---|
| `outreach_cold` | first messages to people they had not met | "learn how I write cold emails" |
| `intro_request` | messages asking someone to introduce them | "look at my past intro asks" |
| `intro_double_opt_in` | introductions they made between two people | "learn from my intros" |
| `follow_up` | nudges and follow-ups after no reply or a meeting | "how I follow up" |
| `decline` | messages saying no | "learn how I pass on companies" |

Pick the purpose from what they asked for. If it is unclear, ask: "Is this for your general
writing, or one kind of message, such as cold emails?" Keep to one purpose per style. Never mix
cold emails and declines into one style.

1. **Ask which text**, if they have not said: their sent emails (through the mail connector, for
   example "my last 10 emails to founders"), memos or documents they wrote (through Drive or
   another connector), or notes they wrote in the brain (`search`, then only sources whose author is
   them: the server refuses anyone else's). For a purpose, keep only messages of that kind: a
   decline style learns from declines, not from every sent email. Skip forwarded or quoted text and
   other people's replies. Six to twelve pieces are enough (five for a purpose, if that is all
   they have).
   **Mail fetched through a connector**: offer to file the messages you will learn from, private,
   with `capture` (their system and message IDs, `scope: "private"`), before saving the style. Then
   cite each one by its `source_id`, so the excerpts stay references into their own filed mail and
   go if they delete it. File them only on their yes. If they say no, cite the messages by system and
   external ID instead.
2. **Describe the style** in five to eight short lines: tone, typical length, structure (bullets
   or prose, what comes first), how they open and sign off, words or habits they use, and what
   they avoid. Pick two or three short excerpts (a few sentences each, word for word) that show it
   best and hold nothing they would not want kept in their profile.
3. **Save it pending** with `me: {"style": {"purpose": "<purpose>", "description": …, "learned_from": "<what, as they
   chose it, e.g. 10 sent emails to founders, October 2026>", "sources": [{"system": "gmail",
   "external_id": …, "title": "<subject>"}, …], "examples": [{"text": "<excerpt>", "system": …,
   "external_id": …, "title": …}]}}`. For a brain note, give `{"source_id": "src_…"}`, and for its
   excerpt `{"source_id": "src_…", "text": "<exact words from it>"}`: the server keeps only its
   place in the note, so the excerpt goes if the note is deleted. A new pending style replaces an
   earlier pending one of the same purpose. The current style for that purpose stays in use
   meanwhile, and styles for other purposes are not touched.
4. **Show it to the user** exactly as the result gives it (description and examples) and ask: "Save
   this as your writing style?" For changes, save it again (step 3). On a no, `forget` its ID.
5. **On their yes**, call `me: {"approve_style": "prf_…"}` with the pending style's ID. It replaces
   the current style of the same purpose. Reply in one line: "Saved your writing style for cold
   emails (learned from …) [prf_…]" (or "your writing style" for the general one).

## When the digest offers a style

`whats_changed` gives `style_nudges` once five or more of the user's own sent emails of one purpose
have arrived since that purpose's style was approved, or ever, with none yet. These emails were
classified when they were filed. Offer the update in one line, and on the user's yes, follow "Learn
my writing style" above for that `purpose`. Read the emails by their `source_ids`: they are already
the user's own filed sources, so cite them by `source_id`. When updating, start from the current
style and change only what the new emails show. Save it pending and show it as usual. Never draft
or save one unasked. If they say "not now", call `me: {"not_now": "<purpose>"}`: the offer comes
back only after five more of their emails of that purpose.

## How other skills use it

`brief`, `prepare-meeting`, `whats-new` and `note` read fresh task guidance at the start of each
new task using `configure(me={"task":{"topic":"briefs"}})` (choose its topic; add `skill` for a
firm workflow). For drafts in the user's name, use topic `writing` and the writing `purpose` when
known. `me: {}` still reads the complete profile for showing, editing or forgetting items.
If an older server returns the whole profile, select only active task/general/never and matching
skill guidance, never pending styles or unrelated topics. Follow it: it changes length, order, emphasis and voice, never citations, what is cited, or
who can see what. Only approved styles are used, never a pending one. For a draft of one purpose
(a cold email, an intro request, a decline), use that purpose's style from `styles` for voice, else
the general `style`. The firm's template for that kind of message, if it has one, still decides
what the message must contain. A request in the
moment overrides the profile for that task. Drafts in the user's name (the `ic-prep` memo, an email)
use the writing style; firm documents keep the firm's own conventions (headings, sections) from the
firm configuration.


For “open my account/settings” or workspace switching, call `open_account()` to show
the account card. For “which workspace am I in?” or a background identity check, use
`configure(account={})` to read the data without opening a card. Reuse the current
`workspace_context`; do not repeat this lookup before every Brain call. Include that
context on either tool to retain the current selection. Pass `account` alone to configure.
The card can approve an additional workspace in the signed-in browser and select it for
this chat without reconnecting the assistant. Approval is explicit, revocable and lasts
up to eight hours; membership alone is not approval.

Use the returned `workspace_context` on **every Brain tool call**, including uploads,
profile changes and skill loading. After the user changes the card selection, read its
visible selection message and replace the previous reference. If the host places the message
in its composer, the user sends it to confirm; “Tell assistant” retries a failed handoff.
Never retry a rejected context by omitting it. Open a fresh account card and let the user
choose again. Do not claim success until the authenticated result names the selected
workspace. Existing work already admitted keeps its original workspace. Other chat
contexts retain their selections; removing workspace approval invalidates all contexts
using that approval. These references route calls, not isolate chats sharing one credential.
