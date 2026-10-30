#!/usr/bin/env python3
# ARC Séance — Python command line twin.
# This file gives judges the same three resurrected technologies in a
# terminal: a BBS door game, an IRC-style channel, and an RSS ticker,
# plus the séance summon that stitches all three together.
# It needs only the Python standard library, no key, no backend.

# Import the argument parser, so the user can pick a subcommand.
import argparse
# Import JSON handling, so the ticker data file can be read.
import json
# Import path handling, so the ticker file is found next to this script.
import os
# Import system tools, so the program can exit cleanly on bad input.
import sys

# The rooms of the Haunted Keep, as plain data.
# Each room has a description, exits to other rooms, and items lying there.
ROOMS = {
    # The gate is where every game starts, and it holds the candle.
    "gate": {
        "desc": "The rusted gate of the Haunted Keep. Fog curls around your boots.",
        "exits": {"north": "hall"},
        "items": ["candle"],
    },
    # The hall holds the key, and it leads to the library and the crypt.
    "hall": {
        "desc": "A dusty hall with portraits whose eyes seem to follow you.",
        "exits": {"south": "gate", "east": "library", "north": "crypt"},
        "items": ["key"],
    },
    # The library holds the grimoire, the book the crypt needs.
    "library": {
        "desc": "A library of books that whisper when you are not looking.",
        "exits": {"west": "hall"},
        "items": ["grimoire"],
    },
    # The crypt is the goal room, reached only with the key in hand.
    "crypt": {
        "desc": "A cold crypt. Something important is meant to happen here.",
        "exits": {"south": "hall"},
        "items": [],
    },
}

# The spirits of the IRC channel, as plain data.
# Each spirit has a personality line and keyword replies.
SPIRITS = [
    {
        # Madame Zara tells fortunes and greets newcomers.
        "name": "Madame Zara",
        "line": "Seer of the old wires, reader of static.",
        "replies": {
            "hello": "Madame Zara: Welcome, traveller. The wires hum your name.",
            "hi": "Madame Zara: Welcome, traveller. The wires hum your name.",
            "future": "Madame Zara: I see a door game in your future. Bring light.",
        },
        "default": "Madame Zara: The spirits murmur, but the message is unclear.",
    },
    {
        # Captain Byte loves the door game and old BBS days.
        "name": "Captain Byte",
        "line": "Ex-sysop of the Haunted Keep BBS, still on duty.",
        "replies": {
            "game": "Captain Byte: The Keep awaits! Type play, then go north.",
            "play": "Captain Byte: The Keep awaits! Type play, then go north.",
            "bbs": "Captain Byte: 2400 baud and proud. The door is open.",
        },
        "default": "Captain Byte: Affirmative. The modem sings.",
    },
    {
        # Professor Patch follows the news ticker.
        "name": "Professor Patch",
        "line": "Keeper of the ticker, patcher of dead feeds.",
        "replies": {
            "rss": "Professor Patch: The ticker lives! Dead feeds, resurrected.",
            "news": "Professor Patch: The ticker lives! Dead feeds, resurrected.",
            "feed": "Professor Patch: The ticker lives! Dead feeds, resurrected.",
        },
        "default": "Professor Patch: Noted. Filed under 'curious'.",
    },
]


# A small class that holds one door game in progress.
class Game:
    # Start a fresh game at the gate, with empty pockets and zero score.
    def __init__(self):
        # Remember the room the player stands in right now.
        self.room = "gate"
        # Remember what the player carries, starting with nothing.
        self.inventory = []
        # Remember the score, starting at zero.
        self.score = 0
        # Remember whether the game has been won yet.
        self.won = False
        # Remember which rooms have been visited, for the first-visit bonus.
        self.visited = {"gate"}

    # Describe the room the player stands in, including exits and items.
    def look(self):
        # Fetch the current room's data from the rooms table.
        room = ROOMS[self.room]
        # Build the list of exits as a readable string.
        exits = ", ".join(sorted(room["exits"]))
        # Build the list of items, or say the room is empty.
        items = ", ".join(room["items"]) if room["items"] else "nothing"
        # Return one plain description line for the player.
        return f"You are in the {self.room}. {room['desc']} Exits: {exits}. Here: {items}."

    # Try to move in a direction, and report what happened.
    def go(self, direction):
        # Fetch the current room's data from the rooms table.
        room = ROOMS[self.room]
        # Refuse the move if that direction has no exit here.
        if direction not in room["exits"]:
            # Tell the player plainly that the way is blocked.
            return "You cannot go that way. The dark holds you back."
        # Find the room that direction leads to.
        target = room["exits"][direction]
        # The crypt stays locked until the player carries the key.
        if target == "crypt" and "key" not in self.inventory:
            # Tell the player the crypt needs the key first.
            return "The crypt door is locked. It wants the key from the hall."
        # Move the player into the target room.
        self.room = target
        # Award points the first time a new room is entered.
        if target not in self.visited:
            # Mark the room visited, so the bonus is only given once.
            self.visited.add(target)
            # Add ten points for exploring somewhere new.
            self.score += 10
        # Check whether this move completed the win condition.
        self._check_win()
        # Describe the new room for the player.
        return self.look()

    # Try to take an item from the current room.
    def take(self, item):
        # Fetch the current room's data from the rooms table.
        room = ROOMS[self.room]
        # Refuse the take if the item is not lying here.
        if item not in room["items"]:
            # Tell the player plainly that the item is not here.
            return f"There is no {item} here to take."
        # Remove the item from the room, so it cannot be taken twice.
        room["items"].remove(item)
        # Put the item in the player's inventory.
        self.inventory.append(item)
        # Award ten points for picking something up.
        self.score += 10
        # Check whether this take completed the win condition.
        self._check_win()
        # Confirm the take for the player.
        return f"You take the {item}. Score: {self.score}."

    # Check the win condition quietly after every move and take.
    def _check_win(self):
        # The win needs the crypt room, the candle, and the grimoire.
        won = (
            self.room == "crypt"
            and "candle" in self.inventory
            and "grimoire" in self.inventory
        )
        # Award the win bonus only the first time the condition is met.
        if won and not self.won:
            # Mark the game won, so the bonus is only given once.
            self.won = True
            # Add fifty points for finishing the game.
            self.score += 50


# Pick a spirit reply for a chat message, by keyword.
def spirit_reply(message):
    # Lowercase the message, so matching ignores capital letters.
    text = message.lower()
    # Walk through the spirits in order, looking for a keyword match.
    for spirit in SPIRITS:
        # Walk through that spirit's keyword replies.
        for keyword, reply in spirit["replies"].items():
            # Return the first reply whose keyword appears in the message.
            if keyword in text:
                return reply
    # If nothing matched, fall back to Madame Zara's default line.
    return SPIRITS[0]["default"]


# Load the ticker data file, or return an empty list if it is missing.
def load_ticker():
    # Build the path to the ticker file next to this script.
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "ticker.json")
    # Return an empty list early if the file does not exist yet.
    if not os.path.exists(path):
        return []
    # Open the ticker file and read it as JSON.
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    # Return just the list of ticker items from the file.
    return data.get("items", [])


# Build a stitched séance briefing for one topic.
def summon_briefing(topic, ticker):
    # Lowercase the topic, so matching ignores capital letters.
    low = topic.lower()
    # Pick a door-game hint by topic keyword, with a general hint as fallback.
    if "candle" in low or "light" in low:
        hint = "Door-game hint: the candle waits at the gate. Take it first."
    elif "key" in low:
        hint = "Door-game hint: the key waits in the hall. It opens the crypt."
    elif "grimoire" in low or "book" in low:
        hint = "Door-game hint: the grimoire waits in the library, east of the hall."
    else:
        hint = "Door-game hint: start at the gate, take the candle, find the key."
    # Pick a spirit quote by topic keyword, or use the default reply.
    quote = spirit_reply(topic)
    # Split the topic into words longer than two letters, for matching.
    words = [word for word in low.split() if len(word) > 2]
    # Default to no headline match yet.
    headline = None
    # Walk through ticker headlines, looking for a topic word in the title.
    for item in ticker:
        # Check whether any topic word appears in this headline title.
        if any(word in item.get("title", "").lower() for word in words):
            # Keep the first matching headline and stop looking.
            headline = item.get("title", "")
            break
    # If no headline matched, fall back to the first headline, honestly.
    if headline is None and ticker:
        # Note the loose match plainly, never pretend it matched.
        headline = f"(loose match) {ticker[0].get('title', '')}"
    # If the ticker is empty, say so plainly instead of inventing a headline.
    if headline is None:
        headline = "(no ticker headlines available)"
    # Return the three stitched parts as one briefing.
    return f"{hint}\n{quote}\nTicker: {headline}"


# Play the door game interactively, reading commands from the keyboard.
def cmd_play(_args):
    # Start a fresh game for this session.
    game = Game()
    # Print the opening lines of the game.
    print("The Haunted Keep opens. Type look, go <direction>, take <item>, or quit.")
    # Print the starting room description.
    print(game.look())
    # Loop forever until the player quits or wins.
    while True:
        # Read one command line from the player, stripped of extra spaces.
        try:
            line = input("> ").strip()
        except EOFError:
            # End the game cleanly if input runs out.
            break
        # Split the line into a command word and the rest.
        parts = line.split(None, 1)
        # Skip empty lines without doing anything.
        if not parts:
            continue
        # Take the command word, lowercased for matching.
        cmd = parts[0].lower()
        # Take the argument, or an empty string if there is none.
        arg = parts[1] if len(parts) > 1 else ""
        # Quit the game when the player says quit or exit.
        if cmd in ("quit", "exit"):
            break
        # Describe the room when the player says look.
        if cmd == "look":
            print(game.look())
        # Move when the player says go with a direction.
        elif cmd == "go":
            print(game.go(arg.lower()))
        # Take when the player says take with an item name.
        elif cmd == "take":
            print(game.take(arg.lower()))
        # Show inventory and score when the player says inventory.
        elif cmd == "inventory":
            print(f"Carrying: {', '.join(game.inventory) or 'nothing'}. Score: {game.score}.")
        # Refuse unknown commands plainly, and suggest look.
        else:
            print("Unknown game command. Try look, go, take, inventory, or quit.")
        # Congratulate and stop when the game has been won.
        if game.won:
            print(f"The crypt glows! You win! Final score: {game.score}.")
            break
    # Return zero, meaning the command finished cleanly.
    return 0


# Run the IRC channel in the terminal, with one optional message.
def cmd_irc(args):
    # Print the channel header, so the user knows where they are.
    print("#seance — the channel where spirits and visitors chat side by side.")
    # List the spirits, so the user knows who is listening.
    for spirit in SPIRITS:
        print(f" * {spirit['name']} — {spirit['line']}")
    # If the user gave a message, post it and print the spirit reply.
    if args.say:
        print(f"<visitor> {args.say}")
        print(spirit_reply(args.say))
    # Return zero, meaning the command finished cleanly.
    return 0


# Print the RSS ticker headlines in the terminal.
def cmd_rss(_args):
    # Load the ticker items from the data file.
    ticker = load_ticker()
    # Say plainly if there are no headlines to show.
    if not ticker:
        print("No ticker headlines available. Run tools/rss_seance.py to fetch some.")
        return 0
    # Print each headline with its link, one per line.
    for item in ticker:
        print(f"- {item.get('title', '')} ({item.get('link', '')})")
    # Return zero, meaning the command finished cleanly.
    return 0


# Print a stitched séance briefing for one topic.
def cmd_summon(args):
    # Load the ticker items from the data file.
    ticker = load_ticker()
    # Build the briefing and print it.
    print(summon_briefing(args.topic, ticker))
    # Return zero, meaning the command finished cleanly.
    return 0


# Build the command line interface and run the chosen subcommand.
def main(argv=None):
    # Create the argument parser with a short description.
    parser = argparse.ArgumentParser(description="ARC Séance — resurrect BBS, IRC, and RSS in one terminal.")
    # Add subcommands, so each feature has its own word.
    sub = parser.add_subparsers(dest="command", required=True)
    # Add the play subcommand for the door game.
    sub.add_parser("play", help="Play the Haunted Keep door game.")
    # Add the irc subcommand for the channel.
    irc = sub.add_parser("irc", help="Visit the #seance channel.")
    # Add an optional message argument to the irc subcommand.
    irc.add_argument("--say", default="", help="One message to post in the channel.")
    # Add the rss subcommand for the ticker.
    sub.add_parser("rss", help="Print the RSS ticker headlines.")
    # Add the summon subcommand for the stitched briefing.
    summon = sub.add_parser("summon", help="Summon a stitched briefing for a topic.")
    # Add the required topic argument to the summon subcommand.
    summon.add_argument("topic", help="The topic to summon a briefing about.")
    # Parse the user's arguments.
    args = parser.parse_args(argv)
    # Dispatch to the matching subcommand function.
    if args.command == "play":
        return cmd_play(args)
    if args.command == "irc":
        return cmd_irc(args)
    if args.command == "rss":
        return cmd_rss(args)
    if args.command == "summon":
        return cmd_summon(args)
    # This line is unreachable, but keeps the function total.
    return 2


# Run the program only when this file is executed directly.
if __name__ == "__main__":
    # Exit with the subcommand's return code.
    sys.exit(main())
