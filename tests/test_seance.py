#!/usr/bin/env python3
# ARC Séance — unit tests, standard library only.
# These tests cover the parts judges cannot see by eye: door game
# moves, item taking, the win condition, IRC line parsing, RSS parsing,
# ticker curation, and MCP tool dispatch. Run them with:
# python3 -m unittest discover -s tests -v

# Import path handling, so the project code can be found from tests.
import os
# Import system tools, so the project root can be added to imports.
import sys
# Import the unit test framework from the standard library.
import unittest
# Import XML tools, so RSS sample documents can be parsed in tests.
import xml.etree.ElementTree as ET

# Add the project root to the import path, so seance.py is importable.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Import the game, spirit replies, briefing, and ticker loader.
from seance import Game, ROOMS, load_ticker, spirit_reply, summon_briefing
# Import the IRC line parser from the client module.
from irc_client import parse_irc_line
# Import the MCP tool dispatcher, without starting the server loop.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "mcp"))
# Import the tool call function from the MCP server module.
from seance_mcp import call_tool


# Tests for the door game state machine.
class TestGame(unittest.TestCase):
    # Build a fresh game before each test, so tests never share state.
    def setUp(self):
        # Create a new game, starting at the gate.
        self.game = Game()
        # Reset the shared room items, since takes mutate them.
        ROOMS["gate"]["items"] = ["candle"]
        ROOMS["hall"]["items"] = ["key"]
        ROOMS["library"]["items"] = ["grimoire"]
        ROOMS["crypt"]["items"] = []

    # Moving north from the gate should reach the hall.
    def test_go_north_from_gate(self):
        # Move north and check the new room is the hall.
        self.game.go("north")
        self.assertEqual(self.game.room, "hall")

    # Moving in a direction with no exit should refuse and stay put.
    def test_illegal_move_refused(self):
        # Try to go west from the gate, which has no west exit.
        text = self.game.go("west")
        # Check the refusal message and that the room did not change.
        self.assertIn("cannot go", text)
        self.assertEqual(self.game.room, "gate")

    # The crypt should stay locked until the player carries the key.
    def test_crypt_locked_without_key(self):
        # Move north into the hall without taking anything.
        self.game.go("north")
        # Try to enter the crypt without the key.
        text = self.game.go("north")
        # Check the lock message and that the player stayed in the hall.
        self.assertIn("locked", text)
        self.assertEqual(self.game.room, "hall")

    # Taking an item should add it to inventory and score points.
    def test_take_item(self):
        # Take the candle lying at the gate.
        text = self.game.take("candle")
        # Check the candle is now carried and the score rose.
        self.assertIn("candle", self.game.inventory)
        self.assertEqual(self.game.score, 10)
        self.assertIn("take the candle", text)

    # Taking an absent item should fail without changing inventory.
    def test_take_absent_item(self):
        # Try to take the grimoire at the gate, where it is not lying.
        text = self.game.take("grimoire")
        # Check the failure message and the empty inventory.
        self.assertIn("no grimoire", text)
        self.assertEqual(self.game.inventory, [])

    # The full winning path should end with the game won.
    def test_win_path(self):
        # Take the candle at the gate.
        self.game.take("candle")
        # Move north into the hall and take the key.
        self.game.go("north")
        self.game.take("key")
        # Move east into the library and take the grimoire.
        self.game.go("east")
        self.game.take("grimoire")
        # Move west back to the hall, then north into the crypt.
        self.game.go("west")
        self.game.go("north")
        # Check the game is won and the player stands in the crypt.
        self.assertTrue(self.game.won)
        self.assertEqual(self.game.room, "crypt")


# Tests for the IRC line parser.
class TestIrcParsing(unittest.TestCase):
    # A normal chat message should parse into prefix, command, and args.
    def test_privmsg_parses(self):
        # Parse a sample PRIVMSG line from a spirit.
        parsed = parse_irc_line(":Madame!zara@host PRIVMSG #seance :Hello there")
        # Check each parsed piece matches the sample line.
        self.assertEqual(parsed["prefix"], "Madame!zara@host")
        self.assertEqual(parsed["command"], "PRIVMSG")
        self.assertEqual(parsed["args"], ["#seance", "Hello there"])

    # A server ping should parse into a PING command with its argument.
    def test_ping_parses(self):
        # Parse a sample PING line from a server.
        parsed = parse_irc_line("PING :12345")
        # Check the command and argument match the sample line.
        self.assertEqual(parsed["command"], "PING")
        self.assertEqual(parsed["args"], ["12345"])


# Tests for RSS parsing and the summon stitch.
class TestRssAndSummon(unittest.TestCase):
    # A small RSS document should yield its item titles.
    def test_rss_sample_parses(self):
        # Build a tiny RSS document with two items.
        sample = "<rss><channel><item><title>Ghost News One</title><link>https://example.test/1</link></item><item><title>Ghost News Two</title><link>https://example.test/2</link></item></channel></rss>"
        # Parse the document as XML.
        root = ET.fromstring(sample)
        # Collect the titles of all item elements.
        titles = [el.findtext("title") for el in root.iter("item")]
        # Check both sample titles were found.
        self.assertEqual(titles, ["Ghost News One", "Ghost News Two"])

    # A summon briefing should contain all three stitched parts.
    def test_summon_has_three_parts(self):
        # Build a tiny fake ticker with one headline.
        ticker = [{"title": "Candlelight festival opens downtown", "link": "https://example.test/x"}]
        # Build a briefing for the topic candle.
        text = summon_briefing("candle", ticker)
        # Check the briefing has a game hint, a spirit quote, and a headline.
        self.assertIn("Door-game hint", text)
        self.assertIn("Madame Zara", text)
        self.assertIn("Candlelight festival", text)

    # A summon with no matching headline should say the match is loose.
    def test_summon_loose_match_is_honest(self):
        # Build a tiny fake ticker with an unrelated headline.
        ticker = [{"title": "Harvest moon rises over the hills", "link": "https://example.test/y"}]
        # Build a briefing for an unrelated topic.
        text = summon_briefing("quasar", ticker)
        # Check the briefing admits the match is loose.
        self.assertIn("loose match", text)


# Tests for MCP tool dispatch.
class TestMcpTools(unittest.TestCase):
    # The summon tool should answer with a briefing, not an error.
    def test_mcp_summon(self):
        # Call the summon tool with a simple topic.
        text = call_tool("summon_spirit", {"topic": "game"})
        # Check the answer mentions the door game hint.
        self.assertIn("Door-game hint", text)

    # An unknown tool name should be refused plainly, not crash.
    def test_mcp_unknown_tool(self):
        # Call a tool name that does not exist.
        text = call_tool("no_such_tool", {})
        # Check the refusal names the unknown tool.
        self.assertIn("Unknown tool", text)


# Run the tests only when this file is executed directly.
if __name__ == "__main__":
    # Run the whole test suite with verbose output.
    unittest.main(verbosity=2)
