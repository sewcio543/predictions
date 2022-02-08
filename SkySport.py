from csv import reader
import Base
import numpy as np
import analyze
from classes import Match, Team, League

leagues = Base.leagues
urls = Base.SkySport


def updateCSVSkySport():
    # for each league
    for league in leagues:
        print(f"{league}\n")
        added = 0
        # get html code and find all games
        games = Base.Driver(urls[league][0]).find_all("div", class_="fixres__item")
        # game is div containing all info about a particular match
        for game in reversed(games):
            info = [team.text for team in game.find_all('span', class_='swap-text__target')] + [score.text.strip() for
                                                                                                score in
                                                                                                game.find_all('span',
                                                                                                              class_='matches__teamscores-side')]
            with open(f'csv/{league}.csv', 'r') as fileR:
                info = Base.changeNames(league, info, urls)
                # check if line already exists
                exists = True if np.array([",".join(line) == ",".join(info) for line in reader(fileR)]).any() else False
                # if not, it is send to be analyzed, to estimate the prediction in comparison to actual outcome
                if not exists:
                    print(",".join(info))
                    analyze.analyze(Match(Team(League(league), info[0]), Team(League(league), info[1])), info[2],
                                    info[3])
                    # and it is also added in csv file
                    with open(f'csv/{league}.csv', 'a') as fileA:
                        fileA.write(",".join(info) + "\n")
                        added += 1
        print(f"{added} games added\n")
