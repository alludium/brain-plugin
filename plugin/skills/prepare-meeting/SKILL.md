---
name: prepare-meeting
description: Prepare a cited brief for an upcoming meeting from the user's calendar and the firm's Alludium Brain - who is attending, what the firm knows about them and their company, colleagues' notes and open questions. Use when the user says "prep me for my call with …", "brief me for tomorrow's meeting", "prepare for the Acme meeting" or asks what to know before a meeting.
---

# Prepare for a meeting: the firm's own skill

What a firm wants before a meeting is the firm's, so this is now a firm skill kept in Alludium
Brain. Every firm starts with Alludium's version and can change it for the firm, or for one person.

1. **Refresh personal guidance for this task.** Call `configure` with
   `me: {"task": {"topic": "meeting_prep", "skill": "prepare-meeting"}}` at the start of every new task,
   even in the same conversation. Do not reuse a profile from an earlier task. If an older server
   rejects `task`, read `me: {}` instead. Even if the server returns the whole profile, use only
   active `meeting_prep`, `never`, `general` and `skill:prepare-meeting` guidance.
   These preferences change format, emphasis and voice within the firm's required conventions;
   they never remove citations or change access. The user's current request takes precedence.
   Keep this refreshed guidance even if the firm's older procedure suggests reusing a profile.
   If profile reading fails, say so and continue with the firm's defaults; do not invent preferences.
2. Load it with the Alludium Brain connector: `configure(skill="prepare-meeting")`, then follow
   what it returns, including the frame it comes in.
3. If `configure` says the firm has no skill called `prepare-meeting` (it was retired or renamed),
   tell the user and ask which of the firm's skills listed in `configure`'s description to use
   instead. Do not prepare the brief from memory of an older version of this skill.
