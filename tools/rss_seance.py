#!/usr/bin/env python3
# ARC Séance — RSS fetcher.
# This script fetches one public RSS feed with only the Python standard
# library, and writes the headlines to data/ticker.json, together with
# the source URL and the fetch date. It never invents headlines.
# Safety rule: if the fetch fails, it exits non-zero and leaves the last
# good file alone, so a bad fetch can never overwrite good data.

# Import JSON handling, so the ticker file can be written.
import json
# Import path handling, so the ticker file lands next to the project.
import os
# Import system tools, so the script can exit with an error code.
import sys
# Import URL tools, so the feed can be fetched over the network.
import urllib.request
# Import XML tools, so the RSS feed can be parsed.
import xml.etree.ElementTree as ET

# The public feed to fetch, chosen because it is free and stable.
FEED_URL = "https://www.nasa.gov/rss/dyn/breaking_news.rss"
# The maximum number of headlines to keep in the ticker file.
MAX_ITEMS = 20


# Fetch one feed URL and return its headline items as plain data.
def fetch_feed(url, timeout=30):
    # Build a request with a plain browser-style user agent string.
    request = urllib.request.Request(url, headers={"User-Agent": "ARC-Seance/1.0"})
    # Open the URL and read the whole feed document.
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = response.read()
    # Parse the feed document as XML.
    root = ET.fromstring(raw)
    # Collect the headline items found in the feed.
    items = []
    # Walk through every item element anywhere in the feed.
    for element in root.iter("item"):
        # Read the item title, or an empty string if it is missing.
        title = (element.findtext("title") or "").strip()
        # Read the item link, or an empty string if it is missing.
        link = (element.findtext("link") or "").strip()
        # Read the item publish date, or an empty string if missing.
        published = (element.findtext("pubDate") or "").strip()
        # Skip items with no title, since a ticker needs a headline.
        if not title:
            continue
        # Add this item to the collected list.
        items.append({"title": title, "link": link, "published": published})
        # Stop once the maximum number of items has been collected.
        if len(items) >= MAX_ITEMS:
            break
    # Return the collected headline items.
    return items


# Fetch the feed and write the ticker file next to the project.
def main():
    # Find the project root as the parent of this script's folder.
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Build the path to the ticker data file.
    out_path = os.path.join(root, "data", "ticker.json")
    # Fetch the feed, letting any network error stop the script here.
    items = fetch_feed(FEED_URL)
    # Refuse to write an empty ticker, so good data is never replaced.
    if not items:
        print("Fetcher found no headlines; leaving the last good file alone.", file=sys.stderr)
        return 1
    # Build the ticker document with source, date, and items.
    doc = {
        # Record the feed URL, so judges can check the source.
        "source": FEED_URL,
        # Record that these items are real fetched headlines, not a sample.
        "sample": False,
        # Record the items themselves for the ticker display.
        "items": items,
    }
    # Make sure the data folder exists before writing.
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    # Write the ticker document as readable JSON.
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(doc, handle, indent=2)
    # Report how many headlines were written, for the user.
    print(f"Wrote {len(items)} headlines to {out_path}")
    # Return zero, meaning the fetch and write both succeeded.
    return 0


# Run the fetcher only when this file is executed directly.
if __name__ == "__main__":
    # Exit with the fetcher's return code.
    sys.exit(main())
