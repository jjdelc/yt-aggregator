
from os.path import basename
from datetime import datetime
from urllib.parse import urlparse
from urllib.request import urlopen
import xml.etree.ElementTree as ET

CSS = """
body {
font-family: sans-serif;
}
.main-feed {
list-style: None;
max-width: 40rem;
margin: 0 auto;
padding: 0;
}
.main-feed li {
margin-bottom: 0.5rem;
border: 1px solid #EEE;
}
.main-feed a {
display: grid;
grid-template-columns: 30% auto;
text-decoration: none;
color: #444;
}
.preview {
display: block;
max-width: 100%;
height: auto;
}
.video-info {
padding: 0 0.5rem;
box-sizing: border-box;
}
.video-info h1 {
font-size: 1rem;
}
"""

CHANNELS = [
"UCTitdGNU65UUwEG75sWoLEA",  # Cybertron 21
"UC90avc9FvlyP1PTH0QXluKg",  # peolesdru
"UCt6y380FcB6E4rdLae4o2sA",  # Peaugh
"UCVEDzEYSNi5FwEKmLY6LT0Q",  # Emgo316
"UCAPhTcmL-a69jL1KWOPe7GA",  # Chris McFeely
"UCTawVEKc2B7x23jwy_95oJg",  # Optibotimus
"UCUChzcoFWnmErS2U-kUOu4w",  # Tonton
"UCJVOioJ7oEFRq7pzVMZKa3A",  # Chefatron
"UCvTEl-XHO9BY3_I1Zssfmjg",  # Patriot Prime
"UClOs-_ohni8SfWRS6glsGIQ",  # Lazy Eyebrow
"UCP3AVTw_73U_8jMzLw5TbEg",  # Thew adams
"UCSavbCuXmMyRzN0mjwB1uEQ",  # Vangelus
"UCx7b66RpQRLuOXvItxy0Wxg",  # Transformers official
"UCbQhXIBPC_1DbUDn0IdhRrQ",  # Cybertronian Beast
"UCmXbBLj_Iv1ElpJ7LIABdJQ",  # Ballmatrix
"UC8tA9aqVj587UzMmW7YTM4w",  # Knerdout
"UCzSYHWdPoWrA3BqI5JoHZ5g",  # Chosen Prime
"UCKl_L5vnewbZNMp8YutEE9Q",  # TM Reviews
"UCEOvklHZd3m5qNxtMis4zRQ",  # RodimusPrimal
"UCi7KR0GzS7veFC6IGKuYHKg",  # Transformers ENI
"UCoAIXvNjN5bYzMYNce0M3uw",  # Bens Collectables
"UC1Dt3QcVWHBIMYSjuZWzJNA",  # Toyhax
"UCnWxXRUOv5zvqbNiXzUNN8A",  # A3u
"UCzo0rWyQdCznorrvd-OzEBA",  # Masterpiece Reanimated
"UCA5e8vqo-aJpZtd7EEDEuDg",  # Transform My Transformers
"UCvU4TcenqcDTrkxaqGEedfw",  # Starscreamer
]

RSS_FEED = "https://www.youtube.com/feeds/videos.xml?channel_id=%s"
RSS_URL = "https://www.youtube.com/channel/{}/"
ENTRY_TAG = "{http://www.w3.org/2005/Atom}entry"
PREVIEW_IMG = "https://i.ytimg.com/vi/{}/hqdefault.jpg"
WATCH_URL = "https://www.youtube.com/watch?v={}"
MAX_ENTRIES = 100
FEED_ITEM = """<li>
<a href="{link}">
<img src="{image}" loading="lazy" class="preview"/>
<div class="video-info">
<h1>{title}</h1>
</div>
</a>
</li>"""


BASE_HTML = """<!doctype html>
<html>
<head>
<title>{title}</title>
<style>{css}</style>
</head>
<body>
    <ol class="main-feed">{feed}</ol>
</body>
</html>
"""

OUTPUT = "page.html"

def parse_tagname(tag):
    return tag.split("}", 1)[1]

def read_entry(entry):
    result = {parse_tagname(e.tag): e.text for e in entry}
    result["published"] = datetime.strptime(result['published'][:19], "%Y-%m-%dT%H:%M:%S")
    return result

def process_entry(entry):
    return {
        "title": entry["title"],
        "image": PREVIEW_IMG.format(entry["videoId"]),
        "link": WATCH_URL.format(entry["videoId"]),
    }


def entry_2_html(entry):
    return FEED_ITEM.format(**process_entry(entry))


def main():
    all_entries = []
    for channel_id in CHANNELS[:]:
        rss = urlopen(RSS_FEED % channel_id).read()
        root = ET.fromstring(rss)
        entries = [read_entry(e) for e in root if e.tag == ENTRY_TAG]
        all_entries.extend(entries)
    all_entries = reversed(sorted(all_entries, key=lambda e: e["published"]))
    html_entries = [entry_2_html(e) for e in all_entries[:MAX_ENTRIES]]
    html = BASE_HTML.format(
        title="YT Feed",
        feed="\n".join(html_entries),
        css=CSS
    )
    with open(OUTPUT, "w") as fh:
        fh.write(html)


if __name__ == "__main__":
    main()
