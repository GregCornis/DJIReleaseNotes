#!/Library/Frameworks/Python.framework/Versions/3.9/bin/python3

from bs4 import BeautifulSoup
from dataclasses import dataclass
from pathlib import Path
import requests

DOWNLOAD_PAGE = "https://developer.dji.com/mobile-sdk/downloads/"
RELEASE_TXT_PATH = Path(__file__).parent / "last_releases.txt"

@dataclass
class Link:
    name: str
    url: str

    @staticmethod
    def from_div(div):
        return Link(div.get("data-ga"), div.get("data-href"))

def get_download_urls():
    r = requests.get(DOWNLOAD_PAGE)
    content = BeautifulSoup(r.content, "html.parser")
    links = content.find_all("a")
    release_divs = [link for link in links if link.string == "Release notes"]
    assert(len(release_divs) == 2)
    ios_div, android_div = release_divs
    return Link.from_div(ios_div), Link.from_div(android_div)

if __name__ == "__main__":
    ios, android = get_download_urls()
    text = f"""iOS: {ios.name}
Android: {android.name}"""
    with open(RELEASE_TXT_PATH, "r") as input:
        content = input.read()
    if content == text:
        print(f"Nothing new! ✅\n{text}")
    else:
        print("New version! 🔥")
        print(content)
        print("vs")
        print(text)
