import os
import requests
from bs4 import BeautifulSoup
URL = "https://www.pgnmentor.com/files.html#events"


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52"}

page = requests.get(URL, headers = headers)

# SELECTS ALL ANCHOR TAGS FROM TABLE 21, DEFAULT PARSER DID NOT WORK
# TODO FIND A BETTER WAY TO SELECT TABLE, CURRENT INDEX WAS FOUND MANUALLY
soup = BeautifulSoup(page.content, "lxml").find_all("table")[20].find_all("a")

# INITIALIZES A LIST TO STORE ALL ANCHORS' TEXT
allAnchors = []

# ADDS TEXT OF ALL ANCHORS TO A LIST
for a in soup:
    allAnchors.append(a.get_text())

# MAKES A LIST OF ALL EVENTS, HANDLES DUPLICATE EVENTS
eventNames = [anchor for anchor in allAnchors if anchor != "Download" and anchor != "View"]

# MAKES AN EMPTY "PGNs" FOLDER
os.mkdir(os.getcwd() + "\PGNs")
print("Made an empty PGNs folder...")

# DOWNLOADS PGNS BY VISITING GENERATED URL EACH ITERATION
print("Downloading PGNs. This can take several minutes...")
for event in eventNames:
    url = "https://www.pgnmentor.com/events/" + event
    path = "./PGNs/" + event
    downloadedObj = requests.get(url)

    with open(path, "wb") as file:
        file.write(downloadedObj.content)

print(f"Successfully downloaded {len(eventNames)} files!")