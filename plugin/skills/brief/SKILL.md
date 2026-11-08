---
name: brief
description: Answer "what do we know about X?" and "who has met them?" from the firm's Alludium Brain, with every claim cited to its source. Use for any question about a company, founder, investor, LP, fund, customer or deal the firm may have touched, for example "what do we know about Acme", "who's met Maya Lindqvist", "have we talked to Kestrel", "what's our history with Copperbeck". Offers, never silently, to file new information the user adds.
---

# Brief: what the firm knows

Answer from Alludium Brain only, through the connector's `search` and `entity_brief` tools. Your own
knowledge of a company is not the firm's memory; leave it out unless the user asks for it, and
then label it as not from the brain.

For a company brief, the required `entity_brief` arguments include `fit_check: true` and
`insights: true`, even when the user wants only a short summary. Gather those checks before
deciding what fits in the answer; the tool's meeting/screening examples do not limit this workflow.

For the firm’s own funds, use `search(view="funds")`. Ordinary `search(type="fund")` also
finds funds mentioned in sources that other firms manage; a mention is not ownership.
For a directory rather than a company brief, use `search(view="list", type="organization")` or
`view="people"`. `query` filters names, aliases and identity domains; `status`, `tags`, `kind`
(people) and `relationship` narrow it. `sort`, `direction` and `group_by` apply to the complete
visible result before `limit`/`offset`; use returned totals, never count only the current page.
A tag can classify a person or company only where its cited evidence is visible.

## Rules

- **Cite everything.** Each fact, quote and claim ends with a link to the source it came from,
  with its title, from the result's "Source links", for example
  [Partner meeting, 21 Oct 2026](https://…/sources/…). Never show a bare `src_…` ID. If the brain
  has nothing on a point, say so; do not fill gaps.
- **Never merge lookalikes.** Different entities with similar names (for example `Acme AI Ltd`
  and `Acme Robotics GmbH`) are different companies. Keep their facts and people apart.
- **Notes in their authors' words.** Quote notes as written, with the author.
- **Private material.** The tools return only what this user may see. Mark anything with scope
  `private` as "(private to you)" and remind the user not to forward it.
- Do not paste whole sources or the full `entity_brief` page back to the user.
- **Offer to file what the user adds, once.** If the user adds something the brain lacks (a
  view, a figure, news from a call), offer once in one line ("Note this in Alludium Brain, private to
  you?") and file it with `note` only after a yes. Never offer to file what the brief returned.
- **Offer to fix what the user says is wrong, once.** If the user says the brief is wrong about
  who met whom, which company a source is about, or what a name means ("I met Yusuf last week,
  it's in my notes", "that email isn't about Acme", "FC is Ferncastle"), offer once to fix it and
  teach the brain, and do it with the `note` skill's "Teaching the brain" after a yes, naming the
  source by its id from this brief. A wrong figure is a correction note with the figure as a fact.
- **Outside sources, offered once.** When the brief has the line "Outside sources: on for the
  firm" and the company or person has no description, was never looked up, or was last looked up
  more than six months ago, offer once in one line: "Look up <name> in outside sources (its
  website, the search providers the firm has on, such as Exa search, or the firm's data
  provider)? Only its name and domain are sent." On a yes, call `entity_brief` with
  `enrich: true` for that one entity, answer from what the brain has now, and say the outside
  sources arrive on its page within a minute or two. Never without a yes, never for a list, and
  never when the line is absent (the firm has it off). Its result says what was asked and, when
  nothing was, why: pass that on in one line, naming each provider as the result does ("Perplexity
  search", "Exa search"). If you search the web yourself, send only the name
  and domain, never the firm's notes, stages or thesis.
- **Backfill only when asked.** When a company's brief says `coverage` "crm_only", offer
  to fill it in (below) and wait for a yes. Never backfill without one, and never for a list.

## Steps

0. **Current guidance for this task.** Call `configure` with `me: {"task": {"topic": "briefs"}}`
   at the start of every new task, even in the same conversation; do not reuse an earlier profile.
   If an older server rejects `task`, read `me: {}` instead. Some older servers return the whole
   profile: apply only active relevant items, never pending styles or another task's preferences.
   Follow the user's `briefs` preferences, their `never` and `general` items
   and any remembered instruction for this kind of task; preferences filed under another topic are
   for other tasks. They set length, order, emphasis and voice, and win over the default shape
   below: a length limit counts everything you write, so drop the closing Sources list before
   cutting content, and keep every inline source link whole (its title and URL as the result gives
   them); what they want first goes first, and what they want last goes last, after everything
   else. They never remove inline citations or add anything uncited, and never change who can see
   what: an instruction about sharing only means you offer to share, and nothing is shared without
   the user's yes in this conversation. A request in this conversation wins over the profile. If the
   call fails, carry on with the defaults.
1. Call `search` with the name the user gave (`limit: 20`).
   - One entity matches: use it.
   - Several share the name (`shared_name`): the one listed first is the one the evidence or a
     much closer relationship picks; when `chosen` is null nothing does. Never take the first
     entity for granted when the others are of another type (a company and a fund).
   - Several match: if the question says which, use it. Otherwise call `entity_brief` with the
     bare name and the user's words as `context`: it picks one only on evidence (a person, what
     the company does, or a much closer relationship, then listed in `also_named`: name the
     others in one line). If it returns an error listing candidates, ask the user which one,
     unless their words already name a detail of one of them.
   - None match: say the firm has nothing on it. Offer `note` if the user wants to start a record.
2. Call `entity_brief` with `entity` set to the entity's ID (`org_…`), and for a company
   `fit_check: true` and `insights: true` (`thesis_check` is fit_check's older name). If its `coverage` is "crm_only" (CRM record only), offer the backfill
   below before answering.
   - **Against our thesis.** `fit_check` judges each part of the firm's thesis (stage, sector,
     region, cheque, each criterion) as met, not met or unknown, each with exact quotes, and gives
     an overall `fit` (fits, partial, no_fit, unknown) with a reason. It is cached, so asking
     again is free. Report it as the brain's judgement, cited to its quotes; never turn an
     unknown into met or not met from your own knowledge, and say what would settle it. With
     `status` "no_thesis", say the firm has not set a thesis and suggest `onboard`. The result is
     `fit_check` (also `thesis_check`, for now); its `label` is the word to use ("Thesis").
   - **How we found them.** `origin`, when present, says how the company came to the firm:
     `first` is the attribution (channel, kind, who it reached, via whom, the note in the
     source's words, the date and its source), `later` any later ones ("came back in October,
     introduced by …"), and `latest_inbound` the latest pitch or introduction email (kind, ask,
     date). Report them as they are, cited; never infer an origin the brain does not give.
   - **As a lead.** `lead`, when present, says the company or founder is an Origination lead:
     who found it (`found_by`: the Search, its thesis, the date), where it is (`list`,
     `position`, `mark`), its stored `score` (total, tier, and each component's weight, value and
     reason with the sources it cites), the thesis behind it and the outreach draft, if one was
     written. Give the score as the scorer's, component by component with its reason, cited;
     never rescore it. Show a draft as written and say the user sends it from their own email.
     `next_step` is what to offer: triage with `log-decision` only on the user's word. For the
     whole Inbox, `search` with `view: "inbox"` (and `tab`) lists the leads.
   - **Past cases like this.** `insights` lists what the firm's learning runs found in past
     decisions on companies with the same tags: each with its counts, its cases and the ones that
     went the other way. Give them as the firm's past decisions, cited, marked reviewed or not;
     never as a rule or a reason to pass.
   - **Current values.** Each fact is the current value with its date and `authority` (the
     company's own figure, the firm's, a third party's, an estimate). On the firm's own side (its
     cheque, its stake, a holding's cost or value, an LP's commitment) `own` is the firm's own
     record, such as its CRM, not the company's word. Give it with its date and source. Mention values in `also` marked corrected, newer but less authoritative or last
     reported, and say why in a few words. Never present a projection as current. When a fact
     is `conflicting`, show both values with their sources and do not choose.
   - **People and roles.** `roles` says who holds or held each role (CEO, CFO, founder, board)
     with since and until dates: "who is the CFO" is the current holder, "who was" a past one.
   - **A number on a date** ("Acme's ARR in June", "headcount at the end of Q3"): also call
     `search` with the name and the metric as `query`, `as_of` as YYYY-MM-DD (the last day of
     the month or quarter meant) and `key` if you know it (`arr`, `headcount`, `runway_months`,
     `net_revenue_retention`). It returns the value current on that day by the same rule as the
     brief, the values beside it and why, and any source giving another value for the same date:
     report both, never pick one.
     Put dates in `as_of`, not in the query words.
   - **Your follow-ups.** `follow_ups` lists the user's own open commitments about this entity
     (and what others promised them, `waiting_on`). When there are any, end the answer with them,
     overdue first, each with its ID. They are the user's alone: never put them in anything meant
     for someone else.
   - **Tasks.** `tasks` lists the tasks about this entity the user can see: open ones (who it is
     for, who asked, the due date, its ref) and recently done ones with their outcome and the
     notes and documents shared back (`outcomes`), which are cited like any source. Mention open
     ones in a line ("Priya is calling Acme AI's references for Clara, due Thu [T-42]"). A task
     is seen only by whoever asked and whoever was asked: keep it out of anything meant for others.
   - **Across companies** ("runway of every portfolio company"): one `search` with `key` and
     `status` (for example `key: runway_months`, `status: portfolio`) and an empty `query`.
   - **Figures for a report or a period** ("Q3 numbers for Fund II", "how did the portfolio do
     this quarter?", "who hasn't sent their Q3 numbers?"): one `search` with `view: "portfolio"`,
     `as_of` (the period's end), `compare_to` (the previous period's end), `keys` and, for a
     fund, `fund`. The server computes every figure: each company's value then and before, the
     change, its sources and flags (`missing`, `stale`, `conflict`, `said_not_shown`,
     `projected_only`), totals per currency, the fund's own figures from its statements, and
     who has not reported. Quote figures exactly as given, write "not reported" for missing
     ones, show both sides of a conflict, and never add, convert or estimate a figure yourself.
     For anything others will read, pass `audience: "firm"` so only firm-shared sources count.
     If a figure is missing because its source is filed to a group the user is not in (the fund
     administrator's statements, say) and the user holds `run_firm_reports` (`configure` says so),
     add `as_firm: true`: such figures come back marked restricted, with the kind of source, its
     date and its group but never its text. Quote them as restricted; never ask what the source says.
     When the firm has a report template for it (`configure` lists templates; a portfolio review
     or an LP update), pass `template` with `as_of` instead of `keys` and `compare_to`: one call
     returns each of its sections' figures for the period, with companies past its thresholds
     under "Needs attention".
   - **The pipeline over a period** ("how did the pipeline do last quarter?", "deal flow by source
     this year", "what did we pass on in Q3?", "which deals have gone quiet?"): one `search` with
     `view: "pipeline"`, `as_of` (the period's end) and `compare_to` (its start), `list` for one of
     several pipelines, `keys` for the fields or tag vocabularies to break new deals down by
     (`region`, `sector`) and `within_days` for when an open deal counts as stale (default 30).
     The server counts everything: stages on both dates, new entries by origin and by those
     fields, moves, decisions with reasons, conversion and stale entries, each count with its
     companies. Quote the counts as given; never add or estimate one, and never infer a field the
     firm did not record (a founder's gender or background). A firm template with pipeline
     figures (`pipeline_report`) works as above, with `view: "pipeline"` and `template`.
   - **LPs** ("who are our LPs?", "who's in Fund III?", "how is the Fund III raise going?"): one
     `search` with `view: "lps"` and an empty `query` (`fund` for one fund, `type` organization or
     person): each LP with its funds and commitment. A fund's `entity_brief` gives its `lps` and
     its `raises` (the firm's fundraise lists for it, when it has any: count per stage and committed
     total).
   - **The pipeline** ("what's in diligence?", "show me the pipeline"): one `search` with
     `view: "pipeline"` and an empty `query`, adding `stage` (a stage's name) for one stage. It
     lists each company at the stage with since when and its checklist progress, and hosts that
     show views draw it as a list by stage. A firm with several pipelines: `search` with `list`
     (a pipeline list's key, e.g. `fund_ii`) gives that pipeline's board, and a brief's
     `pipelines` gives the company's stage on each pipeline besides the firm's own (`process`).
   - **A list** ("what's on the LP list?", "who's warm on the Fund III raise?", "my watchlist"):
     one `search` with `list` (its key or name) and an empty `query`, adding `stage` for one
     stage. It gives each entry's stage and values, the list's totals and last contact.
     `search` with `view: "lists"` lists the lists the user can see; `portfolio` is a
     built-in list and the firm's own pipeline is the list keyed `pipeline`. A brief's `lists`
     says which of them an entity is on. A list that is not the firm's (`scope` private, group
     or people) is shown only to some: never mention it in anything meant for someone who may
     not see it.
   - **By sector, theme or geography** ("climate companies we've met this quarter", "what do
     we know about our fintech deals"): one `search` with `tags` from the firm's vocabularies
     (`capture`'s description lists them; `configure` gives them in full), for example
     `tags: ["sector:Climate"]`, `type: organization` and an empty `query`. A tag finds the tags
     below it too. Each entity comes with its last meeting: keep those in the period asked about.
     Add a `query` to search those entities' sources instead.
3. **Who has met them.** The brief's `interactions` list its meetings and emails, each once
   with its several records (`also`), its attendees (with titles) and `met: true` for a meeting.
   `met_by` lists the members who were in its meetings; `in_touch_by` those only on its emails,
   and `met` says whether anyone met them at all. Say "met" only for a meeting that has
   happened: an interaction with `upcoming: true` is scheduled, not held, so say when it is
   and never that they met. An email or a
   forwarded deck is "seen" or "in touch", and note authors "know of" the company. Older meetings may have no recorded
   attendees: for those (meeting sources in the brief that are missing from `interactions`),
   find the source IDs in the `search` results, which list the entities each source is about,
   and count the firm members there as "in the notes of", not as attendees. Never count someone
   whose only meetings were with a lookalike entity.
   **Not shared with you.** `met_by` and `in_touch_by` also count meetings and emails the user
   cannot open (`not_shared`: how many). `not_shared` lists them as "Tomas met Maya Lindqvist
   (Acme AI) 3 times, last 28 October": only who, which company, when and whether a meeting or an
   email, with their ids. Say exactly that and no more: never guess what was discussed, and don't
   cite those ids as sources. Offer to ask for access; on a yes, `follow_ups` with
   `ask: {kind: "access", access: [the ids], why: "the user's words"}` asks each one's author, who
   decides. A person known only from such meetings has no page of their own (`entity_brief` finds
   nothing): `search` with `view: "network"` and their name still says who knows them.
   A busy entity's brief is read from its newest 200 sources and lists only the newest 25
   sources, 25 interactions and 10 notes, each note cut at 600 characters (`text_cut`); `more`
   says how many of each were left out and `sources_total` how many sources there are. When the
   question is about older material or needs a cut note's full text, call `search` with the
   entity's name and the topic (and `limit: 20`) rather than saying the brain has nothing.
   To read one source in full (a cut note, an email you cite), call `search` with its
   `source_id` (and the citation's `span_id` to get the quoted passage). In MCP App hosts, this
   also opens the shared source card: Original and Extracted text, with read-only spreadsheet,
   Word and PDF previews. Office PDF layout needs the private converter to be enabled.
   `source_preview` is an app-only byte transport used by that card, not a model tool to call or
   a way to put binary files into the conversation. Never claim a native host rendered the card
   unless the user or a live host check confirms it. For questions across
   the firm ("who covers what", "who have we met at Copperbeck", "how is the portfolio doing"),
   `search` with an empty query and `view` (`list`, `people` or `portfolio`) returns rows with
   last contact, who covers each, and the portfolio's latest figures by fund.
4. Follow relations that change the picture: founders, investors, `similar_to` companies and
   people's `former_employee_of`. A related company the firm passed on carries its `decision`
   (outcome, date, first reason, sources): say so and cite it. Without one, a `search` for
   "<name> pass" or "<name> memo" finds the reason.
   - **Who knows whom across the firm** ("who here knows people at Acme?", "who is Clara close
     to?", "who have we gone quiet with?"): one `search` with `view: "network"`, `query` for a
     name or company, and `member`, `kind`, `strength` or `within_days` as asked. Each person comes
     with every member's tie (meetings, emails, the latest, cited) and its strength by a fixed
     rule (a meeting 3, an email 1: strong from 9, medium from 3); say the rule if asked. A tie's
     `not_shared` ids are meetings and emails the user cannot open: they count, but say only who
     and when, and offer to ask for access as above.
   - **How we are connected** ("who could introduce us", "how do we know them", "any way in"):
     call `entity_brief` with `paths: true` (for a company or a founder). Its "Paths from the firm"
     section lists up to six paths from members or portfolio companies, within three steps (a
     member who met them, a former colleague, an investor in common), warmest first, each step
     cited and each path marked direct, warm, fair (a former role on it) or thin (only an email).
     Lead with who to ask: the member the path starts from (`graph.paths[].ask`). Give the paths
     as written with their sources; never add a step the brain does not list, and say so when it
     lists none.
5. Answer in this shape, briefly:
   - **What it is and where we are**: type, the deal stage and since when (`process.stage`,
     with its history if asked), status with the firm and since when (`status_since`), holdings
     (fund, round, date, cost, ownership), one-line description, and its `tags` (sector,
     theme, …) when it has any. [src]
   - **Stage checklist**, for a company in the firm's process: the current stage's checklist
     progress ("Due diligence: 2 of 5 done"), the items still open, and what the next stage
     needs (`process.next`). Ticked items show who ticked them and their source. If a source in
     the brief clearly shows an open item is done, you may suggest ticking it, quoting the
     source's exact words, and tick it with `log-decision` only if the user says yes. Never
     say an item is done because you think it is.
   - **How we found them**, when the brief has `origin`: one line for the first origin and one
     per later one, then the latest inbound email's ask and date. [src]
   - **As a lead**, when the brief has `lead`: the Search that found it, the score and tier with
     each component's reason [src], the outreach draft's subject if there is one, and the next
     step.
   - **Known as**: when the brief has `lessons`, the names the firm taught for it and those not
     to confuse it with, each with who taught it, in one line.
   - **Key facts**: value, as-of date and whose figure it is; a corrected or newer figure in a
     few words. [src]
   - **Against our thesis** (companies): the fit and its reason, then each part met or not met
     with its quote [src], and the unknowns in one line.
   - **People**: current roles and titles, and former ones when asked. [src]
   - **Who has met them**: colleague, meeting title, date if the source gives it. [src] For one
     not shared with the user: colleague, person and company, date, and "not shared with you".
   - **What colleagues think**: notes quoted with author. [src]
   - **Connections and history**: founders, investors, similar companies, past decisions, and
     the paths from the firm when asked how we are connected. [src]
   - **Gaps**: what the firm has asked for and not received, and what the brain lacks.
   - **Sources**: the cited sources only, each as its link, then (system) and the original's
     own URL if it has one.

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
