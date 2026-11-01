# Nightly filing run (file my day)

A scheduled task runs this with nobody watching. Copy the day's meetings, outside calendar
events, the email the firm keeps and threads from chosen Slack channels from the user's own
connectors into Alludium Brain with `capture`. Your job is a faithful copy with source IDs, plus
the commitments each record makes (`follow_ups`). You pass no facts: Alludium Brain extracts the
figures, roles and people from each email and meeting on the
server, with exact quotes, links them to the firm's entities, and recognises copies of the same
email or meeting from other tools.

## Rules

- **No questions.** Nobody will answer. When something is unclear (which company, whether an
  email is of a kind the firm keeps), skip that record and count it as skipped.
- **Word for word.** Pass text exactly as the connector returned it: no summarising,
  shortening, reformatting or fixing. If the connector returned less than the full text,
  capture what you have with `connector_truncated: true` and count it as truncated.
- **Source IDs on every capture**: `system`, `external_id` and `url` exactly as the connector
  gave them. Never invent an ID or a link; leave `url` out if there is none.
- **Run ID on every capture**: `run_id: "file-my-day-YYYYMMDD-HHMM"`, the run's start in UTC,
  the same for every capture in this run, so an operator can remove one run if it went wrong.
- **No facts, no relations.** Do not pass `facts` or `relations`; Alludium Brain extracts them.
- **Follow-ups.** Pass `follow_ups` on each meeting and email as the **Follow-ups** section of
  the `capture-meeting` skill describes: only concrete commitments by a firm member, or made to
  one (`waiting_on`), each with its exact sentence as `quote`. Most emails have none; when in
  doubt, leave it out. The user is the owner unless the text names another firm member.
- **One capture per record.** `Already captured` in a result means the brain had it; count it
  and move on. Re-running a window is safe.
- **No scope on email or meetings.** Leave `scope` out of email and meeting captures. If the
  task prompt says `Email scope: private`, `pipeline` or `firm`, pass it as `email_scope` on every
  email and meeting capture; otherwise leave that out too and the firm's rule applies. Alludium Brain
  keeps each one private until it has checked it, and keeps sensitive ones (an internal 1:1 about
  pay, an HR call) private whatever the rule says.
- **No scope on threads either**, and no `email_scope`: the channel decides. A public channel's
  thread is shared once Alludium Brain has checked it; a private channel's or a direct message's stays
  private to the user.
- Do not repeat captured text in your messages, and do not read attachments: only upload them
  (step 5).
- If a connector is missing or fails, skip it, carry on with the others, and say so at the end.

## Run

1. **Window**: from the task prompt; default from 00:00 yesterday in the user's time zone. A
   window by date works even when you cannot tell the time, and the overlap with last night's
   run is safe. Keep only records that started or were sent inside the window, checking each
   one's own start time or date, because some connectors ignore a date filter. The firm's email
   domain is the user's own email domain. Set the run ID now. Call `configure` with no arguments
   once and keep its **Mail the nightly run files** section: the firm's mail rule, from its packs
   and its own changes, which step 4 follows. Call `configure` with `me: {}`
   once and follow any remembered instruction about what to file or leave out (for example
   "never file email from my personal address"); it cannot widen what these rules allow or change
   any capture's scope.
2. **Meetings.** List the meetings in the window in the notes connector. File each one as the
   `capture-meeting` skill describes in steps 2 to 5, 7 and 8, without step 6 (no `facts`): header
   lines, the notes word for word, every attendee with their email and `attendee: true`, the
   company's `id` from `search`, `occurred_at`, `kind: "meeting"`, and the event's iCal UID in
   `refs` when the connector names the calendar event. Add transcripts only if the task prompt
   says `Include meeting transcripts: yes`. Note each meeting's iCal UID and start, or its title
   and start, for step 3.
3. **Calendar events.** List the events in the window in the calendar connector. Keep an event
   only if at least one attendee's email is outside the firm's domain (rooms and resource
   calendars do not count). Skip events the user declined, cancelled events, and events
   already filed in step 2 (the same iCal UID and start, or the same title and start). For
   each event kept, call `capture` with:
   - `kind: "meeting"`, `title`: the event title, `occurred_at`: the event's start (ISO with
     its offset), `system`: `google_calendar` or `outlook_calendar`, `external_id`: the event
     ID, `url`: the event link if the connector gave one, and
     `refs: [{"system": "ical", "external_id": "<iCal UID>"}]` when the connector gives the
     UID, so notes filed later join this meeting rather than counting twice;
   - `text`: these lines, then a blank line, then the description word for word (if any):

     ```text
     Title: event title
     When: start–end (time zone)
     Attendees: Name <email>, Name <email>, …
     Location: location or meeting link
     ```

     Leave out a line whose value the connector did not give;
   - `entities`: each attendee as a person with `attendee: true` and
     `{"system": "email", "external_id": "<email>"}`, and the company, resolved as in step 4.
4. **Email.** Search the mail connector for messages in the window, leaving out
   promotions, social and forum categories. Keep and skip messages by the firm's mail rule from
   step 1, its kinds as listed; when in doubt, skip. Personal mail is never filed, whatever the
   rule. Also skip automatic replies,
   out-of-office replies and calendar notifications (an `Auto-Submitted` header, or a subject
   such as "Automatic reply:", "Out of Office:", "Invitation:", "Accepted:"). Keep every message
   of a thread, each word for word: Alludium Brain sets quoted history aside. For each message kept,
   call `capture` with:
   - `kind: "email"`, `title`: the subject, `occurred_at`: the message date, `system`: `gmail`
     or `outlook`, `external_id`: the message ID, `url`: the message link if the connector gave
     one, and `refs: [{"system": "rfc822", "external_id": "<Message-ID header>"}]` when the
     connector gives the Message-ID, so a copy in a colleague's inbox or sent to email-in is
     linked rather than counted twice;
   - `text`: the `From:`, `To:`, `Cc:` (if any), `Date:` and `Subject:` lines as returned, a
     blank line, then the body as returned, then `Attachments: name1, name2` if it had any;
   - `entities`: each sender and recipient as a person with `attendee: true` and
     `{"system": "email", "external_id": "<email>"}`, and the company. Resolve each distinct
     company once by `search` on its email domain (unless it is webmail such as gmail.com) and
     reuse its `id`. If the company is unclear, link only the people;
   - `follow_ups`: the message's own commitments (not those in quoted history), if any.

   Upload a message's attachments (step 5) **before** capturing the message.
5. **Attachments.** Only for messages kept in step 4 that have a sender outside the firm's
   domain. Upload an attachment only if it is a PDF, slides (`.pptx`) or a spreadsheet
   (`.xlsx`), and 25 MB or smaller. Skip images, calendar files (`.ics`), signatures, zip
   files and everything else, and count them as skipped. If the mail connector cannot save an
   attachment as a file, skip it, count it and carry on. For each one kept, follow the `drop`
   skill's steps 2 to 5 (its script is `../drop/scripts/upload.py` next to this file), without
   opening the file, and call `request_upload` with:
   - `scope: "private"`, `system`: the message's system (`gmail` or `outlook`),
     `external_id: "<message ID>/<attachment file name>"`, and the message's `url` if any;
   - `entities`: the company resolved for the message, if any.

   Alludium Brain shares the attachments together with their email if it shares the email, and they
   stay private with it otherwise.
6. **Slack threads.** Only when the task prompt lists `Slack channels:` (`none`, or no line,
   means skip this step). Never file direct messages or group DMs unless the task prompt says
   `Include direct messages: yes`. For each channel listed, read its messages in the window with
   the Slack connector. Keep a thread (a message and its replies) when any of its messages is in
   the window and it is about a company, founder, co-investor, LP or deal the firm deals with, or
   records a firm decision; skip social chat, stand-ups, and threads with only bots or channel
   events. A message with no replies counts as a thread of one. For each thread kept, read the
   whole thread (the parent and every reply, including those before the window) and call
   `capture` with:
   - `kind: "thread"`, `title`: `#channel: ` and the parent message's first words (up to 80
     characters), `occurred_at`: the parent message's time, `system: "slack"`, `external_id`:
     `<channel ID>/<parent message timestamp>` (for example `C0123ABC/1697270000.000100`),
     `url`: the parent message's permalink if the connector gave one;
   - `text`: these lines, a blank line, then one line per message in order, each message's text
     word for word (its further lines follow it). Mark a bot's or app's messages with `(bot)`
     after its name. Leave reactions and link previews as the connector gave them: Alludium Brain sets
     them aside, and joins and leaves too.

     ```text
     Workspace: workspace name
     Channel: #channel-name (public)
     [YYYY-MM-DD HH:MM] Display Name: the message, word for word
     ```

     Write `(private)` for a private channel, and `Channel: direct message` or
     `Channel: group DM` for direct messages;
   - `entities`: each person who wrote in the thread as a person with `attendee: true` and
     `{"system": "email", "external_id": "<email>"}` when their Slack profile gives an email,
     and the company the thread is about, resolved once by `search` on its name and reused. If
     the company is unclear, link only the people;
   - `follow_ups`: the thread's commitments, as for email.

   A thread filed last night that has new replies is filed again whole: Alludium Brain stores it as a
   new version, and a thread with nothing new said is `Already captured`.
7. **Finish** with one short table: source (meetings, calendar events, email, attachments,
   threads), found, filed, already there, skipped, truncated, failed, follow-ups. Then the run
   ID, and one line on anything that went wrong.
