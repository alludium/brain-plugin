---
name: onboard
description: Onboard a firm or a person to Alludium Brain, research first. For the first person at a firm, researches the firm's public footprint (website, team, thesis, funds, portfolio, filings, press) and the user's connected data tools, proposes the configuration with every item cited, and asks only to confirm, correct and fill gaps; then records the systems the firm uses and sets up the CRM import, nightly run and team. For later users, a short personal setup (profile, connections, nightly run) and a tour of what the brain already knows. Also changes the firm's configuration - thesis and criteria, deal process (stages, checklists, documents), funds, custom fields, tag vocabularies, team members and focus areas, IC memo headings and house style - by interview or from the firm's own documents (IC charter, strategy, LPA, PPM, LP deck). Use when someone says "onboard us", "onboard me", "set up Alludium Brain for our firm", "I'm new to Alludium Brain", "here are our fund documents", "update our thesis", "add Priya to the team", "Tomas now covers security", "change our deal stages", "add a checklist to due diligence", "add a sector tag for climate", "review suggested tags" or "use our memo template". Not for notes about companies (use note), deal decisions (use log-decision) or one person's own preferences, such as how they like their briefs (use profile).
---

# Onboard

Ask the brain first, then public sources, then the person. Never ask what either already knows.
Everything goes through the Alludium Brain connector's `configure` and `capture` tools. How
`configure` works (each section, `systems`, `connections`, `cites`, tags) is in
`references/configure.md`; read it before the first write.

Interview a partner about how the firm invests and who is on the team, confirm what you heard,
then save it with the Alludium Brain connector's `configure` tool. It is safe to run again: it always
starts from the stored configuration and proposes changes to it.

## How `configure` works

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
- `funds` is the firm's funds (name, vintage, size, currency, strategy); it replaces the list,
  and each fund becomes a Fund in the brain.
- Each section you pass (`fit`, `process`, `funds`, `custom_fields`, `members`,
  `memo_headings`, `house_style`, `templates`, `routines`) **replaces** the stored one. To add one criterion or one
  person, pass the whole thesis or the whole team. Never pass a section that is not changing.
- The thesis is the `fit` section (the firm's fit profile, which VC Brain shows as its thesis;
  `thesis` is its older name and still works, and reads return both). It is an object:
  `statement` (one sentence), `stages` (the funding stages the firm invests
  at, such as Seed and Series A, not its deal stages), `in_scope` and `out_of_scope` (sectors and
  themes), `regions`, `cheque` (`{"min": 500000, "max": 3000000, "currency": "EUR"}`) and
  `criteria` (each `{"text": "...", "weight": "must" | "nice"}`, or without a weight). Leave out
  what the partner did not give. Put criteria inside `fit`; the separate `criteria` argument
  is only for older plugins. Alludium Brain checks companies against each part (`entity_brief` with
  `fit_check`), so keep each part short and specific.
- `members` is the whole team: name, email, role, `focus_areas`, `responsibilities` (what each
  person owns at the firm, in the partner's words: "IC prep", "LP reporting") and
  `approves_skills` (who may approve the firm's own skills; see the `playbook` skill). Focus and
  responsibilities show on each person's page. `configure` refuses a list that leaves out a current member
  and names who would be dropped. To drop someone, name them (name or email) in `remove`, only
  after the partner has said to. `remove` on its own drops those people and keeps the rest of
  the team as stored. A dropped member loses the firm-member role; the person stays.
- **Firm admins.** Removing members, `approves_skills`, `email_scope` and `connectors` change who
  sees or approves what, so once the firm has a firm admin (the admin or owner role in its WorkOS
  organization), only admins can change them; `configure` names the admins and says whether the
  caller is one. If a non-admin asks, say who can do it rather than trying. While the firm has
  none, anyone can, and onboarding asks to have one made. Everything else stays open to every
  member.
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
- `memo_headings` is the firm's IC memo outline, in order: each item a `heading` and an optional
  one-line `guidance` on what goes under it (a plain string is a heading with no guidance).
  The `ic-prep` skill drafts under these; `[]` goes back to its default headings.
  `house_style` is a short note on how the firm writes memos (spelling, units, length, tone);
  `""` clears it. Both are a list and a note, not a template: no formatting, fields or logic.
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
  default, or `firm`), optional `stages` in order (`[{"name": "Target"}, …]`; keep a stage's
  `key` when renaming it) and `fields` (`label`, `kind` `text`, `number`, `date`, `choice` with
  `choices`, `member` or `url`; `total: true` on a number adds up the list). `stages` and
  `fields` replace the list's. `archived: true` archives a list. A list's stages and values are
  the list's, never the company's. Entities go on a list through `capture` (the `note` skill).
  To share a private list with the firm, call `share` with `list`. `portfolio` and `pipeline`
  are built in: never create lists with those names. Lists are rows, not part of the
  configuration: each member sees only the firm's lists and their own.
- `email_scope` is who sees email, and meetings the nightly task files, without a scope:
  `pipeline`, the default, shares it with the firm when it involves a company or person in the
  pipeline or portfolio and keeps the rest private; `firm` shares all of it; `private` keeps it
  to whoever filed it. Anything Alludium Brain finds sensitive stays private under any rule, and each
  person can choose their own rule when they set up the nightly task. Change it only when a
  partner asks.
- The configuration applies to the whole firm, so everyone at the firm sees it.

## Rules

- **Start from the report.** The first call is always `configure` with `onboarding: true`. It
  gives the `phase`, what the brain knows and the `gaps`, each with a question. Ask only about
  gaps, and never re-ask anything the report shows.
- **Cite or ask.** Every item you propose shows where it came from: a public URL or connector
  record with a short quote, "you told me", or "from your documents". Nothing the model
  inferred is presented as known; a guess is a question ("Do you also invest in climate?").
- **Public and connected only.** Research reads open public pages without signing in, and the
  data connectors the user already has. Never the user's email, CRM records, files or notes for
  research. Say "from public sources" when you propose.
- **The firm first.** Confirm which firm it is (name, website domain, city) before researching
  it; names collide.
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

Call `configure` with `onboarding: true`, then go by `phase`:

| Phase | Flow |
|---|---|
| `new` | The firm setup (section 2). Suggest a partner does it; anyone may |
| `setup_incomplete` | Say what is missing in one line ("The thesis and team are set; there's no deal process and nothing about funds") and ask: "Finish the firm's setup now, or just set yourself up?" Then section 2 for the gaps only, or section 3 |
| `in_use` | The personal setup (section 3). Change firm configuration only if they ask (`references/interview.md`, "Already configured") |

A request to change one thing ("add Priya, her email is priya@northwind.vc", "change our deal
stages") skips onboarding: read `configure` and follow `references/interview.md`.

## 2. The firm setup

### 2a. Which firm

From the user's email domain, the firm's name in the report and what they say, find the firm's
website and say in one line: "Is this your firm: Northwind Ventures, northwind.vc, London,
early-stage AI infrastructure?" Two candidates: show both and ask. Do nothing else until they
say yes. If the host has no web search, say so and use `references/interview.md`.

### 2b. Research

Follow `references/research.md`. Before proposing anything:

- open every page of the firm's own site that states its focus, thesis, or what it looks for
  in founders (stages, cheque, regions), as well as the team and portfolio pages: search the
  site for them rather than stopping at the home page;
- look the firm up in **each** data connector you have (Harmonic, a Crunchbase-style
  connector, CRM enrichment), and its portfolio companies too;
- then announcements, filings, press and public profile pages, to fill and cross-check.

Budget about 15 fetches. Collect each item with its exact quote, URL and date. Do not store
anything yet.

### 2c. Propose, one section at a time

In this order, each as a few lines with links and short quotes, then one question:

1. **Thesis**: statement, stages, in and out of scope, regions, cheque. Take the scope from
   what the firm says it invests in and does not, item by item as it lists them; never from
   team members' focus areas or the portfolio's sectors (those are evidence, not the thesis).
   Regions as the firm lists them ("UK, DACH, the Nordics"), not a summary ("Europe"). Then ask
   for criteria that are not public ("a minimum ARR at Series A? the buyer you look for?").
2. **Funds**: name, vintage, size, currency.
3. **Team**: names, titles, focus areas. Then the gap: their emails.
4. **Portfolio**: the companies, current and exited. "Are these yours, and are any missing?"
5. **Tags**: a sector and theme list from the portfolio and focus pages, short.
6. **Deal process**: rarely public. Offer the Seed to Series A template (`configure` lists the
   templates) and ask what to rename; checklists can wait.

For anything that disagrees between sources (a partner on a 2023 press release but not on the
team page; two cheque ranges), show both with dates and ask. Offer documents once: "If you have
an IC charter or LP deck, drop it and I'll take the process and funds from it" (the `drop` skill,
then `references/interview.md` step 1a for the proposals).

### 2d. Store each confirmed section

1. `capture` each page or record the section rests on, as `references/research.md` says
   (firm-scoped, `system: "web"` or the connector, the passages word for word). A data
   connector's record you relied on or showed as a match ("matching Harmonic") is captured too,
   as `external_record` with `system` the connector and its record ID, and cited like a page. For the
   portfolio, its confirmed companies go on the portfolio page's capture with `status:
   "portfolio"` or `"exited"`.
2. `configure` with the section and `cites`: one per item that came from a source, with the
   `source_id` the capture returned and the exact quote. Items the partner gave need no cite.
   A refused cite means the quote is not in the captured text: fix the quote, never drop the
   check.

Members: pass the whole team, as `references/configure.md` says. Funds become Fund entities.

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
`systems`. Then say the visibility line (Rules) and save the user's own `connections`.

Then one question on how the firm works: "Does the firm already have its own Claude skills,
templates for memos or LP letters, or a document on how IC works?" Skills: the `playbook` skill
imports them. Templates and process documents: drop them, or let the `playbook` skill read past
examples and propose the templates; otherwise note "how we run IC" as a next step.

### 2f. Next steps

End with an ordered list built from the report's `gaps` (call it again), each with what it
buys and the words to say:

1. **CRM import**: "Import our Affinity pipeline" (the `import-from-crm` skill; it dry-runs
   first): "your pipeline and its history, so briefs know every company you've seen". If the
   CRM is not connected here, say how to connect it; where you have a tool that suggests
   connectors, use it.
2. **Nightly run**: "Set up the nightly Alludium Brain filing task" (the `whats-new` skill): "your
   meetings and deal email filed every night, so colleagues see who met whom". Claude and Cowork
   only today.
3. **Drives**: "Ask Alludium to connect your Google Drive" (hello@alludium.ai).
4. **Email-in**: the firm's address from `configure`, if it has one.
5. **How the firm works**, if not done: "Teach Alludium Brain how we run IC" or "Make our LP update a
   skill" (the `playbook` skill): "so everyone's assistant drafts in the firm's format".
6. **The team**: a short message the partner can send colleagues: in Claude, install the Alludium Brain
   plugin (Customize → Plugins → Add → Add marketplace → `alludium/brain-plugin`, unless the
   firm already installed it for everyone), connect its connector on the plugin's Connectors tab
   and sign in with their work email, then say "onboard me to Alludium Brain"; other assistants use
   the setup prompt on Alludium Brain's Connect page. On a Team or Enterprise plan, a Claude Owner adds
   the connector for the firm first (Organization settings → Connectors). List who has not
   connected yet (the report's `team`). Alludium Brain sends no invitations itself.

Reply with what was saved (sections and the `src_…` of the last configuration save) and the
list. Then offer one thing to try: "Ask me what we know about <a portfolio company>."

## 3. The personal setup

Ten minutes. In order, skipping what the report already has:

1. **Who you are.** "You're on the team as Priya Raman, Principal, focus: security (set by
   Clara on 1 Nov)." Ask what to change. Not on the team (`not_on_team`): offer to add them
   with their name, role and focus (email from their sign-in, confirmed); pass the whole team.
2. **How you like to work** (two questions at most): how they like briefs and digests, and any
   standing instruction. Save with the `profile` skill's rules (private to them).
3. **Your connections.** Match your tools as in 2e, say the visibility line, save
   `connections`. Then name what the firm uses that they have not connected
   (`your_missing_connections`) and what it buys.
4. **Your nightly run** (`your_nightly`): offer to set it up now (the `whats-new` skill), with
   their own email scope choice.
5. **The tour.** Call `whats_changed` with `mine: true` and `since` 30 days ago, and show:
   - the firm in three lines: thesis, deal process, team, funds (from the report);
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
