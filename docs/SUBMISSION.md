# Devpost submission pack — ARC Séance (Kiroween 2026)

Fill the Devpost "Enter a Submission" form from this file. Do not
retype: copy each field verbatim. (Repo URL and demo URL are filled
in by the submitter once GitHub and YouTube links exist; everything
else below is final.)

## Project title

ARC Séance

## Category

Frankenstein

## Tagline (one line)

A haunted terminal that stitches BBS door games, IRC, and RSS into
one working chimera — summoned by one command.

## Description

ARC Séance is a retro-terminal agent command center that resurrects
three dead technologies in a single app. Open the CRT terminal in a
browser and you can play "The Haunted Keep", a real BBS door game
with four rooms, three items, a locked crypt, and a win condition;
chat in #seance, an IRC-style channel where three bot spirits —
Madame Zara, Captain Byte, and Professor Patch — answer by keyword
alongside visitor messages; and read an RSS ticker fed by a real
public feed, fetched by script with its source and date recorded.
One command, `seance <topic>`, stitches all three together into a
briefing: a door-game hint, a spirit quote, and a ticker headline,
with an honest "loose match" note when no headline matches.

A Python twin offers the same three features in a terminal, plus a
real stdlib IRC protocol client (optional, graceful offline) and the
real RSS fetcher. Everything runs at $0: no API key, no account, no
payment, no backend. Open index.html, or run `python3 seance.py
--help`. Tests: 13 Python unit tests passing, web script syntax
checked, MCP server smoke-tested over stdio JSON-RPC.

Problem solved: dead tools are usually demoed as museum pieces or
not at all. ARC Séance makes them playable again, together, in a way
a judge can run in five minutes with nothing to install beyond a
browser or Python 3.

## Built with

Kiro (specs, steering, hooks, custom agent, MCP), HTML, CSS,
JavaScript, Python 3 standard library only.

## Links (fill in at submit time)

- GitHub repo (public, MIT license, /.kiro at root, not gitignored):
  [REPO URL]
- Demo video (public YouTube, under 3 minutes): [DEMO URL]
- Functional app URL: the repo itself — open index.html, or run the
  Python twin. No login, no credentials needed for judges.

## Kiro-usage write-up

See docs/KIRO-USAGE.md in the repo, and paste its full text into the
form's Kiro-usage field. It is honest about what Kiro's AI did not do in this session
(CLI chat needs an interactive/device-flow Builder ID sign-in that
could not run headlessly) and about the one step that would close
that gap. Do not paraphrase it into a stronger claim.

## Testing instructions for judges

1. Open `index.html` in any modern browser.
2. Type `help`, then `play`, `look`, `take candle`, `go north`,
   `take key`, `go east`, `take grimoire`, `go west`, `go north` —
   the crypt glows and you win.
3. Type `say hello` for a spirit reply, `rss` for the ticker, and
   `seance candle` for the stitched briefing.
4. Or, in a terminal: `python3 -m unittest discover -s tests -v`
   and `python3 seance.py summon candle`.

## Disclosures

- All project code was written Oct 30, 2026 or later, inside the
  submission period. Concept notes from before Oct 30 were planning
  only; no pre-period project code is included.
- Pre-existing resources used: standard libraries only, plus one
  public RSS feed (NASA breaking news) fetched by script, with
  source recorded in data/ticker.json. No other pre-existing code.
- Kiro account on file: AWS Builder ID arc-agent-ops@proton.me,
  free plan. Kiro user ID (for the credit request form, if used):
  d-9067642ac7.c4c8c4c8-3041-7028-2361-d1c65cab1816.
- Credit request: one-time 4,000 Kiro credits are available by
  request before Dec 1, 2026, 12:00 PM PT, via the official credit
  request form. Requesting them needs the form action; it is not
  required for this submission to run.
- No social post is included in this submission. No bonus prize
  requiring a social post or a blog post is claimed.
