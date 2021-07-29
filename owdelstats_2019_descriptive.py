import pandas as pd
import numpy as np
import datetime as dt
import csv
from scipy import stats
import matplotlib.pyplot as plt


def timeupdate(timeteam, eventdate):
    if ratings[timeteam][2] == 0:
        ratings[timeteam][2] = eventdate
    else:
        dayssince = (eventdate - ratings[timeteam][2]).days
        for i in range(2):
            for k in range(2):
                ratings[timeteam][i][k] = (ratings[timeteam][i][k] - 1) * .975**dayssince + 1
        ratings[timeteam][2] = eventdate


def ratingsupdate(offense_team, defense_team, score_rate, opportunities):
    offense_distribution = stats.beta.rvs(
        ratings[offense_team][0][0], ratings[offense_team][0][1], size=sampling_size)
    defense_distribution = stats.beta.rvs(
        ratings[defense_team][1][0], ratings[defense_team][1][1], size=sampling_size)
    offense_samples = []
    defense_samples = []
    for i in range(sampling_size):
        random_offense_score = stats.binom.cdf(score_rate*opportunities,
                                               opportunities, defense_distribution[i])
        random_defense_score = stats.binom.cdf(
            score_rate*opportunities, opportunities, offense_distribution[i])
        offense_samples.append(random_offense_score)
        defense_samples.append(random_defense_score)
    offensive_performance = np.mean(offense_samples)
    defensive_performance = np.mean(defense_samples)
    converted_O_efficiency = np.quantile(league_average_distribution, offensive_performance)
    converted_D_efficiency = np.quantile(league_average_distribution, defensive_performance)

    ratings[offense_team][0][0] += converted_O_efficiency*opportunities
    ratings[offense_team][0][1] += (1-converted_O_efficiency)*opportunities
    ratings[defense_team][1][0] += converted_D_efficiency*opportunities
    ratings[defense_team][1][1] += (1-converted_D_efficiency)*opportunities


def paceupdate(team, goals_for, goals_against):
    ratings[team][3] *= .7
    ratings[team][3] += .3*(int(goals_for)+int(goals_against))


def update(event):
    gamedate = dt.date.fromisoformat(event[0])
    awayteam = event[1]
    hometeam = event[4]
    awaygoals = event[2]
    homegoals = event[5]
    awayefficiency = event[3]
    homeefficiency = event[6]
    timeupdate(awayteam, gamedate)
    timeupdate(hometeam, gamedate)
    ratingsupdate(awayteam, hometeam, float(awayefficiency.strip('%'))/100, int(homegoals))
    ratingsupdate(hometeam, awayteam, float(homeefficiency.strip('%'))/100, int(awaygoals))
    paceupdate(awayteam, awaygoals, homegoals)
    paceupdate(hometeam, homegoals, awaygoals)


teams = [
    "AlleyCats", "Aviators", "Breeze", "Cannons", "Cascades", "Empire",
    "Flyers", "Growlers", "Hustle", "Mechanix", "Outlaws", "Phoenix",
    "Radicals", "Roughnecks", "Royal", "Rush", "Sol", "Spiders",
    "Thunderbirds", "Union", "Wind Chill"
]

ratings = {}
gamesdata = []
sampling_size = 100
league_average_distribution = stats.norm.rvs(loc=.65, scale=.1, size=sampling_size)

for team in teams:
    ratings[team] = [[13, 7], [13, 7], 0, 41]

with open('2019stats.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        gamesdata.append(row)

for game in gamesdata:
    update(game)
    print("UPDATED: " + str(game))

for team in teams:
    print(team + " O rating at the end of the season is " +
          str(ratings[team][0][0]/(ratings[team][0][0] + ratings[team][0][1])))
    print(team + " D rating at the end of the season is " +
          str(ratings[team][1][0]/(ratings[team][1][0] + ratings[team][1][1])))
