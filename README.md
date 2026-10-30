# ARC Séance

A retro-terminal agent command center that resurrects three dead
technologies in one app — **BBS door games, IRC, and RSS** — stitched
together by a séance summon. Frankenstein category, Kiroween 2026.

## Try it in a browser

Open `index.html`. No build step, no framework, no key, no backend.

Type `help`, then:

```
play
look
go north
take key
seance candle
say hello
rss
```

Win the door game: take the candle at the gate, take the key in the
hall, take the grimoire in the library, then go north into the crypt.

## Try it in a terminal

```sh
python3 seance.py play        # interactive Haunted Keep door game
python3 seance.py irc --say hello
python3 seance.py rss
python3 seance.py summon candle
python3 tools/rss_seance.py  # refresh data/ticker.json from NASA RSS
```

The Python twin needs only the standard library. The IRC client in
`irc_client.py` is optional: the local `#seance` channel works offline,
and the real client is only used when you point it at a real server.

## The chimera, part by part

- **BBS door game** — "The Haunted Keep": four rooms, three items, a
  locked crypt, a score, and a win condition. Same game in the browser
  and in the terminal.
- **IRC** — `#seance`: three bot spirits (Madame Zara, Captain Byte,
  Professor Patch) answer by keyword, alongside visitor messages. A
  real stdlib IRC protocol client is included for terminal users.
- **RSS** — a ticker fed by a real public feed (NASA breaking news),
  fetched by `tools/rss_seance.py` into `data/ticker.json` with source
  and fetch date recorded. A failed fetch never overwrites good data.
- **Séance summon** — `seance <topic>` stitches a door-game hint, a
  spirit quote, and a ticker headline into one briefing. Deterministic,
  and honest when the headline match is loose.

## Kiro usage (honest version)

See `docs/KIRO-USAGE.md` for the full, honest account, including what
could not run in this environment. In short:

- Spec-driven: `.kiro/specs/arc-seance/` (requirements in EARS style,
  design, tasks) written before implementation, and followed.
- Steering: `.kiro/steering/` (product, tech, structure).
- Hooks: `.kiro/hooks/` — test suite on Python save, syntax check on
  web script save.
- Custom agent: `.kiro/agents/seance-master.md`.
- MCP: `.kiro/settings/mcp.json` plus `mcp/seance_mcp.py`, a stdio
  JSON-RPC server with four real tools.
- CLI: the real Kiro CLI was installed and used to validate the agent
  configuration; AI chat through the CLI needs an interactive Builder ID
  sign-in, which could not run in this headless environment — see the
  write-up for exactly what was and was not done with the CLI.

## Run the tests

```sh
python3 -m unittest discover -s tests -v
node --check app.js
```

## License

MIT — see `LICENSE`. The repository is public, and `.kiro/` is not
gitignored, as the contest requires.
