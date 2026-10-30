#!/usr/bin/env python3
# ARC Séance — real IRC protocol client, optional.
# This file speaks the IRC protocol with only the Python standard
# library: connect, register, join, send, answer pings, parse lines.
# It is optional on purpose: the local #seance channel works with no
# network at all, and this client is only used when a user asks for a
# real server. Every failure here is reported plainly, never hidden.

# Import socket tools, so this file can open a network connection.
import socket


# Parse one raw IRC line into its parts, for tests and for the client.
def parse_irc_line(line):
    # Start with no prefix, no command, and no arguments.
    prefix = None
    # Strip the trailing newline characters, if any are present.
    line = line.rstrip("\r\n")
    # If the line starts with a colon, the first word is the prefix.
    if line.startswith(":"):
        # Split off the prefix word, keeping the rest as the remainder.
        prefix, line = line[1:].split(" ", 1)
    # Split the remainder on the trailing part marker, if present.
    if " :" in line:
        # Split the line into the head part and the trailing part.
        head, trailing = line.split(" :", 1)
        # Split the head into words, then append the trailing part.
        parts = head.split() + [trailing]
    else:
        # With no trailing part, split the whole line into words.
        parts = line.split()
    # Take the command word, or an empty string if there is none.
    command = parts[0] if parts else ""
    # Take everything after the command as the arguments.
    args = parts[1:] if len(parts) > 1 else []
    # Return the parsed pieces as a small dictionary.
    return {"prefix": prefix, "command": command, "args": args}


# A tiny IRC client that talks to one server and one channel.
class IrcClient:
    # Remember the server, port, nickname, and channel for this client.
    def __init__(self, server, port, nickname, channel):
        # Store the server hostname the client will connect to.
        self.server = server
        # Store the port number the client will connect on.
        self.port = port
        # Store the nickname the client will register with.
        self.nickname = nickname
        # Store the channel the client will join after registering.
        self.channel = channel
        # Start with no open socket yet.
        self.sock = None
        # Start with an empty buffer for half-read lines.
        self.buffer = ""

    # Open the connection, register, and join the channel.
    def connect(self, timeout=15):
        # Create a TCP socket for the connection.
        self.sock = socket.create_connection((self.server, self.port), timeout=timeout)
        # Send the nickname registration line to the server.
        self._send(f"NICK {self.nickname}")
        # Send the user registration line to the server.
        self._send(f"USER {self.nickname} 0 * :ARC Seance visitor")
        # Send the join line for the chosen channel.
        self._send(f"JOIN {self.channel}")
        # Return true, meaning the connection step finished.
        return True

    # Send one raw line to the server, with a newline at the end.
    def _send(self, line):
        # Encode the line as bytes and append the IRC newline pair.
        self.sock.sendall((line + "\r\n").encode("utf-8", "ignore"))

    # Send a chat message to the joined channel.
    def say(self, message):
        # Format the message as a PRIVMSG to the channel.
        self._send(f"PRIVMSG {self.channel} :{message}")

    # Read lines until one chat message arrives, answering pings.
    def read_message(self, timeout=15):
        # Set the socket timeout, so a silent server cannot hang forever.
        self.sock.settimeout(timeout)
        # Loop until a chat message arrives or the socket closes.
        while True:
            # Read a chunk of bytes from the server.
            chunk = self.sock.recv(4096)
            # Stop cleanly if the server closed the connection.
            if not chunk:
                return None
            # Decode the chunk and append it to the line buffer.
            self.buffer += chunk.decode("utf-8", "ignore")
            # Process every complete line now sitting in the buffer.
            while "\n" in self.buffer:
                # Split off the first complete line from the buffer.
                line, self.buffer = self.buffer.split("\n", 1)
                # Parse the line into its parts.
                parsed = parse_irc_line(line)
                # Answer server pings at once, so the server stays happy.
                if parsed["command"] == "PING":
                    # Send back a PONG with the same trailing argument.
                    self._send(f"PONG :{parsed['args'][0] if parsed['args'] else ''}")
                    # Keep waiting, since a ping is not a chat message.
                    continue
                # Return chat messages to the caller as a small dictionary.
                if parsed["command"] == "PRIVMSG":
                    # Return who sent it, where it went, and what it said.
                    return {
                        "from": parsed["prefix"],
                        "target": parsed["args"][0] if parsed["args"] else "",
                        "text": parsed["args"][1] if len(parsed["args"]) > 1 else "",
                    }
                # Ignore all other server lines and keep waiting.
                continue
