---
name: ic-prep
description: Draft an investment committee (IC) memo for a deal from what the firm's Alludium Brain knows, under the firm's own memo headings, with every claim cited. Use when the user says "draft the IC memo for Acme", "prep Acme for IC", "write up Ferrolith for the partner meeting" or "start an investment memo on Kestrel".
---

# Draft an IC memo: the firm's own skill

How a firm writes an IC memo is the firm's, so this is now a firm skill kept in Alludium Brain. Every firm
starts with Alludium's version and can change it for the firm, or for one person.

1. **Refresh personal guidance for this task.** Call `configure` with
   `me: {"task": {"topic": "writing", "skill": "ic-prep"}}` at the start of every new task,
   even in the same conversation. Do not reuse a profile from an earlier task. If an older server
   rejects `task`, read `me: {}` instead. Even if the server returns the whole profile, use only
   active `writing`, `never`, `general` and `skill:ic-prep` guidance. Use only the approved writing
   style, never a pending one.
   These preferences change format, emphasis and voice within the firm's required conventions;
   they never remove citations or change access. The user's current request takes precedence.
   Keep this refreshed guidance even if the firm's older procedure suggests reusing a profile.
   If profile reading fails, say so and continue with the firm's defaults; do not invent preferences.
2. Load it with the Alludium Brain connector: `configure(skill="ic-prep")`, then follow what it returns,
   including the frame it comes in.
3. If `configure` says the firm has no skill called `ic-prep` (it was retired or renamed), tell the
   user and ask which of the firm's skills listed in `configure`'s description to use instead.
   Do not draft the memo from memory of an older version of this skill.
