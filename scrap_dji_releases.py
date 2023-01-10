#!/Library/Frameworks/Python.framework/Versions/3.9/bin/python3

from curses.panel import version
import datetime
from dateutil import parser
import subprocess
from dataclasses import dataclass
from pathlib import Path
import json

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
    assert(len(release_divs) == 1)
    android_div = release_divs[0]
    return Link.from_div(android_div)

def get_latest_release(repo):
    res = subprocess.check_output(["gh", "api", f"repos/{repo}/releases"])
    releases = json.loads(res)
    last_date = datetime.datetime.fromtimestamp(0, tz=datetime.timezone.utc)
    last_release = "none"
    for release in releases:
        date = parser.parse(release["created_at"])
        if date > last_date:
            last_release = release["name"]
            last_date = date
    return last_release, last_date

def get_latest_tag(repo):
    res = subprocess.check_output(["gh", "api", f"repos/{repo}/tags"])
    tags = json.loads(res)
    last_date = datetime.datetime.fromtimestamp(0, tz=datetime.timezone.utc)
    last_tag = "none"
    for tag in tags:
        # fetch date
        sha = tag["commit"]["sha"]
        commit = json.loads(subprocess.check_output(["gh", "api", f"repos/{repo}/commits/{sha}?per_page=1"]))
        #print(commit["commit"])
        date = parser.parse(commit["commit"]["author"]["date"])
        if date > last_date:
            last_tag = tag["name"]
            last_date = date
    return last_tag, last_date

def fetch_latest_version():
    return {
        "Android v5": get_latest_release("dji-sdk/Mobile-SDK-Android-V5"),
        "iOs v4": get_latest_tag("dji-sdk/Mobile-SDK-iOS"),
        "Android v4": get_latest_tag("dji-sdk/Mobile-SDK-Android")
    }

def describe_versions():
    versions = fetch_latest_version()
    desc = ""
    for repo, version in versions.items():
        desc += f"{repo}: {version[0]} ({version[1].date()})\n"
    return desc

if __name__ == "__main__":
    # print(get_latest_release("dji-sdk/Mobile-SDK-Android-V5"))
    # print(get_latest_tag("dji-sdk/Mobile-SDK-iOS"))
    # print(get_latest_tag("dji-sdk/Mobile-SDK-Android"))
    # res = subprocess.check_output(["gh", "api", "repos/dji-sdk/Mobile-SDK-Android-V5/releases"])
    versions = describe_versions()
    with open(RELEASE_TXT_PATH, "r") as input:
        content = input.read()
    if content == versions:
        print(f"Nothing new! ✅\n{versions}")
    else:
        print("New version! 🔥")
        print(versions)
        print("vs")
        print(content)
