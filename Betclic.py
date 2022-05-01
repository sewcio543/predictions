from numpy import mat
import requests
from bs4 import BeautifulSoup as Bs
from classes import League, Match, Team
import urllib.parse
from Base import Driver
from Base import changeNames, Betclic
from collections import defaultdict


# for scraping real odds of the game from boookmaker betclic
def betclicOdds(match_: Match) -> dict[str: dict[str: float]]:
    page = requests.get(Betclic[match_.league.name][0])
    soup = Bs(page.content, "lxml")
    # grouped odds
    groups = soup.find_all('div', class_='groupEvents_content')
    print(len(groups))
    for group in groups:
        # matches
        matches = group.find_all(
            'a', class_='cardEvent prebootFreeze ng-star-inserted')
        print(len(matches))
        for match in matches:
            # names of home and away team of the match
            home, away = [team.text.replace('\n', '').strip() for team in
                          match.find_all('div', class_='scoreboard_contestantLabel')]
            print(home,away)
            # names changed to original names
            homeTeam, awayTeam = changeNames(
                match_.league.name, match_.homeTeam.name, match_.awayTeam.name, Betclic)
            # wanted match
            if homeTeam == home and awayTeam == away:
                # page with its odds
                href = urllib.parse.urljoin(
                    'https://www.betclic.pl/', match['href'])
                print(href)
                # scraping odds
                soup = Driver(href)
                oddsDict = defaultdict(dict)

                # section with odds like over/under - 2 different classes
                for oddsSection in soup.find_all('div', class_='marketBox is-table ng-star-inserted') + soup.find_all(
                        'div', class_='marketBox is-groupedMarket'):
                    category = oddsSection.find('h2').text.strip()
                    # specific odds like over 2.5/ under 2.5
                    for oddsTag in oddsSection.find_all('div', class_='marketBox_lineSelection ng-star-inserted'):
                        # dict odds is created like: {over/under: {over 2.5: 1.96, under 2,5: 1.5}
                        title = oddsTag.find('p').text.strip().replace(
                            homeTeam, 'home team').replace(awayTeam, 'away team')
                        odds = float(oddsTag.find('span').text.strip().replace('-', '0').replace(',', '.'))
                        oddsDict[category][title] = odds
                    
                return oddsDict

