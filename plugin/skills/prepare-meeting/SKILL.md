---
name: prepare-meeting
description: Prepare a cited brief for an upcoming meeting from the user's calendar and the firm's Alludium Brain - who is attending, what the firm knows about them and their company, colleagues' notes and open questions. Use when the user says "prep me for my call with …", "brief me for tomorrow's meeting", "prepare for the Acme meeting" or asks what to know before a meeting.
---

# Prepare for a meeting: the firm's own skill

What a firm wants before a meeting is the firm's, so this is now a firm skill kept in Alludium
Brain. Every firm starts with Alludium's version and can change it for the firm, or for one person.

1. Load it with the Alludium Brain connector: `configure(skill="prepare-meeting")`, then follow
   what it returns, including the frame it comes in.
2. If `configure` says the firm has no skill called `prepare-meeting` (it was retired or renamed),
   tell the user and ask which of the firm's skills listed in `configure`'s description to use
   instead. Do not prepare the brief from memory of an older version of this skill.
