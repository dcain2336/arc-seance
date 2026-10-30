# Steering — Structure

- `index.html`, `style.css`, `app.js` — the web terminal face.
- `seance.py` — the Python command line twin (play, irc, rss, summon).
- `irc_client.py` — the real, optional, stdlib IRC protocol client.
- `tools/rss_seance.py` — the RSS fetcher that writes `data/ticker.json`.
- `mcp/seance_mcp.py` — the stdio JSON-RPC MCP server.
- `tests/test_seance.py` — the unit test suite.
- `.kiro/specs/arc-seance/` — requirements, design, tasks (this spec).
- `.kiro/steering/` — product, tech, structure (this folder).
- `.kiro/hooks/` — agent hooks that automate checks.
- `.kiro/agents/` — the séance-master custom agent.
- `.kiro/settings/mcp.json` — MCP server configuration.
- `docs/KIRO-USAGE.md` — the honest Kiro-usage write-up.
- `docs/SUBMISSION.md` — the Devpost field pack.
