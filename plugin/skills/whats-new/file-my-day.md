# Nightly filing run (file my day)

A scheduled task runs this with nobody watching. Copy the day's meetings, outside calendar
events and deal email from the user's own connectors into Alludium Brain with `capture`. Your job is
a faithful copy with source IDs, plus the commitments each record makes (`follow_ups`). You pass
no facts: Alludium Brain extracts the figures, roles and people from each email and meeting on the
server, with exact quotes, links them to the firm's entities, and recognises copies of the same
email or meeting from other tools.

## Rules

- **No questions.** Nobody will answer. When something is unclear (which company, whether an
  email is deal email), skip that record and count it as skipped.
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
- Do not repeat captured text in your messages, and do not read attachments: only upload them
  (step 5).
- If a connector is missing or fails, skip it, carry on with the others, and say so at the end.

## Run

1. **Window**: from the task prompt; default from 00:00 yesterday in the user's time zone. A
   window by date works even when you cannot tell the time, and the overlap with last night's
   run is safe. Keep only records that started or were sent inside the window, checking each
   one's own start time or date, because some connectors ignore a date filter. The firm's email
   domain is the user's own email domain. Set the run ID now. Call `configure` with `me: {}`
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
4. **Deal email.** Search the mail connector for messages in the window, leaving out
   promotions, social and forum categories. Keep a message only if at least one sender or
   recipient is outside the firm's domain and it is about a company, founder, co-investor or LP
   the firm deals with. Skip newsletters, receipts, notifications, automated senders (no-reply),
   recruiting and personal mail; when in doubt, skip. Also skip automatic replies,
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

   Upload a message's deal documents (step 5) **before** capturing the message.
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
6. **Finish** with one short table: source (meetings, calendar events, email, attachments),
   found, filed, already there, skipped, truncated, failed, follow-ups. Then the run ID, and
   one line on anything that went wrong.
