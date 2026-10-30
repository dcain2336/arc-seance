// ARC Séance — web terminal logic.
// This file mirrors the Python twin: same rooms, same spirits, same
// summon stitch, so the web face and the terminal face agree with
// each other. No network calls happen here except loading the ticker
// data file, which the fetcher script prepares in advance.

// The rooms of the Haunted Keep, as plain data.
// Each room has a description, exits, and items lying there.
const ROOMS = {
  // The gate starts every game, and it holds the candle.
  gate: {
    desc: "The rusted gate of the Haunted Keep. Fog curls around your boots.",
    exits: { north: "hall" },
    items: ["candle"]
  },
  // The hall holds the key, and leads to the library and the crypt.
  hall: {
    desc: "A dusty hall with portraits whose eyes seem to follow you.",
    exits: { south: "gate", east: "library", north: "crypt" },
    items: ["key"]
  },
  // The library holds the grimoire, the book the crypt needs.
  library: {
    desc: "A library of books that whisper when you are not looking.",
    exits: { west: "hall" },
    items: ["grimoire"]
  },
  // The crypt is the goal room, reached only with the key in hand.
  crypt: {
    desc: "A cold crypt. Something important is meant to happen here.",
    exits: { south: "hall" },
    items: []
  }
};

// The spirits of the IRC channel, as plain data.
// Each spirit has a line and keyword replies.
const SPIRITS = [
  // Madame Zara tells fortunes and greets newcomers.
  {
    name: "Madame Zara",
    line: "Seer of the old wires, reader of static.",
    replies: {
      hello: "Madame Zara: Welcome, traveller. The wires hum your name.",
      hi: "Madame Zara: Welcome, traveller. The wires hum your name.",
      future: "Madame Zara: I see a door game in your future. Bring light."
    },
    fallback: "Madame Zara: The spirits murmur, but the message is unclear."
  },
  // Captain Byte loves the door game and old BBS days.
  {
    name: "Captain Byte",
    line: "Ex-sysop of the Haunted Keep BBS, still on duty.",
    replies: {
      game: "Captain Byte: The Keep awaits! Type play, then go north.",
      play: "Captain Byte: The Keep awaits! Type play, then go north.",
      bbs: "Captain Byte: 2400 baud and proud. The door is open."
    },
    fallback: "Captain Byte: Affirmative. The modem sings."
  },
  // Professor Patch follows the news ticker.
  {
    name: "Professor Patch",
    line: "Keeper of the ticker, patcher of dead feeds.",
    replies: {
      rss: "Professor Patch: The ticker lives! Dead feeds, resurrected.",
      news: "Professor Patch: The ticker lives! Dead feeds, resurrected.",
      feed: "Professor Patch: The ticker lives! Dead feeds, resurrected."
    },
    fallback: "Professor Patch: Noted. Filed under 'curious'."
  }
];

// One object holds the whole game state for this page visit.
const state = {
  // The room the player stands in right now, starting at the gate.
  room: "gate",
  // What the player carries, starting with nothing.
  inventory: [],
  // The score, starting at zero.
  score: 0,
  // Whether the game has been won yet.
  won: false,
  // Which rooms have been visited, for the first-visit bonus.
  visited: new Set(["gate"]),
  // Whether the door game has been started with the play command.
  playing: false,
  // The ticker headlines loaded from the data file, or the sample.
  ticker: [],
  // Whether the ticker in use is the bundled sample, not fetched news.
  tickerIsSample: true
};

// Find the screen element, where printed lines appear.
const screen = document.getElementById("screen");
// Find the input box, where the visitor types commands.
const input = document.getElementById("cmd");

// Print one line on the screen, keeping older lines above it.
function print(line) {
  // Create a new div element for this line.
  const div = document.createElement("div");
  // Put the line's text inside the new element.
  div.textContent = line;
  // Add the element to the bottom of the screen.
  screen.appendChild(div);
  // Scroll the screen down, so the newest line stays visible.
  screen.scrollTop = screen.scrollHeight;
}

// Describe the current room, including exits and items.
function look() {
  // Fetch the current room's data from the rooms table.
  const room = ROOMS[state.room];
  // Build the exits as a readable comma list.
  const exits = Object.keys(room.exits).sort().join(", ");
  // Build the items list, or say the room holds nothing.
  const items = room.items.length ? room.items.join(", ") : "nothing";
  // Return one plain description line for the player.
  return `You are in the ${state.room}. ${room.desc} Exits: ${exits}. Here: ${items}.`;
}

// Check the win condition quietly after every move and take.
function checkWin() {
  // The win needs the crypt room, the candle, and the grimoire.
  const won = state.room === "crypt"
    && state.inventory.includes("candle")
    && state.inventory.includes("grimoire");
  // Award the win bonus only the first time the condition is met.
  if (won && !state.won) {
    // Mark the game won, so the bonus is only given once.
    state.won = true;
    // Add fifty points for finishing the game.
    state.score += 50;
  }
}

// Try to move in a direction, and report what happened.
function go(direction) {
  // Fetch the current room's data from the rooms table.
  const room = ROOMS[state.room];
  // Refuse the move if that direction has no exit here.
  if (!room.exits[direction]) {
    // Tell the player plainly that the way is blocked.
    return "You cannot go that way. The dark holds you back.";
  }
  // Find the room that direction leads to.
  const target = room.exits[direction];
  // The crypt stays locked until the player carries the key.
  if (target === "crypt" && !state.inventory.includes("key")) {
    // Tell the player the crypt needs the key first.
    return "The crypt door is locked. It wants the key from the hall.";
  }
  // Move the player into the target room.
  state.room = target;
  // Award points the first time a new room is entered.
  if (!state.visited.has(target)) {
    // Mark the room visited, so the bonus is only given once.
    state.visited.add(target);
    // Add ten points for exploring somewhere new.
    state.score += 10;
  }
  // Check whether this move completed the win condition.
  checkWin();
  // Describe the new room for the player.
  return look();
}

// Try to take an item from the current room.
function take(item) {
  // Fetch the current room's data from the rooms table.
  const room = ROOMS[state.room];
  // Refuse the take if the item is not lying here.
  if (!room.items.includes(item)) {
    // Tell the player plainly that the item is not here.
    return `There is no ${item} here to take.`;
  }
  // Remove the item from the room, so it cannot be taken twice.
  room.items = room.items.filter((x) => x !== item);
  // Put the item in the player's inventory.
  state.inventory.push(item);
  // Award ten points for picking something up.
  state.score += 10;
  // Check whether this take completed the win condition.
  checkWin();
  // Confirm the take for the player.
  return `You take the ${item}. Score: ${state.score}.`;
}

// Pick a spirit reply for a chat message, by keyword.
function spiritReply(message) {
  // Lowercase the message, so matching ignores capital letters.
  const text = message.toLowerCase();
  // Walk through the spirits in order, looking for a keyword match.
  for (const spirit of SPIRITS) {
    // Walk through that spirit's keyword replies.
    for (const [keyword, reply] of Object.entries(spirit.replies)) {
      // Return the first reply whose keyword appears in the message.
      if (text.includes(keyword)) return reply;
    }
  }
  // If nothing matched, fall back to Madame Zara's default line.
  return SPIRITS[0].fallback;
}

// Build a stitched séance briefing for one topic.
function summon(topic) {
  // Lowercase the topic, so matching ignores capital letters.
  const low = topic.toLowerCase();
  // Pick a door-game hint by topic keyword, with a general hint as fallback.
  let hint;
  if (low.includes("candle") || low.includes("light")) {
    hint = "Door-game hint: the candle waits at the gate. Take it first.";
  } else if (low.includes("key")) {
    hint = "Door-game hint: the key waits in the hall. It opens the crypt.";
  } else if (low.includes("grimoire") || low.includes("book")) {
    hint = "Door-game hint: the grimoire waits in the library, east of the hall.";
  } else {
    hint = "Door-game hint: start at the gate, take the candle, find the key.";
  }
  // Pick a spirit quote by topic keyword, or use the default reply.
  const quote = spiritReply(topic);
  // Split the topic into words longer than two letters, for matching.
  const words = low.split(/\s+/).filter((w) => w.length > 2);
  // Default to no headline match yet.
  let headline = null;
  // Only attempt matching when the topic has at least one matchable word;
  // a topic made entirely of short words (≤ 2 chars) has nothing to match,
  // so skipping the loop avoids labelling that case as a "loose match".
  if (words.length > 0) {
    // Walk through ticker headlines, looking for a topic word in the title.
    for (const item of state.ticker) {
      // Check whether any topic word appears in this headline title.
      if (words.some((w) => item.title.toLowerCase().includes(w))) {
        // Keep the first matching headline and stop looking.
        headline = item.title;
        break;
      }
    }
    // If words existed but none matched, fall back to the first headline, honestly.
    if (headline === null && state.ticker.length) {
      // Note the loose match plainly, never pretend it matched.
      headline = `(loose match) ${state.ticker[0].title}`;
    }
  }
  // If the ticker is empty, say so plainly instead of inventing one.
  if (headline === null) headline = "(no ticker headlines available)";
  // Print the three stitched parts as one briefing.
  print(hint);
  print(quote);
  print(`Ticker: ${headline}`);
}

// Handle one typed command line from the visitor.
function handle(raw) {
  // Echo the command back, so the visitor sees what they typed.
  print(`> ${raw}`);
  // Split the line into a command word and the rest.
  const parts = raw.trim().split(/\s+/);
  // Take the command word, lowercased for matching.
  const cmd = (parts[0] || "").toLowerCase();
  // Take the argument as the rest of the line, joined with spaces.
  const arg = parts.slice(1).join(" ");
  // Show the command list when the visitor types help.
  if (cmd === "help") {
    print("Commands: help, play, look, go <direction>, take <item>, inventory,");
    print("score, irc, say <message>, spirits, rss, seance <topic>, clear, about.");
    return;
  }
  // Empty the screen when the visitor types clear.
  if (cmd === "clear") {
    screen.innerHTML = "";
    return;
  }
  // Start the door game when the visitor types play.
  if (cmd === "play") {
    state.playing = true;
    print("The Haunted Keep opens. Try look, go north, take candle.");
    print(look());
    return;
  }
  // Describe the room when the visitor types look, during the game.
  if (cmd === "look") {
    if (!state.playing) print("Type play first, traveller. The Keep waits.");
    else print(look());
    return;
  }
  // Move when the visitor types go with a direction, during the game.
  if (cmd === "go") {
    if (!state.playing) print("Type play first, traveller. The Keep waits.");
    else print(go(arg.toLowerCase()));
    if (state.won) print(`The crypt glows! You win! Final score: ${state.score}.`);
    return;
  }
  // Take when the visitor types take with an item, during the game.
  if (cmd === "take") {
    if (!state.playing) print("Type play first, traveller. The Keep waits.");
    else print(take(arg.toLowerCase()));
    if (state.won) print(`The crypt glows! You win! Final score: ${state.score}.`);
    return;
  }
  // Show inventory when the visitor types inventory.
  if (cmd === "inventory") {
    print(`Carrying: ${state.inventory.length ? state.inventory.join(", ") : "nothing"}. Score: ${state.score}.`);
    return;
  }
  // Show score when the visitor types score.
  if (cmd === "score") {
    print(`Score: ${state.score}.`);
    return;
  }
  // Show the channel when the visitor types irc.
  if (cmd === "irc") {
    print("#seance — spirits and visitors chat side by side.");
    for (const spirit of SPIRITS) print(` * ${spirit.name} — ${spirit.line}`);
    return;
  }
  // Post a message and print the spirit reply when the visitor says say.
  if (cmd === "say") {
    if (!arg) print("Say what? Try: say hello");
    else {
      print(`<visitor> ${arg}`);
      print(spiritReply(arg));
    }
    return;
  }
  // List the spirits when the visitor types spirits.
  if (cmd === "spirits") {
    for (const spirit of SPIRITS) print(` * ${spirit.name} — ${spirit.line}`);
    return;
  }
  // Show ticker headlines when the visitor types rss.
  if (cmd === "rss") {
    if (!state.ticker.length) print("No ticker headlines available.");
    else {
      if (state.tickerIsSample) print("(Sample ticker — bundled for offline use.)");
      for (const item of state.ticker) print(`- ${item.title}`);
    }
    return;
  }
  // Summon a stitched briefing when the visitor types seance.
  if (cmd === "seance") {
    if (!arg) print("Seance about what? Try: seance candle");
    else summon(arg);
    return;
  }
  // Describe the project when the visitor types about.
  if (cmd === "about") {
    print("ARC Séance: BBS door games + IRC + RSS, stitched into one terminal.");
    print("Built with Kiro specs, steering, hooks, and an MCP server. Free, no backend.");
    return;
  }
  // Refuse unknown commands plainly, and suggest help.
  print(`Unknown command: ${cmd}. Type help for the list.`);
}

// Load the ticker data file, falling back to a labelled sample.
async function loadTicker() {
  try {
    // Try to fetch the ticker data file prepared by the fetcher script.
    const response = await fetch("data/ticker.json");
    // Throw if the fetch did not succeed, so the fallback below runs.
    if (!response.ok) throw new Error("ticker fetch failed");
    // Parse the fetched file as JSON.
    const data = await response.json();
    // Use the fetched items, and mark the ticker as real, not sample.
    state.ticker = data.items || [];
    state.tickerIsSample = !!data.sample;
  } catch (e) {
    // Fall back to a small bundled sample, clearly labelled as sample.
    state.ticker = [
      { title: "Sample: The old wires hum again over the Haunted Keep" },
      { title: "Sample: Spirits report the ticker is alive and well" }
    ];
    state.tickerIsSample = true;
  }
}

// Boot the terminal: print the opening lines, load the ticker, focus input.
async function boot() {
  // Print the boot lines, in the voice of the séance-master.
  print("ARC SÉANCE — booting the haunted terminal...");
  print("BBS door: online. IRC channel: open. RSS ticker: waking.");
  print("Type help to see every command, or play to enter the Keep.");
  // Load the ticker data before the visitor asks for it.
  await loadTicker();
  // Put the typing cursor in the input box, ready for the first command.
  input.focus();
}

// Run a command when the visitor presses Enter in the input box.
input.addEventListener("keydown", (event) => {
  // Only act on the Enter key; other keys just type text.
  if (event.key !== "Enter") return;
  // Read the typed line, then clear the box for the next command.
  const raw = input.value;
  input.value = "";
  // Ignore empty lines without doing anything.
  if (!raw.trim()) return;
  // Handle the typed command line.
  handle(raw);
});

// Start the terminal as soon as this script loads.
boot();
