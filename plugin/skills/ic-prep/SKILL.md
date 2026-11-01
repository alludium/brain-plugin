---
name: ic-prep
description: Draft an investment committee (IC) memo for a deal from what the firm's VC Brain knows - facts with their history and conflicts, the team's notes and meetings, decisions, open questions, thesis fit and similar companies the firm passed on - under the firm's own memo headings, with every claim cited. The deal lead edits it in the conversation and it is filed only on their say-so, private by default. Use when the user says "draft the IC memo for Acme", "prep Acme for IC", "write up Ferrolith for the partner meeting" or "start an investment memo on Kestrel".
---

# Draft an IC memo

Gather what the firm knows about one deal with the VC Brain connector's `configure`, `search`,
`entity_brief` and `whats_changed` tools, draft the memo in the conversation, let the deal lead
edit it, and file it with `capture` only when they say so. The memo is the author's document:
Claude drafts, the author decides what it says.

## Rules

- **The brain is the evidence.** Write only what the tools return. Leave out your own knowledge
  of the company, its market and its competitors; if the user asks for it, add it in a separate
  section headed "Not from the brain" with no source IDs.
- **Cite every claim.** Each sentence that states a fact, figure, quote, opinion or event ends
  with the full IDs of the sources it rests on, for example `[src_20e9…]` written out in full,
  so the filed memo links to them. Each bullet and table row carries its own citation. A
  comparison with the thesis cites both the fact and the firm configuration source. The source
  you cite must say the thing itself: a detail you saw only in a brief's summary or attributes
  (a city, a title, a date) needs the source that states it, from `search`, or it stays out. A
  sentence you cannot cite does not go in.
- **No further than the source.** "Met in the recorded meetings", not "the only one to have
  met them"; "eight customers", not "eight paying customers", unless the source says so.
- **Claimed, not shown.** A figure is *claimed* when its only sources are the company's own
  words: a deck, an email, a founder in a meeting, a CRM field typed from those. Write whose
  figure it is and where they said it: "ARR $1.4m as of Q3, claimed by the company in an email
  [src_…]". Call it *shown* only when a cited source is evidence of it (financial statements, a
  data-room export, a signed contract, bank or billing data, or a colleague's note that they
  checked it), and say what showed it. Third-party figures and estimates say whose they are.
- **History and conflicts.** Give each key figure's current value with its as-of date and
  earlier values when they show a trend or a change of story. When the brief marks a value
  `conflicting`, give both values with their sources and do not choose. Mention a corrected
  value and what corrected it. Never present a projection or a target as current.
- **Unknown is an answer.** When the brain has nothing on a point a memo needs (churn,
  burn, the cap table, a reference call), write "Unknown: …" under that heading and list it
  under open questions. Never estimate, extrapolate or fill a gap from general knowledge.
- **The recommendation is the author's.** Label the recommendation section "Draft by Claude:
  the deal lead's call". It may say only what the cited evidence supports: the strongest
  points for and against, and what would have to be true. It never says the firm should
  invest, pass or offer terms unless the user has told you their recommendation, in which case
  write theirs in their words. When the evidence is thin or conflicting, say the evidence does
  not yet support a recommendation and name what is missing.
- **Never merge lookalikes.** A company with a similar name (Acme AI Ltd and Acme Robotics
  GmbH) is a different company. Its facts, notes and people stay out of the memo, except as
  precedent when the firm passed on it.
- **Opinions with their authors.** Quote or paraphrase colleagues' notes and meeting remarks
  with who said them and when. Do not turn one person's view into the firm's view.
- **Earlier memos are opinions.** Cite an earlier memo for what its author concluded, never as
  the evidence for a figure or fact: cite the figure's own source.
- **The memo is about the company, not the brain.** Notes on the brain's own records (a
  lookalike left out, a deal entity not linked, a duplicate record, dates that look odd, what
  you filed) go in your message to the user, never in the memo text.
- **Private material.** The tools return only what this user may see, so a `private` source is
  the user's own. Use it and mark each line that rests on one "(private to you)". If any line
  does, put "Contains your private notes: do not forward" at the top of the draft.

## Steps

1. **Find the deal.** `search` the company name (`limit: 10`). Take the organization and its
   deal entity (type `deal`, for example "Acme AI Series A (2026)"); with several deals, the
   open one, unless the user named another. Use a deal only when its brief shows it is this
   company's round; a deal named only "Series A" or linked to other companies too is not, so
   leave it out, link only the organization and say so in one line. If several organizations
   share the name, ask which, unless the user's words settle it. With no match, say the brain
   has nothing on it and stop: a memo needs evidence. The author is the user unless they name
   someone else.
2. **Read the settings.** `configure` with no arguments gives the thesis, criteria, deal
   stages, team, the firm's **IC memo headings** (with a line of guidance each) and **house
   style**. Note the configuration's source ID: thesis-fit lines cite it. Then `configure`
   with `me: {}` for the user's own profile: keep its approved writing `style` (never a
   `pending_style`), their `writing`, `never` and `general` preferences and any remembered
   instruction for memos, for step 5. If the call fails, carry on without them.
3. **Gather**, by entity ID once resolved:
   - `entity_brief` on the organization, with `thesis_check: true` when the tool takes it:
     summary, key facts (current value, `also`, `conflicts`, authority, as-of), people and dated
     `roles`, notes, `interactions` with `met_by`, decisions, related entities, investors and
     holdings, and the company's fit with the thesis (each part met, not met or unknown, with
     quotes). Then `entity_brief` on the deal for the round.
   - **Round and investors**: `search` "<company> round valuation investors terms"
     (`limit: 20`). Also the lead and other investors from the brief's relations.
   - **Figures over time**: for the two or three figures that matter most (`arr`, `revenue`,
     `headcount`, `burn`, `runway_months`), `search` with the company name, `key` and `as_of`
     six and twelve months back, when the brief's values do not already show the history.
   - **Recent changes**: `whats_changed` with `entity` set to the organization's ID and `since`
     90 days back (or the first interaction, if later).
   - **The team's notes and meetings**: `search` "<company>" (`limit: 20`) for full notes the
     brief cut (`text_cut`) and older material it left out (`more`). Who met whom comes from
     `interactions`; a meeting marked `upcoming` has not happened.
   - **Founders and key people**: `entity_brief` on each founder and executive (at most four):
     background, former employers, how the firm knows them.
   - **Open questions**: requests the firm made that the latest emails and meetings do not
     answer, and concerns colleagues raised.
   - **Precedent**: companies the firm passed on that are like this one: the brief's
     `similar_to` relations, a founder's former company, or a company in the same thesis area
     the user names. For each with status `passed`, `entity_brief` for the decision and its
     reasons, or `search` "<name> pass" for the pass memo. At most three. Say why each is
     comparable and what differs, citing both. With none, say the brain has no comparable
     passes.
4. **Choose the headings.** The firm's IC memo headings, in their order and with their
   guidance, when `configure` returns them. Otherwise these:
   1. **Summary and recommendation**: the company and the ask in a paragraph, then the
      recommendation, marked as a draft (see the rules).
   2. **Company**: what it does, where, since when, its status with the firm.
   3. **Market**: only what sources say about the market; market sizes are claims.
   4. **Product**: what it does for whom, from demos, decks and calls.
   5. **Traction**: a key-figures table (figure, value, as of, whose figure, claimed or shown,
      source), then the trend and any conflicts.
   6. **Team**: founders and key people, their roles and backgrounds; who at the firm has met
      them and when.
   7. **Round and terms**: round size, valuation, lead and other investors, the firm's proposed
      cheque and ownership; each claimed or agreed, and by whom.
   8. **Thesis fit**: each criterion, one line each: meets, does not meet or unknown, cited.
      Use the brief's thesis check when there is one: its verdict per part, the quote and the
      source behind it; check each quote's source yourself and say where you disagree. A
      figure in another currency than the criterion is compared only at a rate a source gives;
      otherwise say so and leave it unknown.
   9. **Risks and mitigants**: risks colleagues raised, with who raised them, and risks from
      the gaps; a mitigant only when a source gives one.
   10. **Open questions**: what the firm asked for and has not received, and every "Unknown".
   11. **Precedent**: comparable passes and their reasons.
   12. **Appendix: sources**: every cited source, as `src_… title (kind, date; private to you)`.

   Under the firm's own headings, put each point under the heading whose guidance fits it best,
   and always end with the appendix of sources, even if the headings leave it out. Put
   unknowns and open questions under the firm's heading for them, or at the end.
5. **Draft.** Start with a header line: "IC memo: <company>, <round>. Draft by Claude for
   <author>, <date>. From VC Brain as of <date>." Keep it to what an IC reads in ten minutes,
   unless the house style says otherwise. Follow the firm's house style for spelling, units,
   number formats and length; follow the user's profile style and preferences for voice and
   phrasing only. The firm's headings and house style still decide structure, and the profile
   never removes a citation, adds anything uncited or changes who can see the memo. A request
   in this conversation wins over the profile.
   With neither, write plain, short sentences, figures with units and dates, and no
   superlatives. Do not paste whole sources or brief pages.
6. **Review with the deal lead.** Show the draft and ask them to edit it, starting with the
   recommendation, which is theirs to write. Apply their edits and show only the changed
   sections. Their words replace the draft's; an edit that adds a claim keeps its citation if
   they give one, else mark it "(author)". Do not file anything until they say to.
7. **File it, on their say-so.** Call `capture` with:
   - `kind: "document"` and `title` "IC memo: <company>, <round> (<author>, <date>)";
   - `text`: the memo exactly as the author last saw it, markdown included, from the header
     line to the appendix (no reply text around it). To change anything when filing (a line
     addressed to "you", say), show the change and ask first;
   - `scope: "private"`, and `entities` linking the organization, and the deal when step 1
     found one, by `id`;
   - `system: "claude"` and `external_id` `ic-memo/<organization id>/<author email>`, always
     (an artifact's link goes in `url`, never in the ID, so every filing finds the last one);
   - no `facts`: the memo's figures are already in the brain under their own sources.

   Filing the memo again after edits, in this conversation or a later one, uses the same
   `system` and `external_id`: the brain stores it as a new version of the same document
   (`revision_of`), with the same scope unless you pass one, and briefs show only the latest. A `.docx` or
   `.pdf` export of the memo goes through the `drop` skill instead.
8. **Offer to share.** Reply with the source ID and offer once: "Filed privately as src_….
   Share it with the firm?" Sharing shares the memo's text. If it rests on sources private to
   the author, list those lines first and ask whether to keep them in the shared version; if
   they are to go, file the edited memo as a new version (step 7) and share that one. On a yes,
   `share` it with `scope: "firm"`. When the IC decides, `log-decision` can cite the memo's
   source ID.
