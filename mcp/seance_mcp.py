#!/usr/bin/env python3
# ARC Séance — MCP server over stdio.
# This file speaks JSON-RPC on standard input and output in the MCP
# shape, so a Kiro-style client can call séance tools: initialize, list
# tools, and call tools. It runs locally, needs no key, no network.
# It reuses the game, spirits, and ticker logic from seance.py, so the
# tools answer from the same code the terminal twin uses.

# Import JSON handling, so requests and replies can be parsed and built.
import json
# Import path handling, so seance.py can be found next to this file.
import os
# Import system tools, so this server can read stdin and write stdout.
import sys

# Add the project root to the import path, so seance.py is importable.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Import the game, spirit replies, briefing, and ticker loader.
from seance import Game, load_ticker, spirit_reply, summon_briefing

# Keep one door game alive for the whole server session, so moves build.
GAME = Game()


# List the four tools this server offers, with plain descriptions.
def list_tools():
    # Return the tool list in the MCP tools/list shape.
    return [
        # The summon tool stitches a briefing for one topic.
        {"name": "summon_spirit", "description": "Summon a stitched briefing (game hint, spirit quote, ticker headline) for a topic.", "inputSchema": {"type": "object", "properties": {"topic": {"type": "string"}}, "required": ["topic"]}},
        # The door game tool moves, looks, or takes in the Haunted Keep.
        {"name": "door_game_move", "description": "Play the Haunted Keep: look, go in a direction, or take an item.", "inputSchema": {"type": "object", "properties": {"action": {"type": "string"}, "argument": {"type": "string"}}}},
        # The ticker tool reads the RSS headlines from the data file.
        {"name": "read_ticker", "description": "Read the current RSS ticker headlines.", "inputSchema": {"type": "object", "properties": {}}},
        # The channel tool posts a message and returns the spirit reply.
        {"name": "irc_say", "description": "Post a message in the #seance channel and get the spirit reply.", "inputSchema": {"type": "object", "properties": {"message": {"type": "string"}}, "required": ["message"]}},
    ]


# Call one tool by name with arguments, and return its text answer.
def call_tool(name, args):
    # Summon a briefing when the summon tool is called.
    if name == "summon_spirit":
        # Load the ticker and build the briefing for the given topic.
        return summon_briefing(args.get("topic", ""), load_ticker())
    # Play a door game move when the door game tool is called.
    if name == "door_game_move":
        # Read the action word, lowercased for matching.
        action = args.get("action", "").lower()
        # Read the argument, such as a direction or an item name.
        argument = args.get("argument", "").lower()
        # Describe the room when the action is look.
        if action == "look":
            return GAME.look()
        # Move when the action is go, with the direction as argument.
        if action == "go":
            return GAME.go(argument)
        # Take when the action is take, with the item as argument.
        if action == "take":
            return GAME.take(argument)
        # Refuse unknown door game actions plainly.
        return "Unknown door game action. Use look, go, or take."
    # Read the ticker when the ticker tool is called.
    if name == "read_ticker":
        # Load the ticker items from the data file.
        ticker = load_ticker()
        # Say plainly if there are no headlines to show.
        if not ticker:
            return "No ticker headlines available."
        # Join the headlines into one readable block of text.
        return "\n".join(f"- {item.get('title', '')}" for item in ticker)
    # Post in the channel when the channel tool is called.
    if name == "irc_say":
        # Return the spirit reply for the given message.
        return spirit_reply(args.get("message", ""))
    # Refuse unknown tool names plainly, naming the tool asked for.
    return f"Unknown tool: {name}"


# Handle one JSON-RPC request dictionary, and return a reply dictionary.
def handle(request):
    # Read the request id, so the reply can be matched to the request.
    req_id = request.get("id")
    # Read the method name from the request.
    method = request.get("method", "")
    # Answer the initialize handshake with server info.
    if method == "initialize":
        # Return the protocol version, capabilities, and server name.
        return {"jsonrpc": "2.0", "id": req_id, "result": {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "serverInfo": {"name": "arc-seance", "version": "1.0.0"}}}
    # Answer a tools/list request with the four tools.
    if method == "tools/list":
        # Return the tool list under the tools key.
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": list_tools()}}
    # Answer a tools/call request by dispatching to the named tool.
    if method == "tools/call":
        # Read the parameters block, or an empty dictionary if missing.
        params = request.get("params", {})
        # Call the tool and capture its text answer.
        text = call_tool(params.get("name", ""), params.get("arguments", {}))
        # Return the answer as one text content block.
        return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": text}]}}
    # Refuse unknown methods plainly, with a standard error code.
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Unknown method: {method}"}}


# Run the server loop, reading one JSON request per stdin line.
def main():
    # Loop over stdin lines until input ends.
    for line in sys.stdin:
        # Skip blank lines without answering anything.
        if not line.strip():
            continue
        # Parse the line as JSON, skipping lines that are not JSON.
        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            continue
        # Handle the request and build the reply dictionary.
        reply = handle(request)
        # Write the reply as one JSON line on stdout, flushed at once.
        sys.stdout.write(json.dumps(reply) + "\n")
        sys.stdout.flush()
    # Return zero when stdin closes cleanly.
    return 0


# Run the server only when this file is executed directly.
if __name__ == "__main__":
    # Exit with the server loop's return code.
    sys.exit(main())
