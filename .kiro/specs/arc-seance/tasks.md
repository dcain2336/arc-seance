# ARC Séance — Tasks

> Written Oct 30, 2026. Each task maps to requirements.md. Mark a task done
> only when its check passes.

- [x] 1. Scaffold the repo
  - Create the directory layout, MIT LICENSE, README, and .gitignore
    that does NOT ignore `.kiro/`.
  - _Requirements: 6.1, 7.4_

- [x] 2. Write the Kiro layer first
  - Spec (this folder), steering docs, hooks, custom agent, MCP settings.
  - Validate the custom agent with the real Kiro CLI where possible.
  - _Requirements: 6.1, 6.2_

- [x] 3. Build the web terminal shell
  - Boot sequence, prompt, parser, dispatcher, `help`, `clear`, unknown
    command handling.
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [x] 4. Build the door game (web + Python)
  - Room data, moves, items, inventory, score, win condition.
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

- [x] 5. Build the IRC channel (web + Python)
  - Channel log, three spirits, keyword replies, `spirits` listing.
  - Real stdlib IRC client in the Python twin, optional, graceful offline.
  - _Requirements: 3.1, 3.2, 3.3, 3.4_

- [x] 6. Build the RSS ticker
  - Fetcher script with source + fetch date recorded; web ticker display;
    sample clearly labelled; failed fetch never overwrites good data.
  - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [x] 7. Build the séance summon stitch
  - One command combining a game hint, a spirit quote, and a headline,
    deterministic, with an honest loose-match note.
  - _Requirements: 5.1, 5.2, 5.3_

- [x] 8. Build the MCP server
  - Stdio JSON-RPC with initialize, tools/list, tools/call, four tools.
  - _Requirements: 6.2_

- [x] 9. Tests, end to end
  - Run the Python test suite; run `node --check` on the web script;
    play the game to a win; post in the channel; read the ticker.
  - _Requirements: all_

- [ ] 10. Demo video and submission package
  - Film the real app working, under 3 minutes, no copyrighted music.
  - Write the honest Kiro-usage write-up and the Devpost field pack.
  - _Requirements: 6.3_
