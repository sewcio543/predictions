import numpy as np
from csv import reader


# function gets as arguments actual result and analyze it based on predictions from outcome.py
# .classes Match object
def analyze(match, hScore: int, aScore: int) -> None:
    with open(match.league.analysisFile, 'r') as fileR:
        # check if line already exists
        exists: bool = True if np.array(
            [",".join(line[:2]) == f"{match.homeTeam.name},{match.awayTeam.name}" for line in
             reader(fileR)]).any() else False
    if not exists:
        # these are probabilities for each result
        ref: dict[str: float] = {'H': match.homeWinProbability, 'D': match.tieProbability,
                                 'A': match.awayWinProbability}
        # we check who won the game
        if hScore > aScore:
            result = 'H'
        elif hScore == aScore:
            result = 'D'
        else:
            result = 'A'
        # and it is sent to csv file with analysis
        stringBuilder: str = f"{match.homeTeam},{match.awayTeam},{hScore},{aScore},{match.expectedHomeScore},{match.expectedAwayScore},{ref[result]},{match.scoresTable.values[int(aScore), int(hScore)]}\n"
        with open(match.league.analysisFile, 'a') as fileA:
            fileA.write(stringBuilder)

# .classes League Team
def predictionAccTeam(team) -> float:
    AE, matches = 0, 0
    for row in team.league.analysis:
        if row[0] == team.name:
            AE += abs(row[2] - row[4])
            matches += 1
        if row[1] == team.name:
            AE += abs(row[3] - row[5])
            matches += 1
    return round(AE / matches, 2)


# without outliers
# .classes League object
def predict(league):
    stats = []
    for row in league.analysis:
        stats.append(abs(row[2] - row[4]))
        stats.append(abs(row[3] - row[5]))
    iqr = np.quantile(stats, 0.75) - np.quantile(stats, 0.25)
    stats = np.array(stats)
    a = np.argwhere(stats < np.quantile(stats, 0.75) + iqr)
    b = np.argwhere(stats > np.quantile(stats, 0.25) - iqr)
    args = [x for x in a if x in b]
    stats = stats[args]
    return round(np.mean(stats), 3)


