---
name: log-decision
description: Record a firm decision on a company or deal in Alludium Brain - move it to a stage of the firm's deal process, pass, lose, put on hold, or invest - with the reasons in the deciders' words, who decided, the date and the sources it rests on; and tick checklist items the user confirms are done. Use when the user says "log a pass on Acme", "we're passing on Kestrel because …", "record that we're moving Acme to IC", "Acme is in due diligence", "we lost Wren to another fund", "put Ferrolith on hold", "we decided to invest in Ferrolith" or "tick customer references for Acme"; and a decision that moves nothing, about any company, person or fund ("we're dropping Kestrel as our fund admin", "Maya joins our advisory board"). Also use it to offer, never silently, when the user mentions a decision without asking to record it. Not for an opinion or a take that is not a decision (use note).
---

# Log a decision

Record one decision, or checklist ticks, with the Alludium Brain connector's `log_decision` tool,
after the user has confirmed it. A decision moves the company or deal to a stage of the firm's
deal process, dated and cited, and keeps its history. On an organization it also sets the
status the stage implies (screening: `prospect`; evaluation through closing: `in_deal`;
portfolio: `portfolio`; passed and lost: `passed`; on hold: `tracking`). A `decide` records a
decision about anything, with its reasons, deciders, date and sources, and moves nothing.

## Rules

- **Reasons in the deciders' words.** Pass the reasons as the user gave them. Do not rewrite,
  summarise, strengthen or add reasons. If the user gave none, ask for them: the reasons are
  the point of the record.
- **The firm's stages.** Name the stage as the firm's process does (from `configure` with no
  arguments, or the brief's stage bar). Never invent a stage. The ways out are Passed, Lost
  (the firm wanted in and did not win it) and On hold.
- **Several pipelines.** A firm may run more than one deal pipeline: its own process (the
  default) and pipeline lists such as a fund's (`configure` lists them; `fund_ii` and so on).
  When the user names one ("move Acme to diligence on the Fund II pipeline"), pass `list` with its
  key and name its stages. A company on more than one needs `list`; `log_decision` refuses
  without it and names them: ask the user which. Each pipeline keeps its own stage, checklist and
  history; the company's status is the highest across them (a portfolio company that another
  fund passes on stays portfolio), so say the status it ends with. A private pipeline's
  decisions are private.
- **The right entity.** Resolve the name with `search` and pass the entity's ID (`org_…` or
  `deal_…`), never a short or shared name. A lookalike with a similar name is a different
  company.
- **Cite only real sources.** Supporting `source_ids` come from `search` results in this
  conversation, never from memory or a guess.
- **Offer, don't record silently.** If the user mentioned the decision without asking to record
  it, offer once in one line ("Log this pass on Acme AI Ltd in Alludium Brain?") and go on to the
  steps only after a yes. Offer once per decision; if they decline, drop it. Never offer for a
  decision the brain already has (its `search` results show a decision on the entity).
- **A person ticks a checklist item, never you.** You may suggest a tick when a source shows
  the item is done, quoting the source's exact words, but tick it only once the user says yes.
- **Confirm before writing.** A decision changes the company's stage and status for the whole firm.

## Steps

1. **Read the request**: the company, where it moves, the reasons, who decided and when.
   - Where it moves: "move to partner meeting", "take it to IC", "diligence" → `stage` with
     that stage's name. "Next stage" → `outcome: "advance"` with no stage (the next one in the
     process). "Pass", "decline", "not for us" → `outcome: "pass"`. "We lost it", "they went
     with another fund" → `outcome: "lose"`. "Park it", "on hold", "come back next year" →
     `outcome: "hold"`. "Invest", "we're in", "signed" → `outcome: "invest"` (the first
     portfolio stage; `win` means the same and is stored as win, shown as invest), or `stage`
     if the user named one, for example "Term sheet". If it is
     unclear, for example "send a term sheet" when the firm's process has no term sheet stage,
     ask which stage. A company back from Passed, Lost or On hold ("they're raising again,
     let's take another look", "back on") is `outcome: "advance"`: without a stage it goes to
     the stage after the last one it was at (the first stage if it never had one), and the
     history keeps the way out. Name the stage if the user said where it goes back to. A
     decision that does not move a company through the process (a choice, a policy, a decision
     about a person, fund or service provider: "we chose Carta for the cap tables", "Maya joins
     our advisory board") → `outcome: "decide"`, with no stage or checklist. If it reverses an
     earlier decision, pass that decision's ID (`dec_…`, from the brief's decisions) as
     `supersedes`. Name the
     stage whenever the company is at the last stage (a follow-on is not an advance) or the
     decision is dated before its latest move: `log_decision` refuses an outcome alone there,
     so the status never contradicts the stage. A move dated before the latest one goes into the history without
     changing the current stage; say so.
   - Deciders: full names. "I" means the user. If the user says "we" or "the partners" without
     names, ask who decided. First names can be matched to the team from `configure` with no
     arguments.
   - Date: today unless the user gave one ("last Tuesday" → that date, as YYYY-MM-DD). A move
     made earlier and recorded now keeps the day it happened: the history is ordered by it. A
     decision not yet taken is not recorded: future dates are refused.
2. **Find the entity**: `search` with the name (`limit: 5`).
   - One organization matches: use it. Use a deal only if the user named that deal. A `decide`
     may be about any entity: a person, fund or deal as well.
   - Several match: pick the one this conversation is about, else the one in active work
     (status `prospect`, `in_deal` or `portfolio`), and name the other in the confirmation.
     If it is still unclear, ask.
   - None match: say so and stop. A decision needs a company the brain knows; offer `note`.
3. **Find supporting sources**: `search` "<entity name>" (`limit: 20`) and pick the few the
   reasons rest on: the latest meetings, a pass or IC memo, the notes that make the same points.
   Use any source the user named. Two to five is usually enough. Note which are private.
4. **Checklist.** `entity_brief` on the entity shows its stage, the stage's checklist and what
   the next stage needs. If the user said items are done, match each to the checklist's
   wording. If a source you found clearly shows an unticked item of the current or the new
   stage is done, you may suggest it in the confirmation with the source and its exact words.
5. **Confirm.** Show, and ask "Record this?":

   ```text
   Decision: advance Acme AI Ltd (org_…) from Partner meeting to Due diligence; status in_deal
   (or, for a decide: "Decision about Carta (org_…), moves nothing; supersedes dec_…")
   Reasons: <exactly as given>
   Decided by: Clara Oyelaran, Tomas Brandt, on 2026-10-30
   Sources: [Partner meeting, 21 Oct 2026](…), [Clara's note, 22 Oct 2026](…) (private)
   Scope: firm
   Tick (you said done): Partner meeting held
   Suggested tick: Key risks listed, from [Partner meeting, 21 Oct 2026](…) "we listed the
   three big risks: …" - tick it?
   ```

   If a source is private, say colleagues will see the decision but not that source. Use
   `scope: "private"` only if the user asks; a private decision does not change the firm's
   stage or status. Wait for a clear yes, and apply any corrections before writing. Leave out
   a suggested tick the user does not say yes to.
6. Call `log_decision` with `entity` (the ID), `stage` and/or `outcome`, `reasons`,
   `deciders`, `decided_on`, `source_ids`, `scope`, `supersedes` when it replaces an earlier
   decision, and `checked` for the items the user
   confirmed: `{"item": "<as the checklist words it>", "source_id": "src_…", "quote": "<the
   source's exact words>"}`, with the source and quote only when a source shows it. To tick
   items without a decision, pass only `entity` and `checked`. `done: false` unticks an item. Ticks take the call's `scope`: with a private decision
   they are private too. A `note` (the user's words, at most 500 characters, e.g. "references
   checked: two strong, one lukewarm") is recorded as its own cited note source. People can also
   tick items, with a note, on the company page in Alludium Brain or its card; the brief shows who
   ticked each one and their note.
7. Reply in two or three lines (no source ID): the decision, the stage it moved
   from and to and the status now, the items ticked, and any warnings from the result in
   plain words. If a cited private source was the user's own, offer to share it with `share`
   so colleagues can see why.
