---
name: capture-meeting
description: File a meeting's notes into the firm's VC Brain word for word, with the meeting's source IDs from the notes connector (Granola, Fireflies, Otter, Fathom, Zoom, Teams or Google Meet). Use after a call when the user says "file this meeting", "capture my call with …", "save today's meeting notes to the brain", or pastes meeting notes to keep. Also use it to offer, never silently, when the user shares or discusses a meeting's notes without asking to file them.
---

# Capture a meeting

You copy one meeting's notes from the user's own notes connector into VC Brain with the
connector's `capture` tool. VC Brain links the meeting to the firm's entities and recognises
copies of it from other tools. Your job is a faithful copy with its source IDs and the figures
it states.

## Rules

- **Word for word.** Pass the notes exactly as the connector returned them. Do not summarise,
  shorten, reorder, reformat, fix typos or add your own commentary. If the connector says it
  returned less than the full text, capture what you have with `connector_truncated: true`
  and tell the user it was truncated.
- **Source IDs on every capture.** Set `system` (`granola`, `fireflies`, `otter`, `fathom`,
  `zoom`, `teams`, `google_meet`), `external_id` (the meeting or note ID exactly as the
  connector gave it) and `url` (the link to the notes, if the connector gave one). Never invent
  or guess an ID or a link.
- **One capture per meeting.** Several meetings mean several captures.
- **Offer, don't file silently.** If the user shared or discussed the notes without asking to
  file them, offer once in one line ("File these meeting notes in VC Brain, private to you?")
  and file only after a yes. Offer once per meeting; if they decline, drop it. Never offer for a
  meeting that came from the brain or is already in it.
- **Do not repeat the notes** in your messages. They are stored; repeating them costs tokens.

## Steps

1. Find the meeting in the notes connector: the one the user named, or their most recent
   meeting. If several could match, list them (title and start time only) and ask which.
2. Fetch the full notes: the generated summary and the user's own notes. Fetch the transcript
   only if the user asks for it, and capture it separately with the same `url` and
   `external_id` plus `/transcript`.
3. If the notes connector gave no attendees, look the event up in the calendar connector, if
   there is one, for names and emails. When the notes connector or the calendar names the
   calendar event, keep its iCal UID and start time: VC Brain uses them to know that the
   calendar event, these notes, a transcript and a CRM note are one meeting.
4. Build `text` as these header lines, copied from the connector's fields, then a blank line,
   then the notes exactly as returned:

   ```text
   Title: meeting title
   Date: start–end (time zone)
   Attendees: Name (email), Name (email), …
   ```

   Leave out a header line whose value the connector did not give.
5. Build `entities`:
   - every attendee as `{"type": "person", "name": "<Name>", "attendee": true,
     "external_refs": [{"system": "email", "external_id": "<email>"}]}`, including colleagues,
     because that is how VC Brain knows who at the firm met them. People the notes only
     mention are not attendees; leave them out.
   - the company the meeting was with. `search` the external attendees' email domain (unless
     it is webmail such as gmail.com), or the company name if there is no domain, and pass the
     match as `{"type": "organization", "name": "<exact name>", "id": "<org_…>"}`. If nothing
     matches, pass the name with `{"system": "domain", "external_id": "<domain>"}`.
6. Build `facts` from figures the notes state about the company, and only those: for example
   ARR, paying customers, design partners, headcount, the round target. Use a key from the list
   in `capture`'s `facts` description, or one of the firm's custom fields (`configure` with no
   arguments lists them; check only if a figure fits no listed key). A figure that fits neither
   can go in under a short snake_case key; it is stored but kept apart, so use a listed key
   whenever one fits. Each fact: `entity_name` (the company's exact name), `key`, `value`
   as stated, `as_of` (the date it is true at if the notes say, else the meeting date) and
   `label: "user_reported"`; `basis: "projected"` for a forecast, plan or target; and
   `stated_by` (their email) when someone outside the company gave the figure, such as a
   co-investor. Never compute or round a figure. A person's job goes in `relations` as
   `works_at` with their `title` as stated (and `valid_from` if the notes date it).
7. Build `follow_ups` from the commitments the notes record, as **Follow-ups** below says.
8. Call `capture` with `kind: "meeting"`, `title`, `text`, `occurred_at` (the meeting's start,
   ISO with its offset), `system`, `external_id`, `url`, `entities`, `facts` and `follow_ups`, and
   `refs: [{"system": "ical", "external_id": "<iCal UID>"}]` when you have the event's UID
   (with the event's start as `occurred_at`). A transcript captured separately gets the same
   `refs` and `occurred_at`. The UID identifies a meeting only together with its start: a
   recurring meeting shares one UID. Meetings
   default to the firm scope when the user asked to file them. Use `scope: "private"` if the user
   asks, or if you offered to file it, and then offer to share it in your reply.
9. Reply in one or two lines: the meeting title, the source ID, the scope, the entities it was
   linked to, any facts recorded or skipped, and the follow-ups recorded (each is private to its
   owner). If the result says it was already captured,
   say it was already in the brain; if it lists a related source (`same event`, `notes of`,
   `duplicate of`), say the meeting was already in the brain from another tool and is now
   linked to it.

## Follow-ups

`follow_ups` lists the concrete commitments the text records. VC Brain shows each one to its
owner only, in their morning digest and on the company's page, until it is done. A list of
false to-dos gets ignored, so precision matters more than completeness: most meetings have one
to three, many emails have none, and when unsure leave it out.

Include:

- **commitment**: a firm member agreed to do a specific thing. "Priya to request the cohort
  table", "I'll send Jane the term sheet by Friday", a "Next steps" or "Actions" line that names
  a firm member. `owner`: that member's email; leave `owner` out when it is the user.
- **waiting_on**: someone outside the firm agreed to give a firm member something specific.
  "Maya will send exact figures", "Owen to circulate the final Q3 update by the end of October",
  "I'll share an update once the quarter closes". `owner`: the firm member it was promised to
  (the user when it is unclear); `counterparty`: who owes it.

Leave out:

- vague intentions and pleasantries: "stay in touch", "we should think about…", "happy to
  help", "possible intro later", "would be glad to keep you updated";
- next steps that name no one to do them ("Partner meeting once the deck is ready", "IC on 14
  October"), and conditional ones ("follow up when they convert", "look again if growth
  re-accelerates");
- what is already done ("attached", "as promised, here is"), requests nobody has agreed to yet
  ("could you send…?"), meetings already scheduled, and a company's own plans (its hiring,
  roadmap, fundraising or targets);
- anything promised between people outside the firm.

Each follow-up: `action` (a short imperative naming who it is for: "Send Maya the draft term
sheet"), `quote` (the line it comes from, copied exactly from `text`; without it nothing is
stored), `kind`, `owner`, `counterparty` (the person or company as named), `about` (the company
or deal, by the exact name you passed in `entities`) and `due_on` only when the text states a
date or deadline ("by Friday" is that Friday, worked out from the meeting's or email's date).
One follow-up per commitment, even when the notes repeat it.

If there is no notes connector and the user pasted the notes, capture the pasted text with
`kind: "meeting"` and no source IDs, and say that it has no link back to a notes system.
