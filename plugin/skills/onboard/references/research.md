# Researching the firm

Public sources first, then the user's own connected data tools. Nothing here reads the user's
email, CRM records, files or meeting notes: those come later, and only with their go-ahead.

## Tools

- **Web**: whatever web search and fetch tools the host gives you (web search, web fetch,
  browsing). Read pages as they come; never sign in, never get round a paywall or a cookie wall,
  and fetch one page at a time rather than crawling a site.
- **Connected data tools** (only those the user already has; never ask them to sign up for one):
  a data provider's connector such as Harmonic, a Crunchbase-style connector, or the CRM's
  company enrichment (Affinity's company lookup). Look up the firm itself and the organisations
  its pages name (a portfolio, customers). Match tools by the name after the host's prefix
  (`mcp__<connector>__harmonic_lookup_company` is Harmonic's `lookup_company`).

Budget: about 15 page fetches and 10 connector lookups. Stop when the sections below are covered.

## Order of trust

1. The firm's own site: home, about, team and bios, news, and the pages each Setup section's
   **Look for** names.
2. The firm's own announcements and posts.
3. Public filings and registers (Companies House, a Handelsregister, a regulator's register),
   where a Setup section says they are authoritative.
4. Press and trade coverage: new people, announcements about the firm.
5. Public profile pages (Crunchbase, PitchBook, Dealroom, LinkedIn): only what shows without
   signing in.
6. The user's data connectors.

When two disagree, prefer the higher one and show both, each with its date. A page about a
different firm with a similar name is not evidence: check the domain, the city and the people.

## What to look for

Each Setup section in the onboarding report says what to look for and where (its **Look for**
line), in the words of the firm's pack. Besides those:

| Section | Look for |
|---|---|
| Team | names, titles, focus areas from bios. No emails unless the firm publishes them |
| Tags | themes and sectors from the firm's focus pages and the filters on its lists of organisations |

## Each item needs

- the exact words it rests on (one sentence or a table row, under 300 characters), copied from
  the page or record as fetched;
- the URL (or the connector record's ID and link);
- the page's date when it shows one (a press release's date, "updated").

No quote, no item. Never round or convert a figure; give it as the page does.

## Storing what the partner confirmed

One `capture` per page or record you used, after the partner has confirmed the firm and the
section it supports, and before the `configure` call that cites it:

- **A web page:** `kind: "document"`, `system: "web"`, `external_id` and `url`: the page's URL
  without tracking parameters or a `#` part, `title`: the page's title, `occurred_at`: the
  page's date if it shows one, `scope: "firm"`, `connector_truncated: true`, and `text`: the
  passages you used, word for word, each under the heading it sat under, in page order (not the
  whole page, not your summary).
- **A data connector's record:** `kind: "external_record"`, `system`: the connector
  (`harmonic`, `crunchbase`, `affinity`), `external_id`: its record ID as the connector gave it
  (prefixed by its type, `company:` or `person:`, as `import-from-crm` does), `url`: the
  record's link if it gave one, `scope: "firm"`, `text`: the fields you used as `Field: value`
  lines, word for word.
- `entities`: what the page names: the team members (people, with `external_refs` of their
  emails only once confirmed), and the organisations it lists (with their domain in
  `external_refs`, and a `status` from a `status:…` Setup section only for those the partner
  confirmed). A section that fills `funds` makes funds Fund entities through `configure`; do not
  capture them as organisations. Never the firm itself as an organization.
- No `facts`: the configuration holds what the Setup sections fill; the server extracts figures
  from the text where it needs them.

The same URL captured again later with changed text is stored as a new version, so a re-run
refreshes it. Cite the `source_id` each capture returns, with the exact words from its `text`.
