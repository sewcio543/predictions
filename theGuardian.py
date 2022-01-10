import datetime
import re
import Base

leagues = Base.leagues
urls = Base.urlsTheGuardian

# form foramt 'Sunday 19 December 2021' creates '19-12' format
def findDate(game):
    date = game.find(class_="date-divider").text
    month = re.search(r" [A-Z]{1}[a-z]+ ", date)[0].strip()
    day = re.search(r" [0-9]+ ", date)[0].strip()
    # numeric
    month = datetime.datetime.strptime(month, '%B').month
    return f"{day}-{month}"


def getUpcomingTheGuardian(league, given_date):
    # get html code and find all games
    dateGames = Base.Driver(urls[league][0]).find_all("div", class_="football-matches__day")
    matches = [dateGame.find_all('tr', class_="football-match football-match--fixture") for dateGame in dateGames if
               findDate(dateGame) == given_date][0]
    return [(match.find('time').text, Base.changeNames(league, [match.find_all(class_="team-name__long")[0].text,
                                                                match.find_all(class_="team-name__long")[1].text], urls)[0],
             Base.changeNames(league, [match.find_all(class_="team-name__long")[0].text,
                                       match.find_all(class_="team-name__long")[1].text], urls)[1]) for match in matches]
