
from os.path import basename
from urllib.parse import urlparse
from urllib.request import urlopen
import xml.etree.ElementTree as ET

RSS_FEED = "https://www.youtube.com/feeds/videos.xml?channel_id=%s"
RSS_URL = "https://www.youtube.com/channel/UCTitdGNU65UUwEG75sWoLEA/"
ENTRY_TAG = "{http://www.w3.org/2005/Atom}entry"
PREVIEW_IMG = "https://i.ytimg.com/vi/%s/hqdefault.jpg"
WATCH_URL = "https://www.youtube.com/watch?v=%s"

def parse_tagname(tag):
    return tag.split("}", 1)[1]

def read_entry(entry):
    result = {parse_tagname(e.tag): e.text for e in entry}
    return result

def process_entry(entry):
    return {
        "title": entry["title"],
        "image": PREVIEW_IMG % entry["videoId"],
        "link": WATCH_URL % entry["videoId"],
    }


def main():
    channel_id = basename(urlparse(RSS_URL).path.rstrip('/'))
    rss = urlopen(RSS_FEED % channel_id).read()
    root = ET.fromstring(rss)
    print(rss)
    entries = [read_entry(e) for e in root if e.tag == ENTRY_TAG]
    import pdb; pdb.set_trace()


if __name__ == "__main__":
    main()
