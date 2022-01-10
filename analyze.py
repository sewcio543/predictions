import numpy as np
import outcome
from csv import reader
import pandas as pd
from outcome import findTeams

# function gets as arguments actual result and analyze it based on predictions from outcome.py
def analyze(league, home, away, hScore, aScore):
    pass
    with open("Analysis" + league + ".csv", 'r') as fileR:
        # check if line already exists
        exists = True if np.array([",".join(line[:2]) == f"{home},{away}" for line in reader(fileR)]).any() else False
    if not exists:
        out = outcome.prediction(league, home, away, analysis=True)
        # these are probabilities for each result
        ref = {'H': out[2][0], 'D': out[2][1], 'A': out[2][2]}
        # we check who won the game
        if hScore > aScore:
            result = 'H'
        elif hScore == aScore:
            result = 'D'
        else:
            result = 'A'
        # and it is sent to csv file with analysis
        stringBuilder = f"{home},{away},{hScore},{aScore},{out[0]},{out[1]},{ref[result]},{out[3].values[int(aScore), int(hScore)]}\n"
        with open("Analysis" + league + ".csv", 'a') as fileA:
           fileA.write(stringBuilder)

def predictionAcc(league):
    data = pd.read_csv(f"Analysis{league}.csv").to_numpy()
    stats = dict()
    teams = findTeams(league)[0]
    for team in teams:
        AE, matches = 0, 0
        for row in data:
            if row[0] == team:
                AE += abs(row[2] - row[4])
                matches += 1
            if row[1] == team:
                AE += abs(row[3] - row[5])
                matches += 1
        MAE = AE / matches
        stats[team] = round(MAE, 2)

    leagueMAE = round(
        np.array([abs(row[4] - row[2]) + abs(row[5] - row[3]) for row in data]).sum() / (data.shape[0] * 2), 2)
    return leagueMAE, stats

#without outliers
def predict(league):
    data = pd.read_csv(f"Analysis{league}.csv").to_numpy()
    stats = []
    for row in data:
        stats.append(abs(row[2] - row[4]))
        stats.append(abs(row[3] - row[5]))
    iqr = np.quantile(stats, 0.75) - np.quantile(stats, 0.25)
    stats = np.array(stats)
    a = np.argwhere(stats < np.quantile(stats, 0.75) + iqr)
    b = np.argwhere(stats > np.quantile(stats, 0.25) - iqr)
    args = [x for x in a if x in b]
    stats = stats[args]
    return round(np.mean(stats), 3)
