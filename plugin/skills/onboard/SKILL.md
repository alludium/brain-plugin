---
name: onboard
description: Alludium-owned Brain onboarding skill, available through the plugin or configure(skill="core:onboard") over MCP; its references are included when loaded through MCP. Use when the user explicitly requests the Brain onboarding skill, including advice-only import questions. Otherwise, onboard every member to Alludium Brain person first, including the first member of a new firm. For a new firm, use public sources and connected tools to propose cited setup, then confirm gaps, systems, CRM import, nightly filing and team. For later users, set up their profile, connections and nightly run, and show what Brain knows. Also update firm configuration including fit/thesis/ICP and criteria, deal stages and checklists, funds, fields, tags, members and focus, memo headings and house style, and mail filing rules. Use for "onboard us", "onboard me", "set up our firm", fund documents, or changes to those settings. Not for company notes (use note), deal decisions (use log-decision), or personal preferences (use profile).
---

# Onboard

Start with what Brain already knows about the person, for every member including the first. Read the cited public research and confirmed private profile before opening; offer a tentative understanding and useful suggestions, then ask only about gaps. Make it easy to correct you or start a task.
Everything goes through the Alludium Brain connector's `configure` and `capture` tools. How
`configure` works (each section, `systems`, `connections`, `cites`, tags) is in
`references/configure.md`; read it before the first write. The connector lists each section only
by name and one line: before the first write of a section in a conversation, call `configure`
with `describe` and every section you will write (`describe: ["fit", "process", "members"]`), and
follow the fields, allowed values and rules it returns.

After the personal introduction, use known evidence to propose what the firm does and who is on
the team. Ask a partner or lead only about gaps, confirm the proposal, then save it with the Alludium Brain connector's `configure` tool. What the firm's setup
asks comes from the server: the firm's packs, set by Alludium when it created the organisation,
each name the sections they need, as questions in their own words. It is safe to run again: it always
starts from the stored configuration and proposes changes to it.

## Connection and scripted-import guidance

For installation help or a message to colleagues, read `references/install.md`. Match the
person's host: Claude app, Claude Code, ChatGPT (workspace GitHub import or permitted ZIP,
respecting Desktop only labels), Codex desktop or CLI (plugins), or the IDE extension (tools only). Use the host context when known; ask only when unclear.
If the connector is unavailable, help connect it before calling tools. Once connected, use
`configure` with `account: {}` to check the signed-in person and firm before onboarding writes.
Do not claim installation or sign-in succeeded just because a ZIP was downloaded.

For questions about bringing existing data in, use the **import-data** skill for advice before
setup. It chooses among direct connections, assistant filing, uploads and CLI/custom readers.
If that skill is unavailable, read `search(source_id="help:feed/import-existing-data")` and the
linked guide for the relevant route. An import-options question is not permission for a full
onboarding interview, configuration changes or imports. Reuse the user's stated source and
one-off/recurring preference. Do not ask them to paste a collection into chat.

## How `configure` works

- `describe: ["<section>", …]`, alone, returns each section's fields with their allowed values,
  its rules, who may change it (`Who:`; "not you" means ask the person it names, never try) and
  its current value, with `config_version`. Describe a section before you first write it in a
  conversation. A refused update names each wrong value and the sections to describe: describe
  them, correct the values and call again; never drop a section to get past a refusal.
- With no arguments it returns the current configuration, and `proposals`: configuration the
  brain proposed from the firm's own documents, waiting for a decision. Each has an `id`, a
  `section` (`process`, `thesis` or `funds`), the proposed `value`, the `quotes` it rests on, and
  what is `configured` now; a thesis proposal also has `adds`, what accepting it adds. Nothing in
  a proposal is applied until someone accepts it.
- Accepting a thesis proposal only adds to the thesis: it fills an empty statement or cheque and
  adds the stages, sectors, regions and criteria it lacks; it never removes or replaces what is
  configured. To change or drop a part, pass the edited `fit` with the acceptance.
- `proposals: [{"id": "cfp_…", "decision": "accept"}]` applies a proposal; `"dismiss"` drops it.
  To accept with changes, pass the edited section in the same call as the acceptance: the
  edited section wins.
- `funds` is the firm's funds (name, vintage, size, `currency`, `cheque`, strategy); it replaces
  the list, and each fund becomes a Fund in the brain. Always give each fund's currency (an ISO
  code such as GBP); nothing defaults to dollars. `cheque` is the fund's own first cheque,
  `{"min": 500000, "max": 1000000}`, in the fund's currency. `mandate` is what the fund may invest
  in, from its LPA or the partners' words: `{"statement", "stages", "sectors", "regions", "since"}`
  (`since` is the date it took effect). Changing a fund's mandate sends the firm's learning-run
  insights back for review; say so before saving it.
- Each section you pass (`fit`, `process`, `funds`, `custom_fields`, `members`,
  `memo_headings`, `house_style`, `templates`, `routines`) **replaces** the stored one. To add one criterion or one
  person, pass the whole thesis or the whole team. Never pass a section that is not changing.
- The fit profile is the `fit` section (shown to a venture firm as its thesis; `thesis` is its
  older name and still works, and reads return both). It is an object:
  `statement` (one sentence), `stages` (the funding stages the firm invests
  at, such as Seed and Series A, not its deal stages), `in_scope` and `out_of_scope` (sectors and
  themes), `regions`, `cheque` (`{"min": 500000, "max": 3000000, "currency": "EUR"}`, only when
  every fund's cheque is the same range in the same currency; when funds differ, give each fund
  its own `cheque` instead and leave the firm's out) and
  `criteria` (each `{"text": "...", "weight": "must" | "nice"}`, or without a weight). Leave out
  what the partner did not give. Put criteria inside `fit`; the separate `criteria` argument
  is only for older plugins. Alludium Brain checks companies against each part (`entity_brief` with
  `fit_check`), so keep each part short and specific.
- `members` is the whole team: name, email, role, `focus_areas`, `responsibilities` (what each
  person owns at the firm, in the partner's words: "IC prep", "LP reporting"). Who approves the
  firm's own skills is the `approve_skills` permission, not a member field. Focus and
  responsibilities show on each person's page. `configure` refuses a list that leaves out a current member
  and names who would be dropped. To drop someone, name them (name or email) in `remove`, only
  after the partner has said to. `remove` on its own drops those people and keeps the rest of
  the team as stored. A dropped member loses the firm-member role; the person stays.
- **Someone who left the firm** ("Tomas has left"): `deactivate` with their name or email, after
  the partner confirms. They can no longer use Alludium Brain, everything they filed stays under
  their name, and they stay on the team marked as left. `remove` of someone who has signed in does
  the same; only someone who never signed in is dropped outright. `reactivate` lets them back in.
  Both need a firm admin, and nobody can deactivate themselves.
- **Firm admins.** Removing members, `groups`, `permissions`, `email_scope`,
  `meeting_scope`, `connectors` and `origination`'s sharing, caps, models and scoring rubric change
  who sees, approves or pays for what, so once the
  firm has a firm admin (the admin role in its WorkOS organization), only admins can
  change them; `configure` names the admins and says whether the
  caller is one. If a non-admin asks, say who can do it rather than trying. While the firm has
  none, anyone can, and onboarding asks to have one made. Everything else stays open to every
  member.
- `groups` are the firm's managed groups: who a note or document can be shared with besides the
  whole firm ("Partners", "LP & finance", "Fund II deal team"). Each entry is a `name`, its
  `members` (emails or full names; they replace the group's members) and an optional
  `rename_to`; only the groups named change. `remove_groups` deletes empty ones. Firm admins
  only. When `configure` lists `group_suggestions` (from the team's titles), offer them once
  ("Make a Partners group of Alice and Bob, so partner-only notes can be shared with just
  them?"); never create a group nobody asked for, and a title is never a reason to add someone.
- `permissions` says which groups, besides the admins (who hold every permission), hold each one:
  `approve_skills` (approve, restore or retire the firm's skills, never one's own version;
  everyone by default), `approve_policy` (adopt a learning-run insight as the firm's rule),
  `final_decider` (who decides passes, investments and losses; advisory: `log_decision` notes a
  decider outside it and never refuses; everyone by default), `manage_billing` (the firm's
  money: firm Searches today, the plan, boosters and invoices later; adding packs stays with
  admins) and `run_firm_reports`, each a list of managed group names or `"everyone"`;
  `[]` leaves it with the admins. Only the permissions named change. Firm admins only. The read
  lists who holds each and `You can:` says what the caller can do. Removing a group drops its
  grants and the result says who holds each now. Once the firm has a Partners group (and more
  than about five people), offer once: "Let Partners approve skills and insights as policy, and
  be the deciders of record?"; never change a grant nobody asked for.
- `settings` changes named limits, only those given: `learning_min_cases` (supporting cases an
  insight needs, default 5; holders of `approve_policy`). How many learning runs the firm may run
  a month is its plan's (`plan_usage`); Alludium sets what a run may spend, never in dollars to
  the firm.
- `process` is the deal process. `{"template": "seed_to_series_a"}` alone sets up a template's
  stages (`seed_to_series_a`, the default; `multi_stage`; `growth`; `blank`). `{"stages": [...]}`
  replaces the stages, in order. Each stage has a `name`, a `kind` Alludium Brain understands
  (`sourcing`, `screening`, `evaluation`, `due_diligence`, `decision`, `negotiation`, `closing`,
  `portfolio`), a `description`, an optional `checklist` (plain items a person ticks) and the
  `documents` it expects. A stored stage has a `key`: keep it when renaming the stage, so the
  history of companies at it follows. The kind sets each company's status (screening:
  prospect; evaluation to closing: in_deal; portfolio: portfolio) and what its page leads
  with. The ways out (Passed, Lost, On hold) are always there; never add them as stages.
  Do not pass the older `stages` (a list of names) when you can pass `process`.
- `connectors` (`{"on_delete": "remove"}` or `"keep"`) says what happens to a file deleted from a
  connected drive: `remove`, the default, hides it at once and deletes it with what only it
  supports once it is gone for good; `keep` keeps it, marked as removed from the drive. Change it
  only when a partner asks, and say which they chose.
- `packs` is the kinds of work the brain records for the firm, primary first, set by Alludium
  when it created the organisation. `configure` shows them and cannot change them: if someone
  says the brain has them wrong, or wants another pack, tell them to ask Alludium. Custom fields,
  funds and tag vocabularies may name only the firm's entity types; `configure` refuses others
  and says which types the firm has.
- `plan_usage` is the firm's plan, set by Alludium, and this month's use of its allowance in
  units: meetings, emails and notes filed; document pages read; learning runs. Everything else is
  unlimited. When someone asks about the plan, limits or usage, answer from it in those units,
  never in dollars, and point to Settings → Plan and usage in the viewer. `configure` cannot change
  the plan: to change it, ask Alludium.
- `memo_headings` is the firm's IC memo outline, in order: each item a `heading` and an optional
  one-line `guidance` on what goes under it (a plain string is a heading with no guidance).
  The `ic-prep` skill drafts under these; `[]` goes back to its default headings.
  `house_style` is a short note on how the firm writes memos (spelling, units, length, tone);
  `""` clears it. Both are a list and a note, not a template: no formatting, fields or logic.
- `extraction_guidance` is a short paragraph (600 characters at most), in the firm's words, on
  what matters to it in documents ("net revenue retention by cohort; customer concentration").
  The brain reads it when it structures uploaded documents, to look harder for those things. It
  never replaces fields: a figure the firm wants tracked is a custom field. `""` clears it.
- `templates` and `routines` are the rest of how the firm works (its other document formats and
  recurring processes); the `playbook` skill captures them. `templates` with key `ic_memo` is the
  same as `memo_headings` and `house_style`: set one or the other.
- `me` is a member's private profile, not firm configuration: never pass it here. A member's own
  preferences ("I like short briefs") go to the `profile` skill; the team entry (role, focus
  areas) stays here and shows in their profile.
- `tag_vocabularies` and `dismiss_tags`: see "Tag vocabularies" below.
- `lists` creates or edits lists, matched by key or name: the sets the firm or a member works
  through that are not the deal process, such as an LP raise, co-investors, a sourcing theme,
  talent or a personal watchlist. Each has a `name`, what it holds (`item_type`:
  `organization`, `person`, `deal` or `fund`; required to create one), `scope` (`private`, the
  default; `people` with `people`, firm members by name or email; `group` with `group`, a group
  the user is in; or `firm`), optional `stages` in order (`[{"name": "Target"}, …]`; keep a stage's
  `key` when renaming it) and `fields` (`label`, `kind` `text`, `number`, `date`, `choice` with
  `choices`, `member` or `url`; `total: true` on a number adds up the list). `stages` and
  `fields` replace the list's. `archived: true` archives a list. A list's stages and values are
  the list's, never the company's. Entities go on a list through `capture` (the `note` skill).
  To change who sees a list, call `share` with `list` and the same `scope`, `people` or `group`
  as for a source: only its creator or a firm admin may. A restricted list hides itself, its
  entries and values, never the companies on it. `portfolio` is built in: never create a list
  with that name. Lists are rows, not part of the configuration: each member sees
  only the lists shown to them.
- A list with `type: "fundraise"` (a venture firm's) is a raise for one of the firm's funds:
  `fund` is required, `item_type` is `organization` or `person`, and it comes with the stages
  Target, Contacted, First meeting, Diligence, Soft-circled, Committed, Passed and Lost to another
  fund, and a `commitment` field. It is usually restricted to a group (`scope: "group"`).
  Reaching Committed records the LP in the fund and its commitment, in the list's scope.
- A list with `type: "pipeline"` is another deal pipeline beside the firm's process, for a
  firm that runs one per fund or strategy ("Fund II has its own pipeline"). Ask whether the firm
  runs one pipeline or several before making any. It takes `template` (as `process` does) or
  `stages` in the process's shape (`name`, `kind`, `description`, `checklist`, `documents`), and
  optionally `fund`. Decisions move companies on it (`log_decision` with `list`); capture only
  records a CRM record's stage there. The firm's own pipeline is the list keyed `pipeline`:
  its stages are `process` (change them there, never through `lists`), and through `lists` with
  `key: "pipeline"` and `type: "pipeline"` it can be renamed or given a `fund`; a firm admin can
  restrict it with `share`.
- A list with `type: "leads"` (a venture firm's origination list: a sourcing theme or a
  watchlist) holds companies or people (`item_type`) the firm could pursue. Its stages are
  fixed: New and Shortlisted, which a person sets through `capture`, then Contacted and Met,
  which filed email and meetings give; do not pass `stages`. It has `owner`, `revisit_on` and
  `added_via` built in, plus any `fields` the firm adds. Decisions take entries out (hold,
  pass, advance into a pipeline), and the entries stay, marked. A person's sourcing list is
  private; a team's is `firm`.
- `email_scope` and `meeting_scope` are the firm's defaults for email and meetings filed without
  a scope. Each always reaches the firm members on it (an email's sender and recipients, a
  meeting's invitees). `people_on_it` goes no further (the meeting default); `lists` (the email
  default) also shares it with whoever can see the lists its companies and people are on: the firm
  for a firm-wide list or pipeline, the group for a restricted one, and only that group when any of
  its lists is restricted; lists only one person or specific people can see never count. `firm`
  shares all of it. Old names are still read: `recipients`, `private` and `attendees` are
  `people_on_it`, `pipeline` is `lists`. Anything Alludium Brain finds sensitive stays with the
  people on it under any rule. Each person may set their own for what they file with `my_scope`
  (`{"email": …, "meetings": …}`, `firm_default` to follow the firm's again), in the nightly setup
  or in Settings → Connections and sharing. `my_scope` is not gated: anyone sets their own, the
  firm sees it, and it never changes anyone else's. Change the firm's only when a partner asks.
- `mail_rules` changes which mail the nightly run files. Every read lists the firm's rule under
  **Mail the nightly run files**: its packs' kinds of mail to keep and to skip, each with a key
  and a line. `{"add": [{"key": "board_packs", "description": "board packs from portfolio
  companies", "keep": true}], "off": ["recruiting"]}` adds a kind and switches a default off; it
  replaces the firm's changes, and `{}` goes back to the defaults. Personal mail is never filed
  and sensitive mail stays private whatever the rules. Firm admins only, once the firm has one.
  Change it only when a partner asks.
- `origination` is how inbound pitches are handled: `inbound_sharing` (`ask`, the default:
  the member a pitch reached is asked to share it; `pipeline`; `private`), the nightly caps
  `classify_usd_per_night` and `inbound_fit_check_usd_per_night` (USD, 1 each by default) and
  `route_by` (`recipient`, the default, `focus_areas` or `responsibilities`). Only the fields
  given change; every read shows all four. Sharing and the caps are firm admins only, once the
  firm has one. Nothing acts on `pipeline` sharing or on routing yet: say so if asked. Change it
  only when a partner asks.
- Origination's Searches and theses (nightly source feeds, research hunts, curated verticals, thesis
  generation) are set up with the firm skill `set-up-search` (`configure(skill="set-up-search")`),
  not here: load it when a partner asks for one.
- The configuration applies to the whole firm, so everyone at the firm sees it.

## Rules

- **Start from the report.** The first call is always `configure` with `onboarding: true`. It
  gives the `phase`, what the brain knows and the `gaps`, each with a question. Ask only about
  gaps, and never re-ask anything the report shows.
- **Cite or ask.** Every item you propose shows where it came from: a public URL or connector
  record with a short quote, "you told me", or "from your documents". Nothing the model
  inferred is presented as known; a guess is a question ("Do you also invest in climate?").
- **Public and connected only.** Research reads open public pages without signing in, and the
  data connectors the user already has. Firm public research does not authorize reading private mail, CRM records, files or notes. The optional personal sent-mail review below requires its own bounded permission. Say "from public sources" only for public evidence.
- **Person first; verify the firm before firm research.** Start with the personal introduction below. Before researching the firm, confirm its name, website domain and city; names collide.
- **The partner's words win.** A correction replaces the page, and that item then needs no cite.
  Do not add sectors, numbers or criteria nobody stated; mark a criterion `must` or `nice` only
  when the partner says so.
- **Never invent an email, role or focus area.** Emails come from the partner, or from the
  CRM's user list or the calendar once those are connected and the partner agrees, each
  confirmed. Never from a pattern.
- **Confirm before writing.** Store a page and save a section only after the partner's yes on
  it. Save each section as it is confirmed, so an interrupted onboarding picks up where it
  stopped.
- **Connections are visible to the firm.** Before recording someone's connections, say once:
  "Everyone at the firm can see which systems each person has connected (not what's in them)."
- **Short.** One section at a time, a few lines each. No walls of text.

## 1. Read the report

Call `configure` with `onboarding: true`, then `configure(me={})` separately. Complete the personal introduction below in **every phase**, before routing the remaining firm work by `phase`:

| Phase | Flow |
|---|---|
| `new` | Personal introduction first, then the firm setup (section 2). Suggest a partner answers firm questions; anyone may |
| `setup_incomplete` | Say what is missing in one line, from the report's **Setup** and gaps ("The thesis and team are set; there's no deal process yet") and ask: "Finish the firm's setup now, or just set yourself up?" Then section 2 for the gaps only, or section 3 |
| `in_use` | The personal setup (section 3). Change firm configuration only if they ask (`references/interview.md`, "Already configured") |

While setup is unfinished, the report's **Setup** block names the firm's packs and lists their
sections in order: each section's key, what it fills (a `configure` section, or organisations
with one of some statuses), whether it is done, its question and where to look for it. The packs
were set by Alludium when it created the organisation: never ask what kind of firm it is or offer
to change them. If they look wrong, say so once and suggest a firm admin asks Alludium
(hello@alludium.ai).

A request to change one thing ("add Priya, her email is priya@northwind.vc", "change our deal
stages") skips onboarding: read `configure` and follow `references/interview.md`.

## Personal introduction — every member

Read the profile and report before asking. Brain starts shared public-person research at verified
sign-in and when teammates are added. If `you.person_id` is present, read `entity_brief` for that
person before the opening; use `you.public_research` to distinguish queued, found, empty or
unavailable work. Start with a short, cited understanding of their professional background and
one useful suggestion, then invite corrections: “Your public bio says you lead portfolio support.
I could help turn board updates into a weekly brief. Would that be useful?” Treat the suggested
need as a hypothesis, not a fact. If research is still queued, say so briefly and use existing
knowledge; do not block the conversation or repeatedly enqueue it. If evidence is missing or
ambiguous, ask only the gap needed to help. Do not present the absence of evidence as a blank
questionnaire. Reuse confirmed role, responsibilities, focus, preferences
and approved style; do not treat a profile-item count as proof that you know their work. Summarise
what is known in one or two lines and let them correct it. Ask one natural question at a time,
usually two or three short turns, not a checklist. For example: “What takes most of your time,
and what would you most like help with?” If their role is missing, start there. Follow their answer
to learn responsibilities, work they enjoy and work they would like to automate. Skip what they
already covered, and let them skip the introduction or get straight to a task.

Explain once that useful personal context can be remembered privately. For role, responsibilities,
enjoyment and goals, offer a concise summary to remember and save it only when they agree, using
`me.add` with `kind: "about"` and their words in `said`. Directly stated ongoing preferences and
explicit remember requests use the profile skill's existing save rules without another approval.
Read first, edit corrections, avoid duplicates, and verify every save. Never copy private profile
answers into the firm's member roster. Changes to the public role/team entry need separate consent.

Inspect the tools actually available in this host and read `configure()` for Brain's connection
readiness. Host connector access and Brain background connections are separate: name the provider,
account where known, route and current status. Recorded host connections may be stale; tool presence
does not prove account access or scope. Use an available read-only account/status operation, without
reading message content. If account identity cannot be established, say so. Never turn a paused,
failing or unknown connection into automatic fallback ingestion. Reuse existing preferences/style;
no need to ask someone to teach their writing style again.

### Optional, bounded sent-mail review

Only offer this when a usable sent-mail route exists. A connection is not permission to read mail.
Offer a choice in plain language: “I can learn a little from up to 20 emails you sent in the last
30 days in [confirmed account], or we can just talk. The review stays in this conversation; I’ll
ask before saving inferred context. Would you like that?” They may narrow the scope or decline.
Do not fetch content until they choose. Use the named account's sent folder/author filter, at most
20 messages and 30 days (or their narrower choice); no inbox sweep, attachments, quoted replies,
forwarded text, extra accounts or automatic filing. If the available tool cannot enforce the
bounds or confirm authorship, explain that and continue the conversation. A direct Brain connection
alone does not expose its mailbox through the host: use only supported tools and authorized,
already-filed sources, or say this review is unavailable here.

Offer two or three tentative observations about work topics, correspondence and role context,
with message links/IDs and dates. Distinguish “this sample suggests” from “you told me”; do not infer
personality, sensitive traits or performance. Frequency is a bounded collaboration signal, not proof
of relationship strength; describe actual counts and shared work instead. Keep third-party
content out of personal memory. Ask the user to correct/confirm useful observations before saving
an `about` item in their own words. Unconfirmed observations remain in the conversation, never
active profile facts. Mail analysis permission is not permission to import or share those messages.

Writing-style learning is optional and separate: use the profile skill's existing sourced,
pending-style flow only if requested, then show it and obtain approval before `approve_style`.
Do not save an inferred style as an ordinary preference to bypass that approval.

### People, enrichment and invitations

A researched Person, a team roster entry, workspace access and an invitation email are different.
Use the report's `you.person_id` or a verified person match; never match on name alone. When a user
asks to look up themselves or a colleague, or accepts your offer, call the shared
`entity_brief(entity=<person id>, enrich=true)`. Do not create a second enrichment engine or turn
on providers to make onboarding work. Explain that shared public person facts may be visible to the
firm for an already firm-visible person; this is separate from their private profile and sent mail.
The response contains the existing brief and `enrichment.requested`, not finished new research.
Report refusals, unavailable sources and queued work honestly. Later read `entity_brief` without
`enrich` and `configure()`'s recent enrichment lookups to distinguish pending, failed, empty and
completed work; cite newly visible sources before claiming facts were learned. Do not repeatedly
request refreshes or promise photos or successful research before it completes.

For every member, offer up to two or three likely collaborators to invite when evidence supports
it; one good candidate is enough. Prefer discovery to another question. Use only the already
permitted sent-mail sample, authorized meeting/calendar or already-filed sources, and confirmed
team identities. Do not expand the account, time window or source access just to rank colleagues.
For mail, count distinct sampled messages to each verified colleague and, when available, distinct
threads; state the sample size and dates. Deduplicate messages/aliases only when identity is known;
exclude the user, automated senders, mailing lists and external people. Combine frequency with
specific shared work where supported, rather than treating a bulk-recipient count as closeness.
For meetings, recurring shared work can support a suggestion without reading private notes unless
authorized. Public enrichment can establish a teammate's role, not who the user works closest with.

Check the current roster and recorded invitation history with `configure()`, and sign-in state
in the onboarding report, before suggesting them. These are not proof of current identity-provider
membership: unknown access remains unknown; the invitation service checks actual membership and
deactivation when an authorized invite runs. A shared email suffix or frequent correspondence alone
is not proof of employment; personal domains, external advisers and ambiguous identities need
confirmation. Never invent addresses or recommend someone already participating as a new invite.
Do not resend merely because a person has not signed in, or reactivate a deactivated member.

Keep it light: “From the 20 sent messages you let me review, Priya appeared in 8 across 3 threads
about IC preparation. She looks like a useful first teammate to invite. Would you like me to invite
her?” Give one short sourced reason per candidate, tailored to the user's work; label uncertainty.
If no usable collaboration evidence exists, ask once who they work most closely with, then suggest
that person. Do not pretend public research establishes closeness. If they decline, move on.
Suggesting or saving a person is not an invitation: only an explicit yes naming the recipients
allows `invite_colleague`. Inviting queues ordinary public person research before their first
sign-in, including an existing roster person, subject to the same policy, caps and deduplication.
Reuse the invitation skill and report each outcome. Explain when relevant
that joining does not automatically import either person's emails: each person must connect and
authorize their sources, with the Brain's normal audience rules.

End the introduction with one useful next step tied to what they want help with, then continue
firm setup if needed. Adapt to the person, rather than inferring technical ability from a title.
For someone who wants a recurring way of working, offer to create or refine a Brain skill using
`playbook`; reuse existing firm skills first. Discuss sharing it only when useful, with an explicit
audience choice. For someone comfortable with scripts or working through large collections,
offer the CLI/import route and a small reviewed example. For someone who just wants help, do the
useful task in ordinary language. Do not turn skills, sharing or CLI adoption into onboarding gates,
and never create a schedule, change a shared skill or publish private context without authorization.
Private mail and meeting-note access can deepen understanding later, under explicit source/account,
content and audience choices; permission for the bounded sent-mail review does not cover meetings. A later fresh conversation reads the saved private profile/task guidance;
do not repeat the interview. Free-text context is guidance, not an enforced product setting.

## 2. The firm setup

### 2a. Which firm

From the user's email domain, the firm's name in the report and what they say, find the firm's
website and say in one line: "Is this your firm: Northwind Ventures, northwind.vc, London,
early-stage AI infrastructure?" Two candidates: show both and ask. Do nothing else until they
say yes. If the host has no web search, say so and use `references/interview.md`.

### 2b. Research

Follow `references/research.md`. Before proposing anything:

- open every page of the firm's own site that a Setup section's **Look for** points to, as well
  as its team page: search the site for them rather than stopping at the home page;
- look the firm up in **each** data connector you have (Harmonic, a Crunchbase-style
  connector, CRM enrichment), and the organisations its pages name too;
- then announcements, filings, press and public profile pages, to fill and cross-check.

Budget about 15 fetches. Collect each item with its exact quote, URL and date. Do not store
anything yet.

### 2c. Propose, one section at a time

Walk the report's Setup sections in their order, skipping those already done, each as a few
lines with links and short quotes, then the section's own question for what is not public. Then
the **Team** (names, titles, focus areas, then the gap: their emails) and **Tags** (a short theme
list from the pages above). By what a section fills:

- **`fit`**: the statement and each part the question names, item by item as the firm lists
  them, in its words: regions as listed ("UK, DACH, the Nordics"), not a summary ("Europe").
  Never from team members' focus areas or the organisations the firm works with (those are
  evidence, not the profile). Then ask for criteria that are not public, each a must or a nice
  only when the partner says so.
- **`process`**: rarely public. Offer the template `configure` lists first and ask what to
  rename; checklists can wait.
- **`status:…`**: the organisations themselves, as the pages list them: "Are these yours, and
  are any missing?" They are captured, not configured (2d).
- **Anything else** (such as `funds`): what the sources say, as "How `configure` works" above
  describes that section.

For anything that disagrees between sources (a partner on a 2023 press release but not on the
team page; two figures for one thing), show both with dates and ask. Offer documents once: "If
you have documents on how the firm works or what it does, drop them and I'll take the setup from
them" (the `drop` skill, then `references/interview.md` step 1a for the proposals).

### 2d. Store each confirmed section

1. `capture` each page or record the section rests on, as `references/research.md` says
   (firm-scoped, `system: "web"` or the connector, the passages word for word). A data
   connector's record you relied on or showed as a match ("matching Harmonic") is captured too,
   as `external_record` with `system` the connector and its record ID, and cited like a page. For a
   `status:…` section, its confirmed organisations go on their page's capture, each with one of
   the section's statuses as the page says (`status:portfolio|exited`: `"portfolio"` or
   `"exited"`).
2. `configure` with the section (described first, as above) and `cites`: one per item that came from a source, with the
   `source_id` the capture returned and the exact quote. Items the partner gave need no cite.
   A refused cite means the quote is not in the captured text: fix the quote, never drop the
   check.

Members: pass the whole team, as `references/configure.md` says.

### 2e. The firm's systems

Look at your own tools and match them (names after the host's prefix):

| Category | Connectors |
|---|---|
| `email` | Gmail, Outlook |
| `calendar` | Google Calendar, Outlook Calendar |
| `crm` | Affinity, Attio, HubSpot (others: record them; the import supports these three) |
| `drive` | Google Drive, SharePoint, OneDrive, Dropbox, Box |
| `meeting_notes` | Granola, Fireflies, Otter, Fathom, Zoom, Teams, Google Meet |
| `data` | Harmonic, Crunchbase, PitchBook, Dealroom |
| `other` | Slack, Notion |

Ask once, with what you have ticked: "Which does the firm use? Email: Google · Calendar: Google
· CRM: Affinity · Drive: Google Drive · Meeting notes: Granola, Zoom. Right?" Save it as
`systems`. The firm's CRM is then its record for its own side of each deal; for an
organisation's own figures it stays an estimate. Then say the visibility line (Rules) and save the user's own `connections`.

Then one question on how the firm works: "Does the firm already have its own Claude skills,
templates for its documents, or a document on how it runs its process?" Skills: the `playbook`
skill imports them. Templates and process documents: drop them, or let the `playbook` skill read
past examples and propose the templates; otherwise note it as a next step.

### 2f. Next steps

End with an ordered list built from the report's `gaps` (call it again), each with what it
buys and the words to say:

1. **CRM import**: "Import our Affinity pipeline" (the `import-from-crm` skill; it dry-runs
   first): "your pipeline and its history, so briefs know every company you've seen". If the
   CRM is not connected here, say how to connect it; where you have a tool that suggests
   connectors, use it.
2. **Ongoing filing**: first offer direct Brain connections for supported mail, calendar and
   meeting-notes accounts where enabled. For what remains, offer "Set up the nightly Alludium
   Brain filing task" (the `whats-new` skill). Check the host's scheduler and explain when it runs;
   use manual filing when scheduling is unavailable. Never duplicate sources already synced.
3. **Drives**: "Ask Alludium to connect your Google Drive" (hello@alludium.ai).
4. **Email-in**: the firm's address from `configure`, if it has one.
5. **How the firm works**, if not done: "Teach Alludium Brain how we run <a recurring process the
   firm named>" or "Make our <document> a skill" (the `playbook` skill): "so everyone's assistant
   drafts in the firm's format".
6. **The team**: list who has not connected yet (the report's `team`) and offer to invite
   colleagues. When the user asks, use `invite_colleague` with each confirmed work email and
   name; never guess addresses or send automatically from research. Any member can invite.
   It grants ordinary member access and sends an email with app sign-in and AI setup links.
   Report each result honestly: access may exist even when email sending failed. Existing
   roles are preserved, and deactivated people need a firm admin to restore them.
7. **Existing collections**, if the firm has a vault, Notion pages or another source to script:
   offer the Brain CLI guide and access to the private import starter. Begin with a reviewed
   selection; do not import a whole account or assume source permissions become Brain sharing.

Reply with what was saved (the sections, in plain words; no source ID or link: the user does not
need one for a configuration save) and the list. Then offer one thing to try: "Ask me what we
know about <an organisation the firm works with>."

## 3. The personal setup

Continue after the personal introduction (already done in every phase). Skip everything already known or completed:

1. **Who you are.** "You're on the team as Priya Raman, Principal, focus: security (set by
   Clara on 1 Nov)." Ask what to change. Not on the team (`not_on_team`): offer to add them
   with their name, role and focus (email from their sign-in, confirmed); pass the whole team.
2. **How you like to work**: reuse the personal introduction and saved private profile. Ask only a useful remaining question; never restart the interview.
3. **Your connections.** Match your tools as in 2e, say the visibility line, save
   `connections`. Then name what the firm uses that they have not connected
   (`your_missing_connections`) and what it buys.
4. **Your ongoing filing**: offer supported direct connections first, then a nightly task
   (`your_nightly`, the `whats-new` skill) for remaining sources if their host can schedule it,
   with their own email scope choice.
5. **The tour.** Call `whats_changed` with `mine: true` and `since` 30 days ago, and show:
   - the firm in three lines, from the report's **The firm**;
   - the firm's own skills, if it has any (the "Firm skills" in `configure`), one line each;
   - the pipeline by stage with counts and the latest names (`data.pipeline`);
   - **your deals** (`you.deals`): company, status, last met;
   - your next meetings (`upcoming`), with an offer to prep the first (`prepare-meeting`);
   - what changed in the last week, five lines at most.
   Every line keeps its IDs, so they can ask for a brief on any of it.
6. **One thing to try**: "Ask me what we know about <one of your deals>."

## Re-runs

Onboarding is safe to run again: the report shows what is done. A firm that changed its
website: offer to research again and show only what differs from the configuration, each with
its source; captured pages are stored as new versions.

## What the brain has learned

`configure` also lists `lessons`: what the brain has learned about the firm, with `counts` by
status. Taught lessons come from members' notes ("FC is Ferncastle", a link fix) and are active
at once; **proposed** ones come from the brain's own observers and wait for a person. Each has an
`id`, a `statement`, its `evidence` (source IDs), who taught it or which observer proposed it, and
how often it has applied.

- **Proposals.** When `lessons.proposed` is not empty, show each statement with its evidence count
  and ask the partner. On a yes, `configure` with `lessons: [{"id": "les_…", "decision":
  "accept"}]`; on a no, `"reject"` (it is never proposed again). A proposed field ("Track 'pilot
  sites' on organizations as a field") becomes a custom field, and the facts stated under that
  name are filed under it. Never accept or reject without asking.
- **Asking it to look.** "What should we be tracking?" or "suggest fields": call `configure` with
  `learn: ["fields"]`; it proposes, never applies. It also runs on its own once a day.
- **Undoing one.** "Stop reading 'Yusuf' as Yusuf Adeyemi": find the lesson in `lessons.active`
  and pass `"retire"`, with the partner's reason as `note`; what it did is taken back. `"restore"`
  brings back a retired or disputed one.

## Learning runs: what the firm's decisions teach

Once the firm has a history of decisions (an imported CRM, or months of use), a partner can ask the
brain what those decisions, taken together, teach: "why do we pass on consumer subscription
companies?", "what has changed since the new fund?". This is a **learning run**.

1. The firm needs a `decision_reason` tag vocabulary: the kinds of reason it records (for a venture
   firm: retention, acquisition economics, team, market size, valuation, stage or cheque fit,
   competition, traction, product risk), each with a description and synonyms in the firm's words.
   Set it up with `tag_vocabularies` like any other vocabulary, from the partner's words.
2. Define and start a run with `configure`: `learning_runs: [{"name": "Consumer passes",
   "kind": "decision_reasons", "outcome": "pass", "cohort": {"tags": ["sector:Consumer"]},
   "run": true}]`. A cohort can also take `decided_from` and `decided_to` (for example since a
   mandate change). `scope: "private"` reads only what the partner can see and keeps the results theirs,
   `scope: "group"` with `group` reads as that group sees and keeps them the group's; the default
   reads what the whole firm can see. Runs cost a little (a few cents; the firm's
   per-run budget) and take a minute or two; `configure` shows each run's status. If the partner
   wants it kept current, add `"after_decisions": 10` (or their number): the run then starts on its
   own once that many new decisions in its cohort have come in (looked at daily). Or, or as well,
   `"every": "month"` (`week`, `month` or `quarter`) runs it on a schedule. `{"id": "lrn_…",
   "after_decisions": 0}` or `"every": "off"` turns either off.
3. Read what it found with `search` and `view: "insights"`. Show each insight's statement, its cases
   with their quoted reasons, the cases that went the other way, its questions and its limits.
   Say plainly that an insight describes past decisions: it is not a rule and it never rejects a
   company.
4. Ask the partner, for each insight, whether it fairly describes the firm's past decisions. On a
   yes, `configure` with `insights: [{"id": "ins_…", "decision": "observe"}]`; on a no, `"reject"`
   with their reason as `note`. Never decide for them. A run that finds nothing says so: "not enough
   evidence" is an answer. An insight goes **stale** at its review-by date (a year on), when the
   thesis changes, or when a newer run no longer finds it: it leaves prep and briefs. `view:
   "insights"` lists stale ones; ask whether each still holds, then `"observe"` brings it back (due
   for review in a year), or `"reject"` or `"retire"` it.
5. `kind: "fit_vs_decisions"` asks where the firm's thesis and what it actually did differ: parts of
   the thesis that companies it advanced did not meet, and reasons that recur in passes of companies
   that fit the thesis but that the thesis does not mention. It checks each company against the
   thesis as the brain sees it today, so say that the comparison is with today's thesis.
6. **Adopting an insight as policy** makes it the firm's rule. Only holders of `approve_policy` (the
   firm's admins, or the groups `permissions` names) can, and only when the partner asks. Agree the
   exact line first, in their words, and where it goes: a thesis criterion (`adopt_as:
   "criterion"`, `text`, `weight` `nice` unless they say `must`) or an item on one stage's checklist
   (`adopt_as: "checklist"`, `stage`, `text`; it defaults to the insight's first question). Read the
   line back and wait for a yes, then call `configure` with only `insights: [{"id": "ins_…",
   "decision": "policy", …, "note": "why"}]`. The line is written into the configuration and
   recorded with the insight it came from. A policy still never rejects a company: a criterion shows
   in the fit check as met, not met or unknown. Retiring a policy (`"retire"`) leaves the line in
   the configuration until someone changes it; say so.
