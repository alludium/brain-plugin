# Researching the firm

Public sources first, then the user's own connected data tools. Nothing here reads the user's
email, CRM records, files or meeting notes: those come later, and only with their go-ahead.

## Tools

- **Web**: whatever web search and fetch tools the host gives you (web search, web fetch,
  browsing). Read pages as they come; never sign in, never get round a paywall or a cookie wall,
  and fetch one page at a time rather than crawling a site.
- **Connected data tools** (only those the user already has; never ask them to sign up for one):
  a data provider's connector such as Harmonic, a Crunchbase-style connector, or the CRM's
  company enrichment (Affinity's company lookup). Look up the firm itself and the portfolio
  companies you found. Match tools by the name after the host's prefix
  (`mcp__<connector>__harmonic_lookup_company` is Harmonic's `lookup_company`).

Budget: about 15 page fetches and 10 connector lookups. Stop when the sections below are covered.

## Order of trust

1. The firm's own site: home, about, team and bios, focus or thesis, portfolio, news, any "for
   founders" page (stages, cheque, regions, how they decide).
2. The firm's own announcements: fund close press releases, thesis posts.
3. Public filings and registers: SEC Form D, Companies House, the FCA register, a
   Handelsregister. Authoritative for fund names, often for sizes.
4. Press and trade coverage: fund closes, new partners, rounds they led.
5. Public profile pages (Crunchbase, PitchBook, Dealroom, LinkedIn): only what shows without
   signing in.
6. The user's data connectors.

When two disagree, prefer the higher one and show both, each with its date. A page about a
different firm with a similar name is not evidence: check the domain, the city and the people.

## What to look for

| Section | Look for |
|---|---|
| Thesis | the firm's own one-sentence statement; funding stages; sectors and themes in and out of scope; regions; first cheque range and currency, when one range covers every fund |
| Funds | names, vintages, sizes and currency, each fund's own first cheque when ranges or currencies differ, strategy line |
| Team | names, titles, focus areas from bios. No emails unless the firm publishes them |
| Portfolio | company names and domains; current or exited, as the page says |
| Process | rarely public: only what a founders page says ("a decision within four weeks") |
| Tags | sectors and themes from the portfolio filters or the focus page |

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
- `entities`: what the page names: the firm's funds (`type: "fund"`), the team members (people,
  with `external_refs` of their emails only once confirmed), the portfolio companies
  (organizations with their domain in `external_refs`, and `status: "portfolio"` or `"exited"`
  only for the companies the partner confirmed). Never the firm itself as an organization.
- No `facts`: the configuration holds the thesis and funds; the server extracts figures from
  the text where it needs them.

The same URL captured again later with changed text is stored as a new version, so a re-run
refreshes it. Cite the `source_id` each capture returns, with the exact words from its `text`.
