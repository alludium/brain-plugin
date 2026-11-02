---
name: get-help
description: 'Ask Alludium for help, report a problem with Alludium Brain, or check on a request already made. Use when the user says "report this to Alludium", "this isn''t working", "ask Alludium", "I have an idea for the brain", "something''s wrong with my upload", "any news on my support request?" or "S-31", or after a brain tool error the user wants looked at. Raises a support request with the user''s own words and only technical details, never firm content.'
---

# Get help from Alludium

A support request goes to the people who run Alludium Brain. It is raised with the Alludium Brain
connector's `follow_ups` tool, as a task asked of Alludium; there is no separate support tool.

## Raise a request

1. Work out what the user needs in their words: what they were doing, what happened, and anything
   urgent ("before IC on Thursday"). If they only said "report this", ask one short question for
   what they expected instead.
2. Choose its kind: `problem` (something is wrong, the default), `question` (how do I…), `idea`, or
   `account` (plan, people, access).
3. If a brain tool error came back, it carries a reference like `err_1a2b3c4d`. Quote every reference
   the user wants looked at.
4. Show the user what will be sent: a one-line title, their words, the kind and the references.
   Say that only technical details go with it (their assistant and its version, the references,
   the IDs of jobs that failed today), and no firm content. Send it only after they say yes.
5. Call `follow_ups` with `ask: {to: "alludium", support: <kind>, action: <title>, why: <their words>,
   references: [<err_…>]}`.
6. Tell them the reference it returns (S-n), that Alludium usually replies within a working day, and
   that the answer shows in what's new, in their follow-ups and by email.

Never include document text, notes, names of companies or people from the brain, or anything the
user did not write for this request. If they want Alludium to see something specific, they say so
in their own words.

## Check on a request

- "Any news on S-31?": call `follow_ups` with `task: "S-31"` and give the latest message from
  Alludium, or say it is still with Alludium.
- "What have I asked Alludium?": call `follow_ups` with `view: "asked"`; open support requests are
  listed at the end.

Firm admins see every request from their firm; everyone else sees their own.
