import requests
import csv
from bs4 import BeautifulSoup


def add(gameurl):
    gamepage = "https://theaudl.com" + gameurl
    gpage = requests.get(gamepage)
    gamecontent = BeautifulSoup(gpage.content, "html.parser")
    gamedate = gameurl[13:23]
    teamnames = gamecontent.find_all(class_="audl-team-name")
    awayteam = teamnames[0].text.strip()
    hometeam = teamnames[1].text.strip()
    teamscores = gamecontent.find_all(class_="audl-game-score")
    awayscore = teamscores[0].text.strip()
    homescore = teamscores[1].text.strip()
    awayefficiencies = gamecontent.find_all(
        class_="views-field views-field-stat-away")
    awayefficiency = awayefficiencies[3].text.strip()
    homeefficiencies = gamecontent.find_all(
        class_="views-field views-field-stat-home")
    homeefficiency = homeefficiencies[3].text.strip()
    data.append([
        gamedate, awayteam, awayscore, awayefficiency, hometeam, homescore,
        homeefficiency
    ])


def writetocsv(gameslist):
    with open('2019stats.csv', 'w') as stats_file:
        for game in gameslist:
            csv.writer(stats_file).writerow(game)


data = [[
    "Date", "Away Team", "Away Score", "Away Hold %", "Home Team",
    "Home Score", "Home Hold %"
]]

for p in range(7):
    print("running page" + str(p))
    homepage = "https://theaudl.com/league/game?page=" + str(p)
    hpage = requests.get(homepage)
    homecontent = BeautifulSoup(hpage.content, "html.parser")
    gamecenters = homecontent.find_all(class_="audl-schedule-game-center")
    for gamecenter in gamecenters:
        a = gamecenter.find("a")
        link = a.get('href')
        add(link)

print(data)
writetocsv(data)
