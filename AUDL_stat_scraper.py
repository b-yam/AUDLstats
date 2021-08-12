import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup


def add(gameurl):
    driver.get("https://theaudl.com" + gameurl)
    print("running: " + str(gameurl))
    away_scores = driver.find_element_by_xpath(
        '//*[@id="stats-pages"]/div[1]/div[2]/div/table/tbody/tr[1]')
    away_scores = away_scores.find_elements_by_tag_name("td")
    away_scores = away_scores[-1]
    home_scores = driver.find_element_by_xpath(
        '//*[@id="stats-pages"]/div[1]/div[2]/div/table/tbody/tr[2]')
    home_scores = home_scores.find_elements_by_tag_name("td")
    home_scores = home_scores[-1]
    game_goals = int(away_scores.text.strip()) + int(home_scores.text.strip())
    turnovers_row = driver.find_element_by_xpath(
        '//*[@id="stats-pages"]/div[1]/div[3]/div[2]/table/tbody/tr[7]')
    turn_values = turnovers_row.find_elements_by_tag_name("td")
    game_turns = int(turn_values[0].text.strip()) + int(turn_values[1].text.strip())
    game_scoring_efficiency = game_goals/(game_goals + game_turns)
    stats_rows = driver.find_elements_by_xpath(
        '//*[@class="rt-tr-group"]')
    for row in stats_rows:
        row_stats = []
        filtered_row_stats = []
        filtered_row_stats.append(gameurl[12:22])
        row_stats = row.find_elements_by_class_name("rt-td")
        for stat in row_stats:
            filtered_row_stats.append(stat.text.strip())
        filtered_row_stats.append(game_scoring_efficiency)
        data.append(filtered_row_stats)


def writetocsv(gameslist):
    with open('2021_player_stats.csv', 'w') as stats_file:
        for game in gameslist:
            csv.writer(stats_file).writerow(game)


data = [[
    "Date", "Name", "Team", "#", "PP", "OPP", "DPP", "AST", "GLS", "BLK", "+/-",
    "Rcv Yds", "Thr Yds", "Yds", "Cmp", "Cmp%", "HA", "T", "S", "C", "D", "GSE"
]]

opts = Options()
opts.add_argument('--ignore-certificate-errors')
opts.add_argument('--incognito')
opts.add_argument('--headless')
driverpath = ("C:\\Users\\Ben Yam\\Downloads\\chromedriver_win32\\chromedriver.exe")
driver = webdriver.Chrome(driverpath, options=opts)
driver.implicitly_wait(5)


for p in range(7):
    gamepage = "https://theaudl.com/league/game?page=" + str(p)
    hpage = requests.get(gamepage)
    homecontent = BeautifulSoup(hpage.content, "html.parser")
    gamecenters = homecontent.find_all(class_="audl-schedule-box")
    for gamecenter in gamecenters:
        a = gamecenter.find("a")
        link = a.get('href')
        status = gamecenter.find(class_="audl-schedule-status").text
        if status == "Final":
            add("/stats" + link[7:])

print(data)
writetocsv(data)
