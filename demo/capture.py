#!/usr/bin/env python3
# ARC Séance — demo capture script.
# Serves the web app locally, drives it with Playwright in a real
# Chromium browser, types the exact demo commands, and saves one
# screenshot after each step. The screenshots are real app footage,
# not mockups: the app code running is the submitted app code.
import os
import subprocess
import sys
import time

# The demo steps: (filename, command to type or None for boot shot).
STEPS = [
    ("01_boot.png", None),
    ("02_help.png", "help"),
    ("03_play.png", "play"),
    ("04_take_candle.png", "take candle"),
    ("05_go_north.png", "go north"),
    ("06_take_key.png", "take key"),
    ("07_go_east.png", "go east"),
    ("08_take_grimoire.png", "take grimoire"),
    ("09_go_west.png", "go west"),
    ("10_win.png", "go north"),
    ("11_say_hello.png", "say hello"),
    ("12_rss.png", "rss"),
    ("13_seance.png", "seance candle"),
]


def main():
    # Find the repo root (two folders up from this script's folder).
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # The repo root is the app folder itself in this layout.
    app_dir = root
    # Make the frames folder for screenshots.
    frames = os.path.join(app_dir, "demo", "frames")
    os.makedirs(frames, exist_ok=True)
    # Start a local static server for the app, on port 8123.
    server = subprocess.Popen(
        [sys.executable, "-m", "http.server", "8123"],
        cwd=app_dir,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        # Wait briefly for the server to start listening.
        time.sleep(2)
        # Import Playwright only after the server is up.
        from playwright.sync_api import sync_playwright

        # Drive a real Chromium browser, headless, at demo size.
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1280, "height": 720})
            # Open the app from the local server.
            page.goto("http://127.0.0.1:8123/index.html")
            # Wait for the boot lines and ticker load to finish.
            page.wait_for_timeout(1500)
            # Walk through the demo steps, screenshotting each one.
            for filename, command in STEPS:
                # Type the command and press Enter, if this step has one.
                if command:
                    page.fill("#cmd", command)
                    page.press("#cmd", "Enter")
                    # Wait for the app to print its answer.
                    page.wait_for_timeout(700)
                # Save a full-page screenshot for this step.
                page.screenshot(path=os.path.join(frames, filename), full_page=True)
                print(f"shot {filename} (command: {command})")
            browser.close()
    finally:
        # Stop the local server, whatever happened above.
        server.terminate()
    print(f"Done. Frames in {frames}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
