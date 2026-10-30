# ARC Séance — Requirements

> Written Oct 30, 2026, in the Kiroween submission period, as the spec that drives this build.
> Frankenstein category: stitch dead technologies into one working chimera.

## Introduction

ARC Séance is a retro-terminal agent command center that resurrects three dead
technologies in one app: BBS door games, IRC chat, and RSS feeds. A visitor
opens a haunted CRT terminal in a browser, plays a text door game, chats in an
IRC-style channel with bot spirits, reads an RSS ticker, and can summon a
stitched briefing that combines all three. A Python command line twin offers
the same three features in a terminal, plus a real (optional) IRC client and
a real RSS fetcher. Everything runs at $0 with no API keys and no backend.

## Glossary

- **Séance-master**: the terminal's host personality, a friendly spooky narrator.
- **Spirit**: a bot chatter in the IRC channel with a fixed personality.
- **Door game**: a small text adventure played with typed commands.
- **Ticker**: the RSS headline strip, curated and narrated by the séance-master.

## Requirements

### Requirement 1: Terminal shell

**User Story:** As a visitor, I want a retro terminal I can type in, so the
dead-tech resurrection feels like sitting at an old BBS machine.

#### Acceptance Criteria

1. WHEN the page loads, THE system SHALL show a boot sequence and a prompt.
2. WHEN the visitor types `help`, THE system SHALL list every command.
3. WHEN the visitor types an unknown command, THE system SHALL say so and
   suggest `help`, without crashing.
4. WHEN the visitor types `clear`, THE system SHALL empty the screen.

### Requirement 2: BBS door game

**User Story:** As a player, I want a playable door game, so the BBS half of
the chimera is a real game, not a picture of one.

#### Acceptance Criteria

1. WHEN the player types `play`, THE system SHALL start "The Haunted Keep".
2. WHEN the player types `look`, THE system SHALL describe the current room.
3. WHEN the player types `go <direction>`, THE system SHALL move between
   rooms only along defined exits, and SHALL refuse impossible moves.
4. WHEN the player takes an item that is present, THE system SHALL add it to
   inventory; taking an absent item SHALL fail with a message.
5. WHEN the player holds the candle and the grimoire in the crypt, THE system
   SHALL declare the game won and award the final score.

### Requirement 3: IRC channel

**User Story:** As a visitor, I want an IRC-style channel where I can chat
alongside bot spirits, so the IRC half of the chimera is alive.

#### Acceptance Criteria

1. WHEN the visitor types `irc`, THE system SHALL show the #seance channel.
2. WHEN the visitor types `say <message>`, THE system SHALL post it and a
   spirit SHALL reply when a keyword matches.
3. WHEN the visitor types `spirits`, THE system SHALL list the spirits.
4. THE Python twin SHALL include a real IRC protocol client (connect, join,
   message, ping/pong, parse) that is optional and fails gracefully offline.

### Requirement 4: RSS ticker

**User Story:** As a visitor, I want an RSS ticker, so the dead social feed
lives again as a curated strip.

#### Acceptance Criteria

1. WHEN the visitor types `rss`, THE system SHALL show ticker headlines.
2. THE ticker data SHALL come from a real public RSS feed fetched by a
   script, with source URL and fetch date recorded in the data file.
3. WHEN the fetcher cannot reach the network, THE system SHALL keep the
   last good data and label any bundled sample as a sample.
4. THE ticker SHALL never present sample or stale items as live news.

### Requirement 5: Séance summon (the stitch)

**User Story:** As a visitor, I want one command that stitches all three dead
technologies together, so the Frankenstein idea is demonstrated, not just
claimed.

#### Acceptance Criteria

1. WHEN the visitor types `seance <topic>`, THE system SHALL print a
   briefing with a door-game hint, a spirit quote, and a ticker headline.
2. WHEN no ticker headline matches the topic, THE system SHALL use the
   first headline and say the match is loose, not pretend it matched.
3. THE briefing SHALL be deterministic for a given topic and ticker, so
   judges can reproduce it.

### Requirement 6: Kiro usage, honestly shown

**User Story:** As a judge, I want to see real Kiro usage, so I can score
Technological Implementation fairly.

#### Acceptance Criteria

1. THE repo SHALL contain `.kiro/` at the root, not gitignored, with this
   spec, steering docs, hooks, a custom agent, and MCP settings.
2. THE repo SHALL contain an MCP server that a Kiro-style client can call
   over stdio JSON-RPC with real tools.
3. THE submission write-up SHALL describe only Kiro steps actually
   performed, and SHALL name any step that could not run here.

### Requirement 7: Free, safe, runnable

**User Story:** As a judge, I want to run this free, so evaluation is easy.

#### Acceptance Criteria

1. THE project SHALL need no API key, no payment, and no backend server.
2. THE project SHALL run with `python3 seance.py --help` and by opening
   `index.html` in a browser.
3. THE project SHALL contain no weapons, explosives, tactical, or
   combat content.
4. THE repo SHALL carry an OSI-approved license (MIT) visible at the root.
