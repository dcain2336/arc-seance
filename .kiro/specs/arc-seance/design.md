# ARC Séance — Design

> Written Oct 30, 2026, from requirements.md, before implementation.

## Overview

One chimera, two faces, same three organs:

- **Web face** (`index.html`, `style.css`, `app.js`): a CRT terminal in the
  browser. No build step, no framework, no network calls at runtime except
  loading the bundled ticker data file. This is the face judges see first.
- **Python face** (`seance.py`): a command line twin with the same door
  game, the same IRC channel simulation, and the real RSS fetcher and IRC
  client. This is the face judges run in a terminal.
- **Kiro layer** (`.kiro/`): the spec that drove the build, steering docs
  that set the voice and rules, hooks that automate checks, a custom agent,
  and an MCP server that exposes séance tools over stdio JSON-RPC.

## Components

### Terminal shell (web)

- A screen element that prints lines, and an input line that reads commands.
- A tiny parser: split the input into a command word and the rest as argument.
- A dispatcher: one function per command, each printing plain text lines.
- State held in one object: current room, inventory, score, channel log.

### Door game

- Rooms are data, not code: each room has a description, exits, and items.
- Moves check the exits table; illegal moves print a refusal, never crash.
- Items move from a room into inventory on `take`, once only.
- Win check runs after every move and take: candle + grimoire + crypt room.

### IRC channel

- The web channel is a log plus three spirits with keyword replies.
- Spirits are data: name, personality line, and keyword-to-reply pairs.
- The Python twin adds `irc_client.py`, a stdlib-only IRC protocol
  client: socket connect, NICK/USER registration, JOIN, PRIVMSG, PING
  reply, and a line parser covered by unit tests. It is optional; the
  local channel works with no network at all.

### RSS ticker

- `tools/rss_seance.py` fetches one public RSS feed with stdlib XML
  parsing, and writes `data/ticker.json` with source, fetched date, and
  items (title, link, published date).
- The web app loads `data/ticker.json` and prints it as a ticker strip.
- If the fetch fails, the script exits non-zero and leaves the last good
  file alone, so a bad fetch can never overwrite good data with nothing.
- A bundled sample is labelled as a sample in the file itself.

### Séance summon

- `seance <topic>` builds a briefing from three parts: a door-game hint
  chosen by topic keyword, a spirit quote chosen by topic keyword, and a
  ticker headline whose title contains a topic word, or the first headline
  with a "loose match" note. Deterministic: same topic, same ticker, same
  briefing.

### MCP server

- `mcp/seance_mcp.py` speaks stdio JSON-RPC in the MCP shape: it answers
  `initialize`, lists tools, and calls tools. Tools: `summon_spirit`,
  `door_game_move`, `read_ticker`, `irc_say`. All tools run locally with
  no network and no key.

## Data flow

- Visitor types a command -> parser -> dispatcher -> state changes ->
  lines printed on the CRT screen.
- Judge runs the fetcher -> public RSS feed -> `data/ticker.json` ->
  web ticker and Python ticker read the same file.
- Kiro-style client starts the MCP server -> stdio JSON-RPC -> tools
  answer from the same game/channel/ticker logic.

## Testing

- `tests/test_seance.py` (Python unittest, stdlib only) covers: room
  moves, item taking, win condition, IRC line parsing, RSS parsing from
  sample XML, ticker curation, and MCP tool dispatch.
- Web code is checked with `node --check` and by opening the page and
  running the command list by hand before filming the demo.
- The demo video shows the real app running, never slides alone.

## Out of scope

- No live IRC server is required to judge the app; the real client is a
  bonus for terminal users, and the local channel is the judged feature.
- No user accounts, no stored personal data, no backend, no payments.
