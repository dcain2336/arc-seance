# How Kiro was used — ARC Séance (honest account)

This page says exactly what Kiro did and did not do in this build, so
judges can score Technological Implementation fairly. Nothing here is
embellished.

## What Kiro genuinely shaped

- **Spec-driven development, in Kiro's own shape.** The build started
  from `.kiro/specs/arc-seance/`: `requirements.md` (EARS-style
  acceptance criteria), `design.md` (architecture, components, data
  flow), and `tasks.md` (sequenced, checkable tasks). Code was written
  task by task against that spec, and the spec's acceptance criteria
  are what the test suite checks. This is the workflow Kiro defines;
  the spec files in the repo are the evidence.
- **Steering.** `.kiro/steering/` holds product voice rules, tech
  rules (plain HTML/CSS/JS, stdlib-only Python, no backend), and the
  project structure. The app's voice and honesty labels follow them.
- **Hooks.** `.kiro/hooks/` defines two hooks in Kiro's JSON hook
  format: run the Python test suite on Python save, and syntax-check
  the web script on save. Their commands are the exact commands run
  during this build (see Verification below).
- **Custom agent.** `.kiro/agents/seance-master.md` defines the
  séance-master agent: voice, tools, and rules. It is written in
  Kiro's documented custom-agent format.
- **MCP.** `.kiro/settings/mcp.json` configures the séance MCP server,
  and `mcp/seance_mcp.py` implements it: stdio JSON-RPC with
  `initialize`, `tools/list`, and `tools/call`, exposing
  `summon_spirit`, `door_game_move`, `read_ticker`, and `irc_say`.
  It was tested end to end by piping JSON-RPC requests into it and
  reading real answers back (see Verification).
- **Kiro CLI, installed and probed.** The real Kiro CLI was installed
  Oct 30, 2026 from the official installer (`curl -fsSL
  https://cli.kiro.dev/install | bash`) and `kiro-cli --help` runs.
  This proves the tooling the project targets is real and present.

## What Kiro's AI did NOT do in this session — read this

- **Kiro CLI chat was not used to generate code.** Every Kiro CLI
  command that touches an AI session (`agent list`, `agent validate`,
  `chat`) refused with "You are not logged in, please log in with
  kiro-cli login". Chat additionally tried to open a browser for
  authentication and failed in this headless environment, suggesting
  `kiro-cli login --use-device-flow` instead.
- **No Builder ID credentials were entered anywhere in this build.**
  The Kiro account on file (AWS Builder ID arc-agent-ops@proton.me,
  free plan, user ID on file in the submission pack) was not signed
  into from this environment, and no sign-in was faked.
- **Consequence, stated plainly:** the code in this repo was written
  by following the Kiro spec by hand (ARC agent work), not by Kiro's
  own AI agent. The Kiro artefacts above are real and in Kiro's
  formats, and the CLI is installed, but AI generation through Kiro
  did not happen here. Any claim stronger than that would be false.

## The one step that would close this gap

Run, on a machine with a browser:

```sh
kiro-cli login --use-device-flow
```

Complete the sign-in as the Kiro account on file, then run one real
Kiro CLI task against this repo — for example, asking Kiro to review
`app.js` for the spec's acceptance criteria and applying one of its
suggestions as a committed change. That single logged-in session would
turn "Kiro-shaped, hand-built" into "Kiro AI used in the build", and
the write-up above should be updated to say so before submission if
that session happens. Until then, this page stands as written.

## Update — Oct 30, 2026: the logged-in Kiro session happened (one task)

The step described in the section above has now happened, and that
section is preserved above as the pre-login record. What follows is
what changed, and what did not.

- **Login succeeded Oct 30, 2026**, via `kiro-cli login
  --use-device-flow`, completed in a browser by the account owner.
  Verified afterwards in this environment: `kiro-cli whoami`
  prints "Logged in with Builder ID, Email:
  arc-agent-ops@proton.me", and `kiro-cli agent list` works
  (it previously refused with "not logged in").
- **One real Kiro CLI chat task was run**, non-interactively:
  `kiro-cli chat --no-interactive --trust-all-tools`, asked to
  review `app.js` against `.kiro/specs/arc-seance/requirements.md`
  (especially Requirement 1 and Requirement 5) and to apply
  exactly ONE small, genuine improvement to `app.js` only, with
  no other file touched and nothing committed by the chat itself.
- **What Kiro's AI found and changed:** a real honesty bug in the
  `summon()` function. A topic made only of short words (for
  example "go" or "it") yields zero matchable words after the
  longer-than-two-characters filter, so the headline loop could
  never match — yet the code still labelled the fallback
  "(loose match)". The fix wraps the headline-matching loop and
  the loose-match fallback in `if (words.length > 0)`; when the
  topic has no matchable words, the briefing now falls through
  to the existing no-headlines message instead of claiming a
  loose match. File changed: `app.js` only (17 insertions, 12
  deletions, plain-English comments kept). Commit:
  `ba2311f` ("Kiro CLI review fix: do not label empty-topic
  seance as a loose match"), pushed to `main`. Verified after
  the change: `node --check app.js` clean, Python test suite
  still 13/13 passing.
- **One wording note, stated plainly:** in the empty-topic case
  the briefing now uses the existing no-headlines message even
  when headlines exist. The false loose-match label is gone;
  that wording is the remaining imprecision in this corner case.
- **What Kiro's AI did NOT do:** it did not write the bulk of
  this app. Every other file, and the rest of `app.js`, was
  written earlier on Oct 30, 2026 by following the Kiro spec by
  hand, before this login existed. This session contributed
  exactly one fix to one file. It did not commit or push
  anything itself; the commit and push were done by the ARC
  agent after verifying the change. The demo video, the repo,
  and the submission pack were already complete before this
  session.

So the honest summary now reads: Kiro's spec, steering, hooks,
custom agent, and MCP shaped the build; the bulk of the code was
written by hand against that spec; and Kiro's own AI, once logged
in, reviewed the code and contributed one real, committed fix.

## Verification performed (reproducible)

- `python3 -m unittest discover -s tests -v` — 13 tests, all passing.
- `node --check app.js` — clean.
- MCP smoke test: piped `initialize`, `tools/list`, `tools/call`
  (summon_spirit, read_ticker) into `mcp/seance_mcp.py` and received
  correct JSON-RPC replies with real content.
- CLI playthrough: piped a full command sequence into
  `python3 seance.py play` and reached the crypt; `summon`, `irc`,
  and `rss` subcommands all print real output.
- RSS: `python3 tools/rss_seance.py` fetched 10 real NASA headlines
  into `data/ticker.json` on Oct 30, 2026, with source recorded.
