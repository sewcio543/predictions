import requests
from bs4 import BeautifulSoup as Bs
from classes import Match
import urllib.parse
from Base import Driver
from Base import changeNames, Betclic
from _collections import defaultdict


# for scraping real odds of the game from boookmaker betclic
def betclicOdds(match_: Match) -> dict[str: dict[str: float]]:
    page = requests.get(Betclic[match_.league.name][0])
    soup = Bs(page.content, "lxml")
    # grouped odds
    groups = soup.find_all('div', class_='groupEvents_content')
    for group in groups:
        # matches
        matches = group.find_all('a', class_='cardEvent prebootFreeze ng-star-inserted')
        for match in matches:
            # names of home and away team of the match
            home, away = [team.text.replace('\n', '').strip() for team in
                          match.find_all('div', class_='scoreboard_contestantLabel')]
            # names changed to original names
            homeTeam, awayTeam = changeNames(match_.league.name, match_.homeTeam.name, match_.awayTeam.name, Betclic)
            # wanted match
            if homeTeam == home and awayTeam == away:
                # page with its odds
                href = urllib.parse.urljoin('https://www.betclic.pl/', match['href'])

                # scraping odds
                soup = Driver(href)
                odds = defaultdict(dict)

                # section with odds like over/under - 2 different classes
                for oddsSection in soup.find_all('div', class_='marketBox is-table ng-star-inserted') + soup.find_all(
                        'div', class_='marketBox is-groupedMarket'):
                    # specific odds like over 2.5/ under 2.5
                    for oddsTag in oddsSection.find_all('div', class_='oddButtonWrapper prebootFreeze loading ng-trigger ng-trigger-oddsStateAnimation'):
                        # dict odds is created like: {over/under: {over 2.5: 1.96, under 2,5: 1.5}
                        if oddsSection.find('h2', class_='marketBox_headTitle ng-star-inserted') is not None:
                            # odds might be empty
                            if oddsTag.find('span').text.replace(',', '.') == '-':
                                odds[oddsSection.find('h2', class_='marketBox_headTitle ng-star-inserted').text.strip()][
                                oddsTag['title'].strip().replace(homeTeam, 'home team').replace(awayTeam, 'away team')] = 0
                            else:
                                odds[oddsSection.find('h2', class_='marketBox_headTitle ng-star-inserted').text.strip()][
                                oddsTag['title'].strip().replace(homeTeam, 'home team').replace(awayTeam, 'away team')] = float(oddsTag.find('span').text.replace(',', '.'))
                        else:
                            if oddsTag.find('span').text.replace(',', '.') == '-':
                                odds[oddsSection.find('h2', class_='marketBox_headTitle').text.strip()][
                                oddsTag['title'].strip().replace(homeTeam, 'home team').replace(awayTeam, 'away team')] = 0
                            else:
                                odds[oddsSection.find('h2', class_='marketBox_headTitle').text.strip()][
                                    oddsTag['title'].strip().replace(homeTeam, 'home team').replace(awayTeam, 'away team')] = float(oddsTag.find('span').text.replace(',', '.'))

                return odds
