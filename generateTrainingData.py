import re
import os
import csv
import glob
import random
import requests
from bs4 import BeautifulSoup


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52"}

# INITIALZES A LIST TO STORE FINAL DATA
megaList = [["ID", "whiteElo", "blackElo", "result", "eloChange"]]

# CALCULATES ELO CHANGE LOCALLY
def calcEloChange(wElo, bElo, res):
    expW = 1 / (1 + 10**((bElo - wElo) / 400))
    return 10*(res - expW)


# ITERATES OVER EVERY FILE IN "Data" FOLDER
pathToPGNs = os.getcwd() + "\PGNs\*.pgn" #PATH TO .pgn FILES IN THE "PGNs" FOLDER
for foo in glob.glob(pathToPGNs):
    fileName = os.path.split(foo)[-1]
    path = "./PGNs/" + fileName
    fHandle = open(path, "r")
    fData = fHandle.read()

    # RESETS COUNTER FOR EVERY FILE
    counter = 1

    # FOR EACH PGN FILE, MATCHES EVERY PGN WHILE IGNORING MOVES & TIMES
    for gameMatchObj in re.finditer("(\[.*\]\n)+", fData):
        game = fData[gameMatchObj.start():gameMatchObj.end()] # STRING PGN

        # GETS WHITE ELO FROM THE PGN
        whiteEloMatchObj = re.search("\[WhiteElo \".*\"]", game) # MATCHES [WhiteElo "1234"], RETURNS MATCH OBJECT
        whiteEloMatchStr = game[whiteEloMatchObj.start() : whiteEloMatchObj.end()] # STRING "[WhiteElo "1234"]"
        whiteEloValueMatchObj = re.search("\".*\"",whiteEloMatchStr) # MATCHES "1234", RETURNS MATCH OBJECT
        whiteEloValueStr = whiteEloMatchStr[whiteEloValueMatchObj.start()+1 : whiteEloValueMatchObj.end()-1] # STRING "1234"

        # GETS BLACK ELO FROM THE PGN
        blackEloMatchObj = re.search("\[BlackElo \".*\"]", game) # MATCHES [BlackElo "1234"], RETURNS MATCH OBJECT
        blackEloMatchStr = game[blackEloMatchObj.start() : blackEloMatchObj.end()] # STRING "[BlackElo "1234"]"
        blackEloValueMatchObj = re.search("\".*\"",blackEloMatchStr) # MATCHES "1234", RETURNS MATCH OBJECT
        blackEloValueStr = blackEloMatchStr[blackEloValueMatchObj.start()+1 : blackEloValueMatchObj.end()-1] # STRING "1234"

        # GETS RESULT FROM THE PGN
        resultMatchObj = re.search("\[Result \".*\"]", game) # MATCHES [Result "1/2-1/2"], RETURNS MATCH OBJECT
        resultMatchStr = game[resultMatchObj.start() : resultMatchObj.end()] # STRING "[Result "1/2-1/2"]"
        resultValueMatchObj = re.search("\".*\"",resultMatchStr) # MATCHES "1/2-1/2", RETURNS MATCH OBJECT
        resultValueStr = resultMatchStr[resultValueMatchObj.start()+1 : resultValueMatchObj.end()-1] # STRING "1/2-1/2"

        # FILTERS OUT INSTANCES OF MISSING DATA
        if not whiteEloValueStr or not blackEloValueStr or not resultValueStr: continue

        ID = fileName[0] + fileName[-5] + "#" + str(counter)
        whiteElo = int(whiteEloValueStr)
        blackElo = int(blackEloValueStr)
        if resultValueStr == "1-0": result = 1
        elif resultValueStr == "0-1": result = 0
        elif resultValueStr == "1/2-1/2": result = 1/2

        counter += 1

        # METHOD BELOW IS PREFERABLE BUT TAKES ~12 HOURS FOR ALL ~28,000 GAMES
        # URL = f"https://ratings.fide.com/calc_rtd.php?f_ro={whiteElo}&f_rc={blackElo}&f_w={result}&f_k=10&sid={random.random()}"
        # page = requests.get(URL, headers = headers)
        # soup = BeautifulSoup(page.content, "lxml").find("font")
        # eloChange = float(soup.get_text())

        # CALCULATES ELO CHANGE
        # LESS PREFERABLE BUT FASTER THAN ABOVE METHOD
        eloChange  = round(calcEloChange(whiteElo, blackElo, result), 1)

        # APPENDS CURRENT DATA TO MEGA LIST
        megaList.append([ID, whiteElo, blackElo, result, eloChange])


# MAKES A CSV FROM THE MEGA LIST
with open("data.csv", "w", newline='') as outfile: 
    wr = csv.writer(outfile, delimiter=',')
    wr.writerows(megaList)

print("Successfully generated data.csv")