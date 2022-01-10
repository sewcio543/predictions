import requests
from bs4 import BeautifulSoup as Bs
import re
import Base
from datetime import date
from dateutil.relativedelta import relativedelta

# file contains all the functions used to interact with forbet
# bs4 is enough to get all the info from this page
urls = Base.urlsForbetOdds
urlsScrape = Base.urlsForbetScrape


# getting wrapper for all forbet pages
def getwrapper(link):
    page = requests.get(link)
    return Bs(page.content, "lxml")


# if event and its text is given, odds are easy to scrape
def find_event(data_gamename, data_outcomename, league, home, away):
    home, away = Base.changeNames(league, [home, away], urls)
    # all the games on page (in given league)
    events = getwrapper(urls[league][0]).find_all(class_="event-panel")
    # the game we look for
    ourEvent = [event for event in events if
                event.find_all("span")[0].text == home and event.find_all("span")[4].text == away]
    # extended link to particular odds related to game takes form of "zdarzenie/some number"
    # regex function is used to look for it in div with class - "event-more" and all odds are found
    oddsEvents = getwrapper(
        "https://www.iforbet.pl/" + re.search('zdarzenie/[0-9]+', str(ourEvent[0].find(class_="event-more")))[
            0]).find_all(class_="event-rate")
    # now we return odds in class - "rate-value" if description is correct
    return float([event.find("span", class_="rate-value").text for event in oddsEvents if
                  data_gamename in str(event) and data_outcomename in str(event)][0])


def winnerOdds(league, home, away):
    home, away = Base.changeNames(league, [home, away], urls)
    events = getwrapper(urls[league][0]).find_all(class_="event-panel")
    info = [event.find_all("span") for event in events if
            event.find_all("span")[0].text == home and event.find_all("span")[4].text == away]
    return [float(info[0][i].text) for i in range(1, 6, 2)]


# these functions are directly called by outcome.prediction
def btts(arguments):
    return find_event("Obie drużyny strzelą bramkę", "data-outcomename=\"Tak\"", arguments[0], arguments[1],
                      arguments[2])


def nbtts(arguments):
    return find_event("Obie drużyny strzelą bramkę", "data-outcomename=\"Nie\"", arguments[0], arguments[1],
                      arguments[2])


def under2_5(arguments):
    return find_event("data-gamename=\"poniżej/powyżej 2.5 goli\"", "Poniżej 2.5 bramki", arguments[0], arguments[1],
                      arguments[2])


def over2_5(arguments):
    return find_event("data-gamename=\"poniżej/powyżej 2.5 goli\"", "Powyżej 2.5 bramki", arguments[0], arguments[1],
                      arguments[2])


def x1(arguments):
    return find_event("Podwójna szansa", "1/X", arguments[0], arguments[1], arguments[2])


def x2(arguments):
    return find_event("Podwójna szansa", "X/2", arguments[0], arguments[1], arguments[2])


def getUpcomingForbet(league, given_date):
    r = requests.get(urlsScrape[league][0])
    # all matches from grouped by days
    info = Bs(r.content, "lxml").find_all(class_='events-group')
    # games of the required day
    if int(given_date.split('-')[1]) > date.today().month:
        m = relativedelta(months=1) + date.today()
    if int(given_date.split('-')[1]) < date.today().month:
        m = relativedelta(months=-1) + date.today()
    else:
        m = date.today()
    gamesOfTheDay = [games for games in info if
                     re.search(r'\d+', games.find_all('span')[1].text)[0] + f'-{m.strftime("%m")}' == given_date.lstrip('0')]
    # all games
    try:
        games = gamesOfTheDay[0].find_all(class_='event-panel')
        # time and teams of the games
        return [(game.find(class_='event-time').text,
                 Base.changeNames(league, [game.find_all('span')[0].text, game.find_all('span')[4].text], urlsScrape)[
                     0],
                 Base.changeNames(league, [game.find_all('span')[0].text, game.find_all('span')[4].text], urlsScrape)[
                     1])
                for game in games]
    except Exception:
        return []

