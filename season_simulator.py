import matplotlib.pyplot as plt
import pandas as pd
import owdelstats_2021_predictive as single_season

"""I need to: display team data: team wins, losses, ratings; record individual sim data - win title, make championship weekend, make playoffs, win games; aggregate it, visuals"""

aggregated_seasons = {}
game_outcomes = {}
season_sims = 10

for i in range(season_sims):
    print("running sim " + str(i+1))
    single_season.run()
    for game in single_season.season_results:
        if game in aggregated_seasons:
            aggregated_seasons[game].append(single_season.season_results[game])
        else:
            aggregated_seasons[game] = [single_season.season_results[game]]

print(aggregated_seasons)
for game in aggregated_seasons:
    gamewinners = {}
    for team in single_season.priors.teams:
        gamewinners[team] = 0
    for team in aggregated_seasons[game]:
        gamewinners[team] += 1
    game_outcomes[game] = gamewinners
print(game_outcomes)

sim_table = pd.DataFrame(game_outcomes)
sim_table = sim_table.transpose()
pd.set_option("display.max_rows", None, "display.max_columns", None)
print(sim_table)

for (team, data) in sim_table.iteritems():
    playoff_chances = sum(
        sim_table.loc[['A1', 'A2', 'A3', 'A4', 'C1', 'C2', 'W1', 'W2'], team]) / season_sims
    cw_chances = sum(
        sim_table.loc[['EastPlayoffs1', 'EastPlayoffs2', 'CentralPlayoffs', 'WestPlayoffs'], team]) / season_sims
    finals_chances = sum(sim_table.loc[['Semi1', 'Semi2'], team]) / season_sims
    championship_chances = sim_table.loc['Finals', team] / season_sims
    print(team + " chances - " + "Playoffs: " + str(playoff_chances) + " Champ Weekend: " +
          str(cw_chances) + " Finals: " + str(finals_chances) + " Champions: " + str(championship_chances))
