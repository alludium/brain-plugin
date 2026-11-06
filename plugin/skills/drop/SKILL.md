---
name: drop
description: Upload files (pitch decks, data-room documents, memos, spreadsheets) to the firm's Alludium Brain without reading them. Use when the user attaches or points to files and says to drop, file, add or upload them to the brain, for example "drop this deck into the brain" or "file the Acme data room". Also uploads the firm's Word reference document (reference.docx) that styles Word exports. Also use it to offer, never silently, when the user shares a deck or document without asking to file it.
---

For a user choosing a local file in chat, call `request_upload(interactive=true)` first. The Add
Source card shows their signed-in firm and name, lets them choose Only me or Whole firm,
and transfers the original directly from their computer. It does not need a code sandbox
or a desktop extension. The card follows processing and offers View source. Do not report a
completed upload until processing is done. If the host cannot display the card, offer the
browser Add Source link returned by the tool. For task outcomes, revisions, provenance or
explicit entity links, use the existing script flow below so that context is preserved; do not
silently replace it with an ordinary picker upload. Never request or display a card's transfer
token. If sign-in changed, open a fresh card so the user can see the current firm and identity.


# Drop files into Alludium Brain

The files go straight from this machine or sandbox to Alludium Brain storage through upload URLs.
Alludium Brain extracts and indexes them afterwards, so you never need their content.

## Rules

- **Do not read the files.** Do not open, view, preview, `cat`, extract text from or summarise
  them, and do not use a file-reading tool on them. Work only with the script's output: names,
  types, sizes and hashes.
- **Offer, don't file silently.** If the user shared a file without asking to file it, offer
  once in one line ("Drop this deck into Alludium Brain, private to you?") and upload only after a
  yes. Offer once per file; if they decline, drop it. Never offer for a file that came from the
  brain or that `request_upload` says the brain already has.
- Upload only what the user asked for. If it is unclear which files they mean, list them and ask.
- **Source IDs.** If a file came from another system (a Gmail attachment, a Drive or SharePoint
  file), pass that system's `system`, `external_id` and `url` to `request_upload`: `gdrive` for a
  Google Drive file, `sharepoint_file` for SharePoint or OneDrive, `gmail` for an attachment.
  Never pass `google_drive` or `sharepoint`: those belong to drives the firm connects to the brain
  and are refused. Files attached to this chat or on local disk have none; leave them out. Never
  invent them.
- **Original dates.** When the source system provides the file's date, pass it as `occurred_at`
  on that file (an ISO timestamp with its timezone). For Affinity, use the entity file's
  `created_at`: when it was added to Affinity, not a date guessed from its name or contents.
  Leave it out when unknown; never use the download time or local file modification time.
  The brain keeps its import time separately. A repeated upload keeps the stored date and warns
  if the supplied date differs; report that warning rather than claiming the date was corrected.
- Do not print upload URLs back to the user.

The script is at `${CLAUDE_SKILL_DIR}/scripts/upload.py`. If that path was not filled in, it is
`scripts/upload.py` next to this SKILL.md. It uses only the Python standard library.

## Steps

1. If the user did not give paths, list the attached files (names and sizes only):

   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/upload.py" --list
   ```

   Pass a directory to look elsewhere: `--list /path/to/dir`.
2. Hash and type the files (a file or a directory; prints one JSON line per file):

   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/upload.py" --prepare <file or directory> ...
   ```

   Still PNG, JPEG and WebP images are supported (up to 20 megapixels); animated images are not.
   Tell the user about any `SKIP` lines (unsupported types such as zip files or legacy Office files).
3. Call the Alludium Brain connector's `request_upload` once, with `files`: one entry per file,
   with `filename`, `content_type` and `sha256` copied exactly from its line (up to 50 files a
   call). Add `entities` to an entry if the user said who that file is about. Resolve all the
   names first in one `search` call with `query: ""` and `queries` (one `{"name": …}` row per
   company), then pass `{"type": "organization", "name": "<exact name>", "id": "<org_…>"}`.
   Add `doc_type` to an entry when the user said what the file is ("Acme's board pack" →
   `board_pack`, "the financial model" → `financials`; at a venture firm, "our LPA" → `lpa`,
   "the IC charter" → `investment_process`, "Acme's term sheet" → `term_sheet`), and `hints` with
   the folder path when the files come from a folder. Otherwise the brain works out the type. The
   types come from the firm's packs: if a type is refused, the error lists the firm's types; pick
   the one that fits, or leave `doc_type` out.
   When the user says a file is a new version of one already in the brain ("the revised Acme
   memo", "v3 of the LP letter"), find the earlier one (`search`), confirm it in one line, and add
   `revision_of: "<src_…>"` to that entry: the earlier version's comments follow to the new one.
   A Word file's own comments (and replies, and done) come in as comments on it, under their Word
   authors' names; say so in your report when the user mentions them.
   Add `scope: "private"` (for the whole call) if the user asked, or if you offered the drop
   yourself; then offer to share the files in your report (`share` with each source ID and the
   scope the user chooses). When the user names who should see them, pass `scope: "people"` with
   `people`, or `scope: "group"` with `group`. Without
   a scope, fund documents (LPA, side letter, subscription booklet, administrator's statement)
   stay private to the user, and every file is private until the brain has read what it is; tell
   them, and that `share` shows one to the firm. Each upload in the
   result has an `upload_url`, `upload_headers` and a `job_id`; if it says no upload is needed,
   the brain already has that file. If your host exposes only text, read the JSON transfer plan
   in that text: it contains the same exact URLs, headers and job IDs as the structured result.
   Never reconstruct a signed URL or replace it with the field name `upload_url`.
4. Check that this machine can reach the upload host, using any one `upload_url`:

   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/upload.py" --check "<upload_url>"
   ```

   If it prints `EGRESS FAIL`, stop and offer the fallback (below), quoting the `EGRESS FAIL`
   line.
5. Write the upload plan to a file named `vcbrain-upload-plan.json`, in a scratch or temporary
   directory if you have one, else the working directory. Use your file-writing tool, not a
   shell heredoc (Claude Code's shell check rejects JSON heredocs). One entry per file that
   needs uploading:

   ```json
   [{"path": "<path from step 2>", "upload_url": "<upload_url>", "upload_headers": {"Content-Type": "<type>"}}]
   ```

   Then upload them all in one call. The script deletes the plan when it finishes:

   ```bash
   python3 "${CLAUDE_SKILL_DIR}/scripts/upload.py" --put <path to vcbrain-upload-plan.json>
   ```

   Copy each `upload_url` exactly; they are signed and expire after about 15 minutes. If the
   script reports `FAIL … expired`, call `request_upload` again for those files. If files fail
   for another reason (the host cannot be reached, a proxy or network refusal), offer the
   fallback for those files, quoting one `FAIL` line.
6. Call `job_status` with the job IDs. If any job is still `waiting_for_upload` or
   `processing`, wait about ten seconds and check again, up to four times. Then stop waiting.
7. Report, from the script's summary and `job_status`: how many files were uploaded, which jobs
   are done, each file's type (its `Type:` line), any failures or warnings (for example "no
   text layer, OCR needed", or one kept private), and each file as its link from `job_status`
   (never its source ID). Do not describe what the
   files contain: you have not read them.
8. If a job's `Type:` line says the brain is not sure, ask the user what that file is, using the
   types it suggests. When they answer, call `request_upload` with only that file's `source_id`
   and the `doc_type` they gave; nothing is uploaded or created.

## The firm's Word reference document

When the user gives a `.docx` to style the firm's Word exports ("use this as our Word template",
"our reference.docx", "make exported memos look like this"), it is configuration, not a document
to file: its styles, page setup, header, footer and logo dress every draft exported to Word. Do
steps 1 and 2 for that one file, then call `request_upload` with `asset: "reference_docx"` and
the single-file fields (`filename`, `content_type`, `sha256`), no `files`, scope or entities. It
replaces the firm's current one for everyone, so say so first. If the result has an
`upload_url`, do steps 4 and 5 for it; there is no job to follow. Report that exports now use it.

## Fallback when the upload cannot get through

This sandbox cannot reach Alludium Brain's storage, so the files never left. Offer these options in order:

1. **Add Source in chat.** For an ordinary upload (the result includes `browser_upload_url`),
   call `request_upload(interactive=true)` and ask the user to select the original. The card
   transfers from their computer, without the sandbox. Follow its processing receipt, not
   the earlier untransferred job. If the card is unavailable, offer `browser_upload_url`.
   The user signs in to the same firm, selects the original file and explicitly chooses its
   audience. It supports one ordinary document at a time, up to 25 MiB. Follow the browser's
   receipt/source afterwards, not the earlier job that never received bytes. This page does
   not preserve original dates, task-outcome links, external-system provenance or reference-document settings;
   do not substitute it for those operations. Never describe the file as uploaded until the
   browser confirms receipt, or as indexed until processing finishes.
2. **Email them in.** Call `configure` with no arguments. If it gives an email-in address, tell
   the user they can send or forward the files as attachments from their own firm address to
   it (to file them under a deal, the `+<deal-name>` form it shows). Say that anything sent
   there is shared with the whole firm, so it is not a way to file something privately. If
   `configure` gives no address, say the firm has none set up yet and go to 3. Skip this option
   for imports carrying original dates or external-system provenance: email-in cannot preserve
   that metadata. Resolve the transfer restriction and retry the original upload instead.
3. **Allow the upload host, where supported.** On Team/Enterprise an org owner can allow the host from the `EGRESS FAIL` or `FAIL`
   line under Organization settings → Capabilities → Code execution → network egress. Then run
   the drop again. The personal-plan package-manager toggle alone does not promise access to this host.

The jobs from `request_upload` wait for the files for about an hour, then fail; nothing else
needs undoing.
