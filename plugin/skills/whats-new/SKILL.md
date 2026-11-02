---
name: whats-new
description: A cited digest of what changed in the firm's Alludium Brain since a given time - inbound pitches and introductions, decisions, status changes, new notes, meetings, emails and documents, shares and changed facts - across the firm or for one company. Load it before calling whats_changed. Use when the user asks "what's new?", "anything I should know this morning?", "what changed since yesterday?", "anything new on Acme this week?", "what changed in Ferrolith's numbers?" or for a morning digest. Also sets up and runs the nightly scheduled task that files each day's meetings, the email the firm keeps and chosen Slack threads into the brain.
---

# What's new

Turn the Alludium Brain connector's `whats_changed` result into a short digest, grouped by company,
with every line cited.

If this is the nightly filing run (the task prompt says so), read `file-my-day.md` next to this
file and follow it instead of the steps below.

## Rules

- **Only what the tool returned.** Do not add background from `entity_brief` or your own
  knowledge unless the user asks.
- **Cite every line** with links to its sources, with their titles, from the result's "Source
  links", for example [Email from Priya Raman, 30 Oct 2026](https://…/sources/…); never a bare
  `src_…` ID.
- **Private material.** Mark changes with scope `private` as "(private to you)".
- **Email kept private.** A change that ends "kept private (…): share?" or "private, looks like
  <a kind of mail the firm keeps, such as deal flow>: share?" is one of the user's own emails that
  Alludium Brain did not share. List these together under **Kept private**, one line each with the
  reason, and ask once whether to share any. Share only the ones the user names, with `share` and
  `scope: "firm"`; never share one without being asked.
- Do not paste the tool's change list back as it is; group and shorten it.

## Steps

0. **Your profile first.** Call `configure` with `me: {}` once per conversation (reuse what it
   returned after that). Follow the user's `digest` preferences, their `never` and `general` items
   and any remembered instruction for this kind of task; preferences filed under another topic are
   for other tasks. They set length, order, emphasis and voice, and win over the default shape
   below: a length limit counts everything you write, so drop the closing Sources list before
   cutting content, and keep every inline source link whole (its title and URL as the result gives
   them); what they want first goes first, and what they want last goes last, after everything
   else. They never remove inline citations or add anything uncited, and never change who can see
   what: an instruction about sharing only means you offer to share, and nothing is shared without
   the user's yes in this conversation. A request in this conversation wins over the profile. If the
   call fails, carry on with the defaults. For example, if they want portfolio first or no shares
   and status confirmations, do that.
1. **The window.** Turn what the user said into an ISO timestamp for `since`, in their time
   zone if you know it, otherwise UTC (say which):
   - "since yesterday" → yesterday 00:00; "this week" → Monday 00:00; "since Tuesday" →
     Tuesday 00:00; a date or time as given.
   - "since last time" or "since I last checked" → the time of your previous digest in this
     conversation. If there is none, use the default and say so.
   - Nothing said → leave `since` out (the last 24 hours). On a Monday, use Friday 00:00.
2. **One company or the firm.** If the user named a company, `search` it (`limit: 5`), keep
   lookalikes apart as the `brief` skill does, and pass its ID as `entity`.
3. Call `whats_changed` with `since`, `entity`, and `limit: 200`. For a morning digest across the
   firm, add `mine: true`: `upcoming` then lists the user's own next meetings (soonest first);
   open the digest with them, one line each, before the changes.
4. **Group.** Every change lists the entities it is about. Group by the company, fund or deal
   each one is about. The firm's own members and the firm's own organization are not groups; a
   change about only people goes under the company they work for if the change says so, else
   under **People**.
5. **Shorten within each group**:
   - A status line that says `confirmed as` repeats the current status; leave it out. Keep
     `recorded as` and `changed from … to …`.
   - A decision and the status change it caused are one line.
   - Several sources of the same kind by the same author become one line with a count and
     a link to each, for example "3 emails from Priya Raman on Q3 numbers ([1](…), [2](…),
     [3](…))".
   - Fact changes: label, old → new value, as-of date. A change with `conflict: true` means two
     sources disagree about the same date and both are kept: give both values with their
     sources, never pick one.
   - Each change's `at` is when it happened (the meeting, the email, the as-of date) and
     `captured_at` is when the brain got it. Date lines by `at`; when the two are far apart, say
     so ("a 2024 memo, filed today").
6. **Write the digest**:
   - First line: the window ("Since Thu 29 Oct 09:00 UK time") and, for the firm, how many
     companies and decisions ("4 companies, 1 decision").
   - **What came in** first, before everything else: the changes of kind `inbound` (a pitch, a
     banker's process, an introduction or a co-investor's share classified in the window) and
     `resurfaced` (one from a company the user could already see as passed, on hold or met). One
     line each, resurfaced first: the company, the kind, the ask in the email's words, who it
     reached (`inbound.to`) and, for resurfaced, what was known before with its date and reason
     ("passed 15 Sep: consumer app"), cited. The email's own "added email" line is the same
     source: fold it into this line, keeping its "share?" offer. Then offer once to triage them
     ("3 pitches came in: triage now?"). On a yes, load the firm's `triage-inbound` skill
     (`configure(skill="triage-inbound")`) and follow it; if the firm has none, read `search` with
     `view: "inbound"`, which gives each one's fit and whether anyone has decided on it since.
   - **Decisions and status changes** next, across all companies, one line each.
   - Then one short section per company, most recent change first, at most five lines each.
     Name a company's status when the change list gives it.
   - **People** last, only if anything is left. Firm configuration changes (the
     `external_record` sources about the team) go under **Firm setup**, one line.
   - If nothing changed: "Nothing new that you can see since …". If the result says more
     changes exist, say the digest is partial and offer one company at a time or a shorter window.
   - **Asked of you**, from `tasks_new`: tasks colleagues asked of the user in the window, one line
     each with who asked, the action, the due date and the ref ("Clara asked: call Acme AI's
     references, due Thu 5 Nov [T-42]"). Offer to work on one ("work on Alludium Brain task T-42").
   - **Your requests**, from `requests_changed`: the user's requests that were done, declined or
     cancelled, one line each with who, the outcome text in their words (or the reason for a
     decline) and the ref; cite each shared note or document in `outcomes` by its link. Leave out
     either section when it is empty.
   - **Your follow-ups** last, from `follow_ups` in the result (the user's own, open): overdue
     ones first with how late they are, then those due soonest, at most eight lines, each with a
     link to its source (keep the `fu_…` ID for `update`; the user needs no ID). Say "(waiting on …)" for `waiting_on`. Leave the
     section out when there are none. Add one line for any in `follow_ups_changed` (ones the user
     closed, reopened, rescheduled or shared since then, in Claude or the viewer). When the user
     says one is done or no longer needed, call `follow_ups` with
     `update: [{"id": "fu_…", "status": "done"}]` (or `"dismissed"`).
   - If the result has `to_label`, end with **Documents to label**: the user's own documents
     whose type the brain could not tell, one line each, and ask what each is. Record an answer
     with `request_upload`, passing only the entry's `source_id` and the `doc_type`; nothing is
     uploaded or created.
   - If the result has `proposals_pending`, add one line: configuration proposed from the
     firm's documents is waiting, and the `onboard` skill reviews it.
   - If the result has `learned`, add **What the brain learned**: one line per item, from its
     `statement`, who taught it (`by`) or that it was learned from a fix, and its id. If
     `lessons_proposed` is more than 0, add one line that the brain has proposals waiting and the
     `onboard` skill reviews them. Never accept a proposal from the digest.
   - If the result has `insights`, add **What the firm's decisions suggest**: each new or changed
     insight in one line, from its statement, and whether it waits for review (`candidate`). The
     `onboard` skill reviews them; never mark one from the digest.
7. **Offer the nightly task**, once, at the end of a firm-wide digest: "Want the brain fed
   every night? I can set up a scheduled task that files each day's meetings and the email we keep."
   Skip the offer if a scheduled task named "Alludium Brain: file my day" already exists (check if
   you have a tool that lists scheduled tasks) or the user has declined in this conversation.

## Set up the nightly task

Do this when the user accepts the offer or asks for the nightly task.

1. **Who sees their email and meetings.** Call `configure` with no arguments and read the firm's
   email rule (`email_scope`; `pipeline` when it is not set), which the nightly run applies to
   meetings too. Explain it in one line: `pipeline` shares an email or meeting with the firm when
   it involves a company or person in the pipeline or portfolio, `firm` shares all of them,
   `private` keeps all of it to the user. Whatever the rule, Alludium Brain keeps sensitive ones
   (personal, HR, pay, legal, health, NDA, LP-confidential)
   private, and their morning digest offers to share what was kept back. Ask whether the firm's
   rule suits them or they want `private`, `pipeline` or `firm` for their own email.
2. Check what will feed it: a notes connector (Granola, Fireflies, Otter, Fathom and so on) for
   meetings, a calendar connector (Google Calendar or Outlook) for meetings with people outside
   the firm that have no notes, a mail connector (Gmail or Outlook) for the email the firm keeps
   (the step 1 read lists its mail rule under **Mail the nightly run files**: say it in one
   line), and Slack for threads in chosen channels. Say which are connected and that missing ones
   will be skipped.
   If Slack is connected, ask which channels to file (for example `#deal-flow`, `#portfolio`;
   none by default). Say that a public channel's threads are shared with the firm once Alludium Brain
   has checked them for sensitive content, and a private channel's stay private to them. Direct
   messages are never filed unless they ask for them.
   Then record what you found with `configure` `connections` (each `{"category": …, "system": …}`
   for the connectors you have: `email`, `calendar`, `meeting_notes`, `crm`, `drive`, `data`,
   and `other` for Slack),
   after saying in one line that everyone at the firm can see which systems each person has
   connected (not their content). It replaces only the user's own entry.
3. If you have a tool that creates scheduled tasks, show the user the name, schedule and prompt
   below, ask them to confirm, then create it: name `Alludium Brain: file my day`, daily at 22:30 in
   their time zone (cron `30 22 * * *`), no folder, with the prompt below. Pass on anything the
   result says about when it runs, for example only while the app is open. Otherwise give them
   these steps:
   1. In Cowork, open **Scheduled** in the sidebar, then **New task**, then **Set up manually**.
   2. Name it `Alludium Brain: file my day`. Set the frequency to **Daily** at 22:30, after the
      working day.
   3. Do **not** pick a folder: a task without a folder runs in the cloud, while the laptop
      is closed.
   4. Choose an approval mode that lets it call the connectors and Alludium Brain without waiting
      for someone to approve each call.
   5. Paste the prompt below, save, and click **Run now** once to check that it finishes.
4. The prompt:

   ```text
   Use the Alludium Brain plugin's whats-new skill for the nightly filing run (file-my-day).
   Window: from 00:00 yesterday, my time, until now.
   File meetings from my notes connector, outside meetings from my calendar, the email my firm keeps from my mail connector and threads from my Slack channels into Alludium Brain.
   Include meeting transcripts: no.
   Email scope: firm default
   Slack channels: none
   Include direct messages: no
   Finish with the summary table.
   ```

   Replace `firm default` with the user's choice from step 1 if they made one, and `none` with
   the channels they chose in step 2.

5. Tell the user that filing runs as them: meetings go in with the firm scope (colleagues can
   see them), email and its attachments follow the email rule from step 1, and Slack threads
   follow their channel. Re-filing
   is safe: the brain skips records it already has.
