import numpy as np
import pandas as pd
import math
import Forbet

pd.set_option('display.float_format', lambda x: '%.1f' % x)
np.set_printoptions(suppress=True)

# leagues saved in csv file
leagues = ["LaLiga", "Bundesliga", "PremierLeague", "Championship", "SerieA", "Ligue1"]


# csv format contains all the games played in a particular league in season 2021/22
# all the line constructions follows a simple pattern: home team,away team,goals scored by home team,goals scored by away team


# finds all teams from csv of the given league and returns list of teams and csv data as numpy
def findTeams(league):
    if type(league) == str:
        league = leagues.index(league)
    data = pd.read_csv(leagues[league] + ".csv").to_numpy()
    teams = list(set(data[:, 0]))
    teams.sort()
    return teams, data


def prediction(league, homeTeam, awayTeam, streak=1.3, realOdds=False, analysis=False, betting=False):
    # if odds are not available on forbet they will not be printed
    error = False
    # string variable printed at the end
    stringBuilder = ""

    # if argument is given as a name of the team or league it is changed for its index representation
    if type(league) == str:
        league = leagues.index(league)

    # get teams and data from external function
    teams, data_numpy = findTeams(league)

    if type(homeTeam) == str:
        homeTeam = teams.index(homeTeam)

    if type(awayTeam) == str:
        awayTeam = teams.index(awayTeam)

    stats, HomeGoalsAverage, AwayGoalsAverage = strengths(league, streak=streak, prediction=True)
    # list containing arguments for scraping functions from Forbet.py file, which are used to get all the real odds from forbet page
    # each arguments is string while indexes are int type
    arguments = [leagues[league], teams[homeTeam], teams[awayTeam]]
    # for a specific game we calculate expected goals of each team by getting values from stats dict
    # expected home goals = home team strength in attack at home * away team strength away in defence * average of leagues goals scored by home team
    # expected away goals = away team strength in attack away * home team strength home in defence * average of leagues goals scored by away team
    ExpectedGoalsHome = round(stats[teams[homeTeam]][0] * stats[teams[awayTeam]][3] * HomeGoalsAverage, 3)
    ExpectedGoalsAway = round(stats[teams[homeTeam]][1] * stats[teams[awayTeam]][2] * AwayGoalsAverage, 3)

    # expected result of the match
    stringBuilder += f"Expected Result:\n{ExpectedGoalsHome} : {ExpectedGoalsAway}\n\n"

    # Poisson distribution for each value (probability of an event for each number of goals(30) to cover the whole margin and get all possible results)
    # in Poisson distribution probability of getting k is___(lambda^k)*e^(-lambda)/k! where lambda is the expected value
    scoreRestriction = 30
    probabilityHome = [(ExpectedGoalsHome ** result) * math.exp(-ExpectedGoalsHome) / math.factorial(result) for
                       result in range(scoreRestriction)]
    probabilityAway = [(ExpectedGoalsAway ** result) *
                       math.exp(-ExpectedGoalsAway) / math.factorial(result) for result in range(scoreRestriction)]

    # result probability based on Poisson distribution
    probabilityOfResult = list()
    for awayResult in probabilityAway:
        for homeResult in probabilityHome:
            probabilityOfResult.append(homeResult * awayResult)

    # making the numpy array 30x30 from the list
    # list contains 900 elements with 900 probabilities for each result
    probabilityOfResultnp = np.array(
        [probabilityOfResult[x:x + 30] for x in range(0, scoreRestriction ** 2, scoreRestriction)])
    # saving it as pd.df 4x4 (most probable results) *100 to get the percentage values
    tableOfScores = pd.DataFrame((probabilityOfResultnp[:6, :6] * 100).round(4))

    # now it's time to sum up the probabilities and get the chances of a specific outcome
    tieProbability, homeWinProbability, awayWinProbability = 0, 0, 0

    # iterating through np array and summing up probabilities
    for row in range(probabilityOfResultnp.shape[0]):
        for column in range(probabilityOfResultnp.shape[1]):
            # that gives as a draw
            if row == column:
                tieProbability += probabilityOfResultnp[row, column]
            # away team win
            elif row > column:
                awayWinProbability += probabilityOfResultnp[row, column]
            # home team win
            else:
                homeWinProbability += probabilityOfResultnp[row, column]

    # times 100 to get the percentage value
    homeWinProbability = round(homeWinProbability * 100, 2)
    awayWinProbability = round(awayWinProbability * 100, 2)
    tieProbability = round(tieProbability * 100, 2)

    # adding probabilities to string builder
    stringBuilder += f"{teams[homeTeam]} : {homeWinProbability}%\ntie : {tieProbability}%\n{teams[awayTeam]} : {awayWinProbability}%\n"

    # to avoid division by 0, if probability of some results is 0 it is used try except
    # method to count expected odds is divide 100 by percentage value of probability of an occurrence of some event
    ExpectedOdds = [0, 0, 0]
    # noinspection PyBroadException
    try:
        ExpectedOdds[0] = round(100 / homeWinProbability, 2)
    except:
        ExpectedOdds[0] = 0
    # noinspection PyBroadException
    try:
        ExpectedOdds[1] = round(100 / tieProbability, 2)
    except:
        ExpectedOdds[1] = 0
    # noinspection PyBroadException
    try:
        ExpectedOdds[2] = round(100 / awayWinProbability, 2)
    except:
        ExpectedOdds[2] = 0

    # probabilities of a specific results (each score in range 4)
    stringBuilder += f"\n{tableOfScores}\n"
    # the most probable outcome (index of the flatten np array probabilityOfResultnp)
    maxi = np.argmax(probabilityOfResultnp)
    # maxi % 30 is a number of the column (home team score), maxi/30 as int is a number of the row (away team score)
    stringBuilder += f"\nExpected result : {maxi % 30} : {int(maxi / 30)}"
    # 5 most probable outcomes (indices of sorted array in descending order with axis none (flatten array)
    arg = np.argsort(-probabilityOfResultnp, axis=None)[1:5]
    stringBuilder += "\nAlso: "
    for i in arg:
        # method as before
        stringBuilder += f"{i % 30}:{int(i / 30)}  "

    # argument of the function (for processing the scraping part)
    if realOdds:
        # noinspection PyBroadException
        try:
            # odds and real probabilities for the results
            stringBuilder += f"\n\n{teams[homeTeam]} : Expected Odds: {ExpectedOdds[0]} Forbet: {Forbet.winnerOdds(leagues[league], teams[homeTeam], teams[awayTeam])[0]}\n" \
                             f"tie: Expected Odds: {ExpectedOdds[1]} Forbet: {Forbet.winnerOdds(leagues[league], teams[homeTeam], teams[awayTeam])[1]}\n" \
                             f"{teams[awayTeam]} : Expected Odds: {ExpectedOdds[2]} Forbet: {Forbet.winnerOdds(leagues[league], teams[homeTeam], teams[awayTeam])[2]}\n"
        except:
            error = True
            stringBuilder += f"\n\n{teams[homeTeam]} : Expected Odds: {ExpectedOdds[0]}\n" \
                             f"tie: Expected Odds: {ExpectedOdds[1]}\n" \
                             f"{teams[awayTeam]} : Expected Odds: {ExpectedOdds[2]}\n"

    else:
        stringBuilder += f"\n\n{teams[homeTeam]} : Expected Odds: {ExpectedOdds[0]}\n" \
                         f"tie: Expected Odds: {ExpectedOdds[1]}\n" \
                         f"{teams[awayTeam]} : Expected Odds: {ExpectedOdds[2]}\n"

    # summing all the scores in which both teams score at least one goal
    bttsChances = np.array(probabilityHome[1:]).sum() * np.array(probabilityAway[1:]).sum() * 100
    # getting real odds for particular events from Forbet.py functions
    # chance of -2.5 goals in the game
    under3 = (probabilityOfResultnp[0:3, 0].sum() + probabilityOfResultnp[0, 1:3].sum() + probabilityOfResultnp[
        1, 1]) * 100
    if realOdds:
        # noinspection PyBroadException
        try:
            # odds for btts
            stringBuilder += f"\nBTTS: {round(bttsChances, 2)}% Expected Odds: (TAK: {round(100 / bttsChances, 2)}, NIE: {round((100 / (100 - bttsChances)), 2)}) " \
                             f"Forbet : (TAK: {Forbet.btts(arguments)}, NIE: {Forbet.nbtts(arguments)})"
            # odds for -+2.5
            stringBuilder += f"\n-2.5 : {round(under3, 2)}% Expected Odds: {round(100 / under3, 2)} Forbet : {Forbet.under2_5(arguments)}" \
                             f"\n+2.5 {round(100 - under3, 2)}% Expected Odds: {round((100 / (100 - under3)), 2)} " \
                             f"Forbet : {Forbet.over2_5(arguments)}\n"

            # odds for 1/x 2/x
            stringBuilder += f"1/X : {round(tieProbability + homeWinProbability, 2)}% Expected Odds: {round(100 / (tieProbability + homeWinProbability), 2)} Forbet: {Forbet.x1(arguments)}\n" \
                             f"2/X : {round(tieProbability + awayWinProbability, 2)}% Expected Odds: {round(100 / (tieProbability + awayWinProbability), 2)} Forbet: {Forbet.x2(arguments)}\n\n"


        except:
            stringBuilder += f"\nBTTS: {round(bttsChances, 2)}% Expected Odds: (TAK: {round(100 / bttsChances, 2)}, NIE: {round((100 / (100 - bttsChances)), 2)})" \
                             f"\n-2.5 : {round(under3, 2)}% Expected Odds: {round(100 / under3, 2)}" \
                             f"\n+2.5 {round(100 - under3, 2)}% Expected Odds: {round((100 / (100 - under3)), 2)}" \
                             f"\n1/X : {round(tieProbability + homeWinProbability, 2)}% Expected Odds: {round(100 / (tieProbability + homeWinProbability), 2)}" \
                             f"\n2/X : {round(tieProbability + awayWinProbability, 2)}% Expected Odds: {round(100 / (tieProbability + awayWinProbability), 2)}\n\n"
            error = True

    else:
        stringBuilder += f"\nBTTS: {round(bttsChances, 2)}% Expected Odds: (TAK: {round(100 / bttsChances, 2)}, NIE: {round((100 / (100 - bttsChances)), 2)})" \
                         f"\n-2.5 : {round(under3, 2)}% Expected Odds: {round(100 / under3, 2)}" \
                         f"\n+2.5 {round(100 - under3, 2)}% Expected Odds: {round((100 / (100 - under3)), 2)}" \
                         f"\n1/X : {round(tieProbability + homeWinProbability, 2)}% Expected Odds: {round(100 / (tieProbability + homeWinProbability), 2)}" \
                         f"\n2/X : {round(tieProbability + awayWinProbability, 2)}% Expected Odds: {round(100 / (tieProbability + awayWinProbability), 2)}\n\n"

    # argument of the function, we can use it if we want use data for further processing and calculations
    if analysis:
        return [ExpectedGoalsHome, ExpectedGoalsAway, [homeWinProbability, tieProbability, awayWinProbability],
                pd.DataFrame((probabilityOfResultnp[:10, :10] * 100).round(1))]
    if betting:
        try:
            return [Forbet.winnerOdds(leagues[league], teams[homeTeam], teams[awayTeam])[0], homeWinProbability,
                    Forbet.winnerOdds(leagues[league], teams[homeTeam], teams[awayTeam])[1], tieProbability,
                    Forbet.winnerOdds(leagues[league], teams[homeTeam], teams[awayTeam])[2], awayWinProbability,
                    Forbet.btts(arguments), round(bttsChances, 2),
                    Forbet.nbtts(arguments), round(100 - bttsChances, 2),
                    Forbet.under2_5(arguments), round(under3, 2),
                    Forbet.over2_5(arguments), round(100 - under3, 2),
                    Forbet.x1(arguments), round(tieProbability + homeWinProbability, 2),
                    Forbet.x2(arguments), round(tieProbability + awayWinProbability, 2)]
        except:
            return []

    if error:
        stringBuilder += "Odds unavailable\n"

    return stringBuilder


def strengths(league, prediction=False, streak=1.3):
    # variables contain numbers of matches played at home and away and goals scored and conceded
    HomeGoalsScored, AwayGoalsScored, HomeMatches, AwayMatches, HomeGoalsConceded, AwayGoalsConceded = 0, 0, 0, 0, 0, 0
    # last 5 rounds goals are multiplied by streak to to give more attention to actual form
    # foundation of all the calculations - stats for all teams
    stats = dict()
    teams, data_numpy = findTeams(league)
    # calculations of the stats for the teams
    for team in teams:
        for game in data_numpy[:-int(len(teams) * 2.5)]:
            # if the team plays at home
            if game[0] == team:
                HomeMatches += 1
                HomeGoalsScored += game[2]
                HomeGoalsConceded += game[3]
            # if the team plays away
            if game[1] == team:
                AwayMatches += 1
                AwayGoalsScored += game[3]
                AwayGoalsConceded += game[2]
        # roughly last 5 games goals have a stronger influence on the stats
        for game in data_numpy[-int(len(teams) * 2.5):]:
            # if the team plays at home
            if game[0] == team:
                HomeMatches += 1
                HomeGoalsScored += game[2] * streak
                HomeGoalsConceded += game[3] * streak
                # if the team plays away
            if game[1] == team:
                AwayMatches += 1
                AwayGoalsScored += game[3] * streak
                AwayGoalsConceded += game[2] * streak

        # averages of goals for a team are added to dictionary with a key as team name
        stats[team] = [round(HomeGoalsScored / HomeMatches, 4), round(HomeGoalsConceded / HomeMatches, 4),
                       round(AwayGoalsScored / AwayMatches, 4), round(AwayGoalsConceded / AwayMatches, 4)]
        # all variables are equal 0 now, we proceed to the next team's calculations
        HomeGoalsScored, AwayGoalsScored, HomeMatches, AwayMatches, HomeGoalsConceded, AwayGoalsConceded = 0, 0, 0, 0, 0, 0

    # league's averages
    HomeGoalsAverage = round(data_numpy[:, 2].sum() / data_numpy.shape[0], 4)
    AwayGoalsAverage = round(data_numpy[:, 3].sum() / data_numpy.shape[0], 4)

    # stats are now corrected with leagues averages to count real strengths of the teams
    for i in stats:
        stats[i] = [round(stats[i][0] / HomeGoalsAverage, 3), round(stats[i][1] / AwayGoalsAverage, 3),
                    round(stats[i][2] / AwayGoalsAverage, 3), round(stats[i][3] / HomeGoalsAverage, 3)]

    if prediction:
        return stats, HomeGoalsAverage, AwayGoalsAverage
    else:
        return stats
