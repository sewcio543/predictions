from time import strftime
from csv import reader
import numpy as np
from Base import leagues, SkySport, TheGuardian, Flashscore, getPage, changeNames
from .analyze import analyze
from .classes import Match, Team, League
import bs4
from datetime import datetime
import re

# file contains necessary function to update data or get upcoming games from flashscore, the guardian and sky sport

# find out more in Base.py
leaguesList: list[str] = leagues
skySport: dict[str: list[str: dict[str: str]]] = SkySport
guardian: dict[str: list[str: dict[str: str]]] = TheGuardian
flashscore: dict[str: list[str: dict[str: str]]] = Flashscore



def updateCSVSkySport():
    # for each league
    for league in leaguesList:
        print(f"{league}\n")
        added = 0
        # get html code and find all games
        games: bs4.ResultSet = getPage(skySport[league][0]).find_all("div", class_="fixres__item")[:20]
        # game is div containing all info about a particular match
        for game in reversed(games):
            info = [team.text for team in game.find_all('span', class_='swap-text__target')] + [score.text.strip() for score in game.find_all('span', class_='matches__teamscores-side')]

            with open(f'csv/{league}.csv', 'r') as fileR:
                info: list[str] = changeNames(league, info[0], info[1], skySport) + [info[2], info[3]]
                # check if line already exists
                exists = True if np.array([",".join(line) == ",".join(info) for line in reader(fileR)]).any() else False
                # if not, it is send to be analyzed, to estimate the prediction in comparison to actual outcome
                if not exists:
                    try:
                        analyze(Match(Team(League(league), info[0]), Team(League(league), info[1])), int(info[2]),
                                        int(info[3]))
                        print(",".join(info))
                        with open(f'csv/{league}.csv', 'a') as fileA:
                            fileA.write(",".join(info) + "\n")
                            added += 1
                    except AttributeError:
                        pass
                    # and it is also added in csv file
        print(f"{added} games added\n")



# from format 'Sunday 19 December 2021' creates '19-12' format using regular expressions
def findDate(game: bs4.element.Tag) -> str:
    date_ = game.find(class_="date-divider").text
    month = re.search(r" [A-Z][a-z]+ ", date_)[0].strip()
    day = re.search(r" [0-9]+ ", date_)[0].strip()
    # numeric
    month = datetime.strptime(month, '%B').strftime('%m')
    return f"{day if int(day) > 9 else f'0{day}'}-{month}"


# function returns all games from given league which take place on the particular day
def getUpcomingTheGuardian(league: str, given_date: str = datetime.now().strftime('%d-%m')) -> list[tuple]:
    # get html code and find all games
    dateGames: bs4.element.ResultSet = getPage(guardian[league][0]).find_all("div", class_="football-matches__day")
    # games played on the given day
    try:
        matches = [dateGame.find_all('tr', class_="football-match football-match--fixture") for dateGame in dateGames if findDate(dateGame) == given_date][0]
        # returns list of tuples, in each: time of the kick-off, home team, away team for each game on the given day
        # names must be changed to be consistent with csv files
        return [(match.find('time').text, *changeNames(league, match.find_all(class_="team-name__long")[0].text,
                                                            match.find_all(class_="team-name__long")[1].text, guardian)) for
                match in matches]
    except IndexError:
        return []



def updateCSVFlashscore() -> None:
    # for each league
    for league in leaguesList:
        print(f"{league}\n")
        added = 0
        # get html code and find 20 recent games
        games: bs4.ResultSet = getPage(flashscore[league] + "wyniki/").find_all("div", title="Zobacz szczegóły meczu!")[:20]
        # game is div containing all info about a particular match
        # they are iterated in order in which they were played

        for game in reversed(games):
            # info about the match, 1-4 are teams and score
            info = [x.text for x in game.find_all(
                "div") if x['class'] != ['eventSubscriber', 'eventSubscriber__star', 'eventSubscriber__star--event']]
    
            with open(f'csv/{league}.csv', 'r') as fileR:
                # star is visible by live games
                star = False if game.find(class_="eventStarTouchZone") is None else True
                if not star:
                    gameInfo = info[1:5]
                    # true if any line in csv file is the same as scraped data, false if data is not in file
                    exists = True if np.array([",".join(line) == ",".join(info[1:5]) for line in reader(fileR)]).any() else False
                else:
                    gameInfo = info[2:6]
                    exists = True if np.array([",".join(line) == ",".join(info[2:6]) for line in reader(fileR)]).any() else False
                # if not, it is send to be analyzed, to estimate the prediction in comparison to actual outcome
                if not exists:
                    try:
                        analyze(Match(Team(League(league), gameInfo[0]), Team(League(league), gameInfo[1])), int(gameInfo[2]), int(gameInfo[3]))
                        print(",".join(gameInfo))
                        with open(f'csv/{league}.csv', 'a') as fileA:
                            fileA.write(",".join(gameInfo) + "\n")
                            added += 1
                    except AttributeError:
                        pass
        print(f"{added} games added\n")


# getting upcoming games using flashscore page, returns list of tuples containing time, home team, away team for each game on the given day
def getUpcomingFlashscore(league: str, given_date: str = datetime.now().strftime('%d-%m')) -> list[tuple]:
    # all games available on page (limit 30)

    games: bs4.ResultSet = getPage(flashscore[league] + "mecze/").find_all("div", title="Zobacz szczegóły meczu!")[:30]
    return [(game.find_all("div")[1].text[-5:], game.find_all("div")[2].text,
             game.find_all("div")[3].text) for game in games if
            game.find_all("div")[1].text[:5].replace('.', '-') == given_date]

