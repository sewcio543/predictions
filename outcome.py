import numpy as np
import pandas as pd
from scipy.stats import poisson
from tabulate import tabulate
from classes import Match, Team


pd.set_option('display.float_format', lambda x: '%.1f' % x)
np.set_printoptions(suppress=True)


def prediction(match: Match, realOdds: bool = False):
    import Betclic
    # string variable returned at the end
    stringBuilder = ""

    homeTeam, awayTeam = match.homeTeam.name, match.awayTeam.name

    stringBuilder += f"{match.__str__()}\n\nExpected Result:\n{match.expectedHomeScore} : {match.expectedAwayScore}\n\n"
    # expected result of the match

    # Poisson distribution for each value (probability of an event for each number of goals(30) to cover the whole margin and get all possible results)
    # in Poisson distribution probability of getting k is (lambda^k)*e^(-lambda)/k! where lambda is the expected value
    scoreMax = 30
    probabilityHome = [poisson.pmf(result, match.expectedHomeScore) for result in range(scoreMax)]
    probabilityAway = [poisson.pmf(result, match.expectedAwayScore) for result in range(scoreMax)]

    # results' probability based on Poisson distribution
    probabilityOfResult: np.ndarray = np.array(
        [homeResult * awayResult for awayResult in probabilityAway for homeResult in probabilityHome]).reshape(scoreMax,
                                                                                                               scoreMax)

    tableOfScores = tabulate(pd.DataFrame((probabilityOfResult[:6, :6] * 100).round(4)), headers='keys',
                             tablefmt='psql')

    # now it's time to sum up the probabilities and get the chances of a specific outcome
    tieProbability, homeWinProbability, awayWinProbability = 0, 0, 0

    # iterating through np array and summing up probabilities
    for row in range(probabilityOfResult.shape[0]):
        for column in range(probabilityOfResult.shape[1]):
            # that gives as a draw
            if row == column:
                tieProbability += probabilityOfResult[row, column]
            # away team win
            elif row > column:
                awayWinProbability += probabilityOfResult[row, column]
            # home team win
            else:
                homeWinProbability += probabilityOfResult[row, column]

    # times 100 to get the percentage value
    homeWinProbability = round(homeWinProbability * 100, 2)
    awayWinProbability = round(awayWinProbability * 100, 2)
    tieProbability = round(tieProbability * 100, 2)

    # adding probabilities to string builder
    stringBuilder += f"{homeTeam} : {homeWinProbability}%\ntie : {tieProbability}%\n{awayTeam} : {awayWinProbability}%\n"

    # to avoid division by 0, if probability of some results is 0 it is used try except
    # method to count expected odds is divide 100 by percentage value of probability of an occurrence of some event
    ExpectedOdds = [round(100 / homeWinProbability, 2) if homeWinProbability else 0,
                    round(100 / tieProbability, 2) if tieProbability else 0,
                    round(100 / awayWinProbability, 2) if awayWinProbability else 0]

    # probabilities of a specific results (each score in range 4)
    stringBuilder += f"\nScores and probabilities:\n{tableOfScores}\n"
    # the most probable outcome (index of the flatten np array probabilityOfResult)
    maxi = np.argmax(probabilityOfResult)
    # maxi % 30 is a number of the column (home team score), maxi/30 as int is a number of the row (away team score)
    stringBuilder += f"\nExpected result : {maxi % 30} : {int(maxi / 30)}"
    # 5 most probable outcomes (indices of sorted array in descending order with axis none (flatten array)
    arg = np.argsort(-probabilityOfResult, axis=None)[1:5]
    stringBuilder += "\nAlso: "
    for i in arg:
        # method as before
        stringBuilder += f"{i % 30}:{int(i / 30)}  "

    # summing all the scores in which both teams score at least one goal
    bttsChances = round(np.array(probabilityHome[1:]).sum() * np.array(probabilityAway[1:]).sum() * 100, 2)
    # getting real odds for particular events from Betclic.py functions
    # chance of -2.5 goals in the game
    under3 = round(
        (probabilityOfResult[0:3, 0].sum() + probabilityOfResult[0, 1:3].sum() + probabilityOfResult[1, 1]) * 100, 2)


    odds = {}
    if realOdds:
        odds = Betclic.betclicOdds(match)
        if not odds:
            stringBuilder += f"\n\n{homeTeam} : Expected Odds: {ExpectedOdds[0]}\ntie: Expected Odds: {ExpectedOdds[1]}\n{awayTeam} : Expected Odds: {ExpectedOdds[2]}\n \
                            \nBTTS: {bttsChances} % Expected Odds: (TAK: {round(100 / bttsChances, 2)}, NIE: {round(100 / (100 - bttsChances), 2)}) \
                            \n-2.5 : {under3}% Expected Odds: {round(100/under3,2)} \
                            \n+2.5 {round(100 - under3,2)}% Expected Odds: {round((100 / (100 - under3)), 2)}  \
                            \n1/X : {round(tieProbability + homeWinProbability, 2)}% Expected Odds: {round(100 / (tieProbability + homeWinProbability), 2)} \
                            \n2/X : {round(tieProbability + awayWinProbability, 2)}% Expected Odds: {round(100 / (tieProbability + awayWinProbability), 2)}"

            return [stringBuilder + '\n\nodds unavailable', homeWinProbability, tieProbability, awayWinProbability,
                    bttsChances, under3, pd.DataFrame(
                    (probabilityOfResult[:10, :10] * 100).round(1))]

        # odds and real probabilities for the results from betclic
        stringBuilder += f"\n\n{homeTeam} : Expected Odds: {ExpectedOdds[0]} Betclic: {odds['Wynik meczu (z wyłączeniem dogrywki)']['home team']}\n" \
                         f"tie: Expected Odds: {ExpectedOdds[1]} Betclic: {odds['Wynik meczu (z wyłączeniem dogrywki)']['Remis']}\n" \
                         f"{awayTeam} : Expected Odds: {ExpectedOdds[2]} Betclic: {odds['Wynik meczu (z wyłączeniem dogrywki)']['away team']}\n"

        # odds for btts
        stringBuilder += f"\nBTTS: {bttsChances} % Expected Odds: (TAK: {round(100/ bttsChances, 2)}, NIE: {round(100 / (100 - bttsChances), 2)}) " \
                         f"Betclic : (TAK: {odds['Oba zespoły strzelą gola']['Tak']}, NIE: {odds['Oba zespoły strzelą gola']['Nie']})"
        # odds for -+2.5
        stringBuilder += f"\n-2.5 : {under3}% Expected Odds: {round(100/under3,2)} Betclic : {odds['Gole Powyżej/Poniżej']['Poniżej 2,5']}" \
                         f"\n+2.5 {round(100 - under3, 2)}% Expected Odds: {round((100 / (100 - under3)), 2)} " \
                         f"Betclic : {odds['Gole Powyżej/Poniżej']['Powyżej 2,5']}\n"

        # odds for 1/x 2/x
        stringBuilder += f"1/X : {round(tieProbability + homeWinProbability, 2)}% Expected Odds: {round(100 / (tieProbability + homeWinProbability), 2)} Betclic: {odds['Podwójna szansa'][f'home team lub Remis']}\n" \
                         f"2/X : {round(tieProbability + awayWinProbability, 2)}% Expected Odds: {round(100 / (tieProbability + awayWinProbability), 2)} Betclic: {odds['Podwójna szansa'][f'Remis lub away team']}\n\n"

    else:
        stringBuilder += f"\n\n{homeTeam} : Expected Odds: {ExpectedOdds[0]}\ntie: Expected Odds: {ExpectedOdds[1]}\n{awayTeam} : Expected Odds: {ExpectedOdds[2]}\n \
                            \nBTTS: {bttsChances} % Expected Odds: (TAK: {round(100 / bttsChances, 2)}, NIE: {round(100 / (100 - bttsChances), 2)}) \
                            \n-2.5 : {under3}% Expected Odds: {round(100/under3,2)} \
                            \n+2.5 {100 - under3}% Expected Odds: {round((100 / (100 - under3)), 2)}  \
                            \n1/X : {round(tieProbability + homeWinProbability, 2)}% Expected Odds: {round(100 / (tieProbability + homeWinProbability), 2)} \
                            \n2/X : {round(tieProbability + awayWinProbability, 2)}% Expected Odds: {round(100 / (tieProbability + awayWinProbability), 2)}"



    return [stringBuilder, homeWinProbability, tieProbability, awayWinProbability, bttsChances, under3,
            pd.DataFrame((probabilityOfResult[:10, :10] * 100).round(1))]


def getOdds(match: Match) -> list[float]:
    import Betclic
    odds = Betclic.betclicOdds(match)
    if odds:
        homeWinOdds = odds['Wynik meczu (z wyłączeniem dogrywki)']['home team']
        tieOdds = odds['Wynik meczu (z wyłączeniem dogrywki)']['Remis']
        awayWinOdds = odds['Wynik meczu (z wyłączeniem dogrywki)']['away team']
        over2_5Odds = odds['Gole Powyżej/Poniżej']['Powyżej 2,5']
        under2_5Odds = odds['Gole Powyżej/Poniżej']['Poniżej 2,5']
        bttsOdds = odds['Oba zespoły strzelą gola']['Tak']
        nbttsOdds = odds['Oba zespoły strzelą gola']['Nie']
        x1 = odds['Podwójna szansa'][f'home team lub Remis']
        x2 = odds['Podwójna szansa'][f'Remis lub away team']
        return [homeWinOdds, tieOdds, awayWinOdds, bttsOdds, nbttsOdds, under2_5Odds, over2_5Odds, x1, x2]
    return []


def strengths(team: Team, streak: float = 1.3):
    # variables contain numbers of matches played at home and away and goals scored and conceded
    HomeGoalsScored, AwayGoalsScored, HomeMatches, AwayMatches, HomeGoalsConceded, AwayGoalsConceded = 0, 0, 0, 0, 0, 0
    # last 5 rounds goals are multiplied by streak to to give more attention to actual form

    data, teams = team.league.data, team.league.teams
    # calculations of the stats for the teams

    for game in data[:-int(len(teams) * 2.5)]:
        # if the team plays at home
        if game[0] == team.name:
            HomeMatches += 1
            HomeGoalsScored += game[2]
            HomeGoalsConceded += game[3]
        # if the team plays away
        if game[1] == team.name:
            AwayMatches += 1
            AwayGoalsScored += game[3]
            AwayGoalsConceded += game[2]
    # roughly last 5 games goals have a stronger influence on the stats
    for game in data[-int(len(teams) * 2.5):]:
        # if the team plays at home
        if game[0] == team.name:
            HomeMatches += 1
            HomeGoalsScored += game[2] * streak
            HomeGoalsConceded += game[3] * streak
            # if the team plays away
        if game[1] == team.name:
            AwayMatches += 1
            AwayGoalsScored += game[3] * streak
            AwayGoalsConceded += game[2] * streak

    stats = [round(HomeGoalsScored / HomeMatches / team.league.homeGoalsAverage, 4),
             round(HomeGoalsConceded / HomeMatches / team.league.awayGoalsAverage, 4),
             round(AwayGoalsScored / AwayMatches / team.league.awayGoalsAverage, 4),
             round(AwayGoalsConceded / AwayMatches / team.league.homeGoalsAverage, 4)]

    return stats
