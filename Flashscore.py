from csv import reader
import Base
import numpy as np
import analyze

leagues = Base.leagues
urls = Base.urlsFlashscore


def updateCSVFlashscore():
    # for each league
    for league in leagues:
        print(f"{league}\n")
        added = 0
        # get html code and find all games
        games = Base.Driver(urls[league] + "wyniki/").find_all("div", title="Zobacz szczegóły meczu!")[:20]
        # game is div containing all info about a particular match
        for game in reversed(games):
            # info about the match, 1-4 are teams and score
            info = [x.text for x in game.find_all("div")]
            with open(league + ".csv", 'r') as fileR:
                starOverride = False if game.find(class_="eventStarTouchZone") is None else True
                if not starOverride:
                    gameInfo = info[1:5]
                    exists = True if np.array([",".join(line) == ",".join(info[1:5]) for line in reader(fileR)]).any() else False
                else:
                    gameInfo = info[2:6]
                    exists = True if np.array([",".join(line) == ",".join(info[2:6]) for line in reader(fileR)]).any() else False
                # if not, it is send to be analyzed, to estimate the prediction in comparison to actual outcome
                if not exists:
                    print(",".join(gameInfo))
                    analyze.analyze(league, gameInfo[0], gameInfo[1], gameInfo[2], gameInfo[3])
                    with open(league + ".csv", 'a') as fileA:
                        fileA.write(",".join(gameInfo) + "\n")
                        added += 1
        print(f"{added} games added\n")


def getUpcomingFlashscore(league, given_date):
    games = Base.Driver(urls[league] + "spotkania/").find_all("div", title="Zobacz szczegóły meczu!")[:10]
    return [(game.find_all("div")[1].text[-5:], game.find_all("div")[2].text,
             game.find_all("div")[3].text) for game in games if
            game.find_all("div")[1].text[:5].replace('.', '-') == given_date]


