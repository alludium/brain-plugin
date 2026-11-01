---
name: ic-prep
description: Draft an investment committee (IC) memo for a deal from what the firm's Alludium Brain knows, under the firm's own memo headings, with every claim cited. Use when the user says "draft the IC memo for Acme", "prep Acme for IC", "write up Ferrolith for the partner meeting" or "start an investment memo on Kestrel".
---

# Draft an IC memo: the firm's own skill

How a firm writes an IC memo is the firm's, so this is now a firm skill kept in Alludium Brain. Every firm
starts with Alludium's version and can change it for the firm, or for one person.

1. Load it with the Alludium Brain connector: `configure(skill="ic-prep")`, then follow what it returns,
   including the frame it comes in.
2. If `configure` says the firm has no skill called `ic-prep` (it was retired or renamed), tell the
   user and ask which of the firm's skills listed in `configure`'s description to use instead.
   Do not draft the memo from memory of an older version of this skill.
