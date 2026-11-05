# Interview and the firm's own documents

Use this when the host has no web search or research found little, for the firm's own documents
(a process document, a strategy, fund documents), for what research cannot answer, and on a
re-run to change what is configured. The rules in SKILL.md apply.

1. Call `configure` with no arguments. If the partner has documents about the firm (how it runs
   its process, its strategy or what it looks for, its fund documents), offer to start from
   them: run the `drop` skill on them, passing `doc_type` for each one the partner named (for a
   venture firm `investment_process`, `thesis`, `firm_policy`, `lpa`, `ppm`, `fund_deck`; the
   `drop` skill lists them). Without a scope, a document stays private to the partner; that is
   fine, its proposals are theirs to accept.
   Wait for the jobs (`job_status`), then call `configure` again and go to step 1a. Do not read
   the documents yourself.

   1a. **Proposals.** Walk the partner through each proposal, one section at a time: the
   proposed stages with their checklists, the fit profile (only what it `adds`), the funds, each
   beside what is configured now and with a short quote showing where it came from. Ask "Accept, change or skip?" For
   accept, call `configure` with that decision; for a change, the edited section and the
   acceptance together; for skip, `"dismiss"`. A proposal from a document only the partner can
   see (a private fund document) becomes firm-wide configuration once accepted, while the document stays
   private: say so and ask before accepting; `configure` repeats it as a warning. Then interview
   only for what no document gave (usually members' emails and focus areas).
2. **Nothing stored yet:** interview, a few questions at a time, and wait for the answers:
   1. **The Setup sections**, in the onboarding report's order (`configure` with `onboarding:
      true`), each with its own question. By what a section fills:
      - `fit`: what the firm looks for, in one sentence, and each part the question names; then
        **criteria**: anything else they screen for, one item each, and which are musts and
        which are nice-to-haves.
      - `process`: offer a template and show its stages in one line each; `configure` with no
        arguments lists each template's stages, checklists and documents while the firm has no
        stages. Then ask what to rename, add, remove or reorder in the firm's own words, and
        whether each stage's checklist and documents fit. Keep each stage's kind; ask when a
        renamed or new stage's kind is unclear. A firm that names no process gets the default
        template.
      - `status:…`: the organisations, each captured with one of the section's statuses once
        the partner confirms it (`references/research.md`, "Storing what the partner confirmed").
      - anything else: its question, saved as "How `configure` works" in SKILL.md describes
        that section.
   2. **Team**: each person's name, email, role and focus areas.
   3. **Custom fields** (optional): anything they track per company, person or deal beyond the
      basics, for example lead partner or deal source. Each field is `entity_type`
      (`organization`, `person`, `fund` or `deal`), `key` (lowercase snake_case), `label`, and
      `kind` (`text`, `number`, `date`, `choice` with its `choices`, or `list`). For a figure,
      also give `unit_kind` (`currency`, `count`, `percent`, `months` or `ratio`) and
      `synonyms`: other names the firm's sources use for it ("venues", "live restaurants").
      Skip this if they have none.

      Alludium Brain already records standard figures per type, listed in `capture`'s `facts`
      description (for example `arr`, `paying_customers`, `round_target`,
      `pre_money_valuation` and `logo_churn` for organizations, `round_size` and `check_size`
      for deals). Do not add a custom field for one of those: say it is already tracked under
      that key (each also has synonyms: "employees" is `headcount`). A custom field's key and
      synonyms also become fact names, so figures captured later are stored against it, and
      figures already stored under its key or a synonym are filed under it when it is added
      (`configure` says how many). Suggest a custom field for a figure the firm tracks that has
      no standard key.
   4. **Memo headings** (optional, when the firm drafts memos with a firm skill such as
      `ic-prep`): the headings the firm's memos use, in order, with a
      line on what goes under each if they want, and any house style (for example "British
      spelling, figures in $m, four pages at most"). If they paste or attach a memo template,
      take the headings from it in its order and confirm them; leave out its boilerplate. Skip
      this if they are happy with the default headings.

   **Already configured:** summarise what is stored in a few lines, ask what to change, and
   ask only about those sections. A firm configured before structured stages has stages with
   kinds guessed from their names and no checklists: show the kinds and offer to add
   checklists, once. If the partner just says what to change ("add Priya, her
   email is priya@northwind.vc"), skip the interview.
3. **Confirm.** Show what will be saved, section by section. On a re-run show only the sections
   that change, as before and after, and name any member who would be dropped. Ask
   "Save this?" and wait for a clear yes. Apply any corrections and confirm again.
4. If you have not described them in this conversation, call `configure` with `describe` and the
   changed sections; if `Who:` says you cannot change one, tell the partner who can and leave it
   out. Then call `configure` with only the changed sections. For `process`, pass every stage, with
   its stored `key`, kind, description, checklist and documents, including stages that are not
   changing. For `members`, pass the full team,
   including people who are not changing, with their stored emails, roles and focus areas,
   and put anyone the partner agreed to drop in `remove`. If `configure` says the update would
   drop someone, do not add them to `remove` yourself: ask the partner whether to keep them.
5. Reply in two or three lines: which sections were saved and how many members the team now
   has, with no source ID or link (a configuration save needs none). If `configure` lists `tag_suggestions`,
   say how many and offer to review them (below). Suggest the next step once: "Try
   `brief` on a company, or `note` to add a first take."

