# How `configure` works

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
  `{"min": 500000, "max": 1000000}`, in the fund's currency.
- Each section you pass (`fit`, `process`, `funds`, `custom_fields`, `members`,
  `memo_headings`, `house_style`) **replaces** the stored one. To add one criterion or one
  person, pass the whole thesis or the whole team. Never pass a section that is not changing.
- The thesis is the `fit` section (the firm's fit profile, which VC Brain shows as its thesis;
  `thesis` is its older name and still works, and reads return both). It is an object:
  `statement` (one sentence), `stages` (the funding stages the firm invests
  at, such as Seed and Series A, not its deal stages), `in_scope` and `out_of_scope` (sectors and
  themes), `regions`, `cheque` (`{"min": 500000, "max": 3000000, "currency": "EUR"}`, only when
  every fund's cheque is the same range in the same currency; when funds differ, give each fund
  its own `cheque` instead and leave the firm's out) and
  `criteria` (each `{"text": "...", "weight": "must" | "nice"}`, or without a weight). Leave out
  what the partner did not give. Put criteria inside `fit`; the separate `criteria` argument
  is only for older plugins. Alludium Brain checks companies against each part (`entity_brief` with
  `fit_check`), so keep each part short and specific.
- `members` is the whole team. `configure` refuses a list that leaves out a current member
  and names who would be dropped. To drop someone, name them (name or email) in `remove`, only
  after the partner has said to. `remove` on its own drops those people and keeps the rest of
  the team as stored. A dropped member loses the firm-member role; the person stays.
- **Someone who left the firm** ("Tomas has left"): `deactivate` with their name or email, after
  the partner confirms. They can no longer use Alludium Brain, everything they filed stays under
  their name, and they stay on the team marked as left. `remove` of someone who has signed in does
  the same; only someone who never signed in is dropped outright. `reactivate` lets them back in.
  Both need a firm admin, and nobody can deactivate themselves.
- **Firm admins.** Removing members, `groups`, `permissions`, `email_scope`, `meeting_scope`,
  `connectors` and `origination`'s sharing and caps
  change who sees or approves what, so once the
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
- `memo_headings` is the firm's IC memo outline, in order: each item a `heading` and an optional
  one-line `guidance` on what goes under it (a plain string is a heading with no guidance).
  The `ic-prep` skill drafts under these; `[]` goes back to its default headings.
  `house_style` is a short note on how the firm writes memos (spelling, units, length, tone);
  `""` clears it. Both are a list and a note, not a template: no formatting, fields or logic.
- `me` is a member's private profile, not firm configuration: never pass it here. A member's own
  preferences ("I like short briefs") go to the `profile` skill; the team entry (role, focus
  areas) stays here and shows in their profile.
- `tag_vocabularies` and `dismiss_tags`: see "Tag vocabularies" below.
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
- `origination` is how inbound pitches are handled: `inbound_sharing` (`ask`, the default:
  the member a pitch reached is asked to share it; `pipeline`; `private`), the nightly caps
  `classify_usd_per_night`, `inbound_fit_check_usd_per_night` and
  `lead_fit_check_usd_per_night` (fit checks of companies added to leads lists; USD, 1 each by
  default) and `route_by` (`recipient`, the default, `focus_areas` or `responsibilities`). Only
  the fields given change; every read shows all five. Sharing and the caps are firm admins only, once the
  firm has one. Nothing acts on `pipeline` sharing or on routing yet: say so if asked. Change it
  only when a partner asks.
- The configuration applies to the whole firm, so everyone at the firm sees it.

- `systems` is the systems the firm uses, by category: `email`, `calendar`, `crm`, `drive`,
  `meeting_notes`, `data` (data providers such as `harmonic`) and `other`, each a list of names
  (`{"crm": ["affinity"], "meeting_notes": ["granola", "zoom"]}`). It replaces the stored section.
- `connections` is the **caller's own** connected systems in their assistant, each
  `{"category": …, "system": …}` (`[]` records none). It replaces only their entry, never
  anyone else's, and **everyone at the firm can see it** (connector names and when, never
  content). Say so before you record it.
- `cites` says where items of the same update came from: each `{"field", "source_id", "quote"}`.
  `field` is `section.part` or `section[item]`: `fit.statement`, `fit.stages`,
  `fit.in_scope`, `fit.out_of_scope`, `fit.regions`, `fit.cheque`,
  `fit.criteria` (`thesis.…` still works), `funds[<fund name>]`, `members[<email, else name>]`, `process.stages`,
  `tag_vocabularies.sector`, `systems.crm`. The source must be shared with the firm and the
  quote must be its exact words; otherwise the whole update is refused and nothing changes.
  Cite only what came from a source; what the partner told you needs no cite (the
  configuration's own record says who saved it). Replacing a section drops its old cites, so
  pass the cites again with an edited section.
- `onboarding: true`, alone, reads the onboarding report: the `phase`, what the brain knows about
  the firm, the data and the team, the caller (`you`) and `gaps`, each a key and a question.

# Tag vocabularies

Tags classify companies, deals, funds and theses by the firm's own lists: sectors, themes,
geographies, stages of interest. Claude tags from them when filing notes and meetings, and the
server when reading decks and email; `search` with `tags` then answers "climate companies we met
this quarter". People are not tagged (a firm member's areas are their focus areas).

- **Setting them up** (optional during the first interview; ask "Do you want to tag companies
  by sector or theme? Which do you use?"). Each vocabulary is a `key` (`sector`, `theme`,
  `geography`), a one-line `description`, optionally `applies_to` (default: organization, deal,
  thesis, fund), and `tags`. Each tag is a `label` the firm uses, a `description` of what
  belongs (it guides Claude and the server's model, so make it specific), `synonyms` its
  sources use, and an optional `parent` for a sub-tag (`Carbon removal` under `Climate`).
  Build the lists from the partner's words and their thesis. Do not add sectors they did not
  name; keep each vocabulary short (tens of tags, not hundreds).
- `tag_vocabularies` replaces the whole list. To add a tag, pass every vocabulary with the new
  tag added. Relabelling a tag keeps its `key` (from `configure`'s output), so existing tags
  follow; a tag left out stops showing but is not deleted.
- **Suggested tags.** A label outside the vocabulary is never created: captures and the server
  store it as a suggestion, and `configure` lists `tag_suggestions` with how many entities and
  examples. Show them to the partner. For each one they accept, add it to the right vocabulary
  (or as a synonym of an existing tag, if it means the same); stored suggestions are then
  applied (`configure` says how many). Put the ones they reject in `dismiss_tags`
  (`["sector:Quantum"]`) so they are not listed again. Never accept or dismiss without asking.

