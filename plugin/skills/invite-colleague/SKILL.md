---
name: invite-colleague
description: Invite a colleague to Alludium Brain or resend their welcome email. Use when a member asks to bring someone into their workspace, give a colleague access, or send their setup links again.
---

# Invite a colleague

Any active member can invite colleagues. This grants ordinary member access and sends an email
with two routes: sign in to the app, or choose an AI and copy the current setup prompt.

1. Use the chat's current workspace_context. If none is established, read `configure(account={})`
   and verify the intended workspace. Never invite into a workspace inferred from an email domain.
2. Get the person's work email and, if known, their name. When given only a name, first read
   `configure()` to look up the existing team. Reuse its confirmed email for an unambiguous
   colleague. Ask only if that lookup leaves the person or address missing or ambiguous; never guess an
   email from a name or website. Researching or listing a team is not permission to invite them.
3. When the user asks to invite that person, call `invite_colleague(email=..., name=...)`. Do not
   merely save `configure(members=...)`: that records the roster without granting access.
4. Say whether the invitation email was sent. If access was added but the email failed, say both
   and offer to retry the same action. Sending again preserves existing roles and is allowed after
   first sign-in too. If deactivation blocks the invite, stop. Only a firm admin can restore access,
   even when the firm has no admin configured. Do not offer an ordinary member a configure call or
   another workaround; offer Alludium help if there is no admin.

For several explicitly requested colleagues, report each outcome; do not repeat successful sends
when retrying failed ones. Do not claim inbox delivery, acceptance or setup completion from a sent
email. No domain restriction is enforced yet; ask for work email without inventing a blocking policy.
