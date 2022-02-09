import requests
from bs4 import BeautifulSoup as Bs
from classes import Match, League, Team
import urllib.parse
from Base import Driver
from _collections import defaultdict
from Base import changeNames, Betclic


def betclicOdds(match_: Match) -> dict[str: dict[str: float]]:
    page = requests.get(Betclic[match_.league.name][0])
    soup = Bs(page.content, "lxml")
    # group
    groups = soup.find_all('div', class_='groupEvents_content')
    for group in groups:
        # matches
        matches = group.find_all('a', class_='cardEvent prebootFreeze ng-star-inserted')
        for match in matches:
            home, away = [team.text.replace('\n', '').strip() for team in
                          match.find_all('div', class_='scoreboard_contestantLabel')]

            homeTeam, awayTeam = changeNames(match_.league.name, home, away, Betclic)
            # wanted match
            if homeTeam == home and awayTeam == away:
                href = urllib.parse.urljoin('https://www.betclic.pl/', match['href'])

                # scraping odds
                soup = Driver(href)
                odds = defaultdict(dict)

                for oddsSection in soup.find_all('div', class_='marketBox is-table ng-star-inserted') + soup.find_all(
                        'div', class_='marketBox is-groupedMarket'):
                    for oddsTag in oddsSection.find_all('div', class_='oddButtonWrapper prebootFreeze loading ng-trigger ng-trigger-oddsStateAnimation'):
                        if oddsSection.find('h2', class_='marketBox_headTitle ng-star-inserted') is not None and oddsSection.find(
                                'h2', class_='marketBox_headTitle ng-star-inserted').text.strip() in Match.oddsKeys:

                            odds[oddsSection.find('h2', class_='marketBox_headTitle ng-star-inserted').text.strip()][
                                oddsTag['title'].strip().replace(homeTeam, 'home team').replace(awayTeam, 'away team')] = float(oddsTag.find('span').text.replace(',', '.'))
                        else:
                            odds[oddsSection.find('h2', class_='marketBox_headTitle').text.strip()][
                                oddsTag['title'].strip().replace(homeTeam, 'home team').replace(awayTeam, 'away team')] = float(oddsTag.find('span').text.replace(',', '.'))

                return odds


if __name__ == '__main__':
    ls = League("LaLiga")
    m = Match(Team(ls, 'Alaves'), Team(ls, 'Valencia'))
    print(m.realOdds)
