from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup as Bs
import bs4
import pandas as pd
import time

# leagues that are available to make operations on, which data we have
leagues = ["LaLiga", "Bundesliga", "PremierLeague", "Championship", "SerieA", "Ligue1"]


# function to return html code of dynamic page
def Driver(link: str) -> bs4.element.Tag:
    opts = Options()
    opts.headless = True
    s = Service("chromedriver.exe")
    driver = webdriver.Chrome(options=opts, service=s)
    driver.get(link)
    time.sleep(0.5)
    soup: bs4.element.Tag = Bs(driver.page_source, "lxml")
    return soup


# this functions loads all data coming from analysis and updates form csv files to excel
def loadExcel() -> None:
    with pd.ExcelWriter('database.xlsx') as writer:
        for league in leagues:
            d = pd.read_csv(f'csv/{league}.csv')
            d.to_excel(writer, sheet_name=league, index=False)

    with pd.ExcelWriter('Analisis.xlsx') as writer:
        for league in leagues:
            d = pd.read_csv(f'csv/Analysis{league}.csv')
            d.to_excel(writer, sheet_name=league, index=False)


# changes names scraped from different pages to adjust them to csv data
def changeNames(league: str, homeTeam: str, awayTeam: str, page: dict[str: list[str, dict]]) -> list[str]:
    if homeTeam in page[league][1].keys():
        homeTeam = page[league][1][homeTeam]
    if awayTeam in page[league][1].keys():
        awayTeam = page[league][1][awayTeam]
    return [homeTeam, awayTeam]


# original names in csv data comes from flashscore, this dict contains links to every league on flashscore
Flashscore: dict = {'LaLiga': f"https://www.flashscore.pl/pilka-nozna/hiszpania/laliga/",
                    'Bundesliga': f"https://www.flashscore.pl/pilka-nozna/niemcy/bundesliga/",
                    'PremierLeague': f"https://www.flashscore.pl/pilka-nozna/anglia/premier-league/",
                    'Championship': f"https://www.flashscore.pl/pilka-nozna/anglia/championship/",
                    'SerieA': f"https://www.flashscore.pl/pilka-nozna/wlochy/serie-a/",
                    'Ligue1': f"https://www.flashscore.pl/pilka-nozna/francja/ligue-1/"}

# if we scrape to find particular event, keys are names from original data, values are names on scraped page, since we want them to be our final names
LaLigaBetclic: dict = {"Ath. Bilbao": "Athletic Bilbao", "Atl. Madryt": "Atletico Madryt",
                       "Cadiz": "Cádiz", "Vallecano": "Rayo Vallecano"}

BundesligaBetclic: dict = {"B. Moenchengladbach": "Borussia M'gladbach", "FC Augsburg": "Augsburg",
                           "TSG Hoffenheim": "Hoffenheim", "SC Freiburg": "Freiburg", "VfB Stuttgart": "Stuttgart",
                           "Furth": "Greuther Furth", "1. FC Union Berlin": "Union Berlin",
                           "Bayer Leverkusen": "B. Leverkusen", "RB Lipsk": "RB Lepizig",
                           "VfL Wolfsburg": "Wolfsburg", "Borussia Dortmund": "Dortmund",
                           "Eintracht Frankfurt": "Eintracht Fr.", "1. FSV Mainz 05": "Mainz", "1. FC Koeln": "FC Koln",
                           "Arminia Bielefeld": "Arminia"}

PremierLeagueBetclic: dict = {"Norwich": "Norwich City", "Wolves": "Wolverhampton"}

ChampionshipBetclic: dict = {"Nottingham": "Nottingham Forest", "West Brom": "West Bromich",
                             "Peterborough": "Peterborough United", "Preston": "Preston North End"}

SerieABetclic: dict = {"AS Roma": "Roma"}

Ligue1Betclic: dict = {"St.Etienne": "Saint-Etienne", "Clermont": "Clermont Foot", "PSG": "Paris SG"}

# dict with link to webpage to be scraped and dicts of names to be changed in order to scrape properly
Betclic: dict = {'LaLiga': ["https://www.betclic.pl/pilka-nozna-s1/la-liga-c7", LaLigaBetclic],
                 'Bundesliga': ["https://www.betclic.pl/pilka-nozna-s1/bundesliga-c5", BundesligaBetclic],
                 'PremierLeague': ["https://www.betclic.pl/pilka-nozna-s1/premier-league-c3", PremierLeagueBetclic],
                 'Championship': ["https://www.betclic.pl/pilka-nozna-s1/anglia-championship-c28",
                                  ChampionshipBetclic],
                 'SerieA': ["https://www.betclic.pl/pilka-nozna-s1/serie-a-c6", SerieABetclic],
                 'Ligue1': ["https://www.betclic.pl/pilka-nozna-s1/ligue-1-c4", Ligue1Betclic]}

# if we scrape in order to update our data, keys are names from scraped page, values are original names, since we want them to be our final names
LaLigaSkySport: dict = {"Athletic Bilbao": "Ath. Bilbao", "Atletico Madrid": "Atl. Madryt", "FC Barcelona": "Barcelona",
                        "Elche CF": "Elche", "Cadiz CF": "Cadiz", "Rayo Vallecano": "Vallecano", "Real Betis": "Betis",
                        "Real Madrid": "Real Madryt", "Real Mallorca": "Mallorca"}

BundesligaSkySport: dict = {"M'gladbach": "B. Moenchengladbach", "Bayern Munich": "Bayern Monachium",
                            "Hoffenheim": "TSG Hoffenheim", "Stuttgart": "VfB Stuttgart",
                            "Greuther Furth": "Furth", "FC Union Berlin": "1. FC Union Berlin",
                            "Wolfsburg": "VfL Wolfsburg", "RB Leipzig": "RB Lipsk",
                            "Frankfurt": "Eintracht Frankfurt", "Mainz": "1. FSV Mainz 05", "Cologne": "1. FC Koeln",
                            "Hertha": "Hertha Berlin"}

PremierLeagueSkySport: dict = {"Leeds United": "Leeds", "Wolverhampton Wanderers": "Wolves", "Norwich City": "Norwich",
                               "Leicester City": "Leicester", "Brighton and Hove Albion": "Brighton",
                               "Tottenham Hotspur": "Tottenham", "Manchester United": "Manchester Utd",
                               "West Ham United": "West Ham", "Newcastle United": "Newcastle"}

ChampionshipSkySport: dict = {"Blackburn Rovers": "Blackburn", "Hull City": "Hull", "Queens Park Rangers": "QPR",
                              "Huddersfield Town": "Huddersfield", "Birmingham City": "Birmingham",
                              "Nottingham Forest": "Nottingham", "Cardiff City": "Cardiff", "Stoke City": "Stoke",
                              "Coventry City": "Coventry", "Peterborough United": "Peterborough",
                              "Swansea City": "Swansea",
                              "Derby County": "Derby", "Preston North End": "Preston",
                              "West Bromwich Albion": "West Brom",
                              "Luton Town": "Luton", "Sheffield United": "Sheffield Utd"}

SerieASkySport: dict = {"Roma": "AS Roma", "Inter Milan": "Inter"}

Ligue1SkySport: dict = {"FC Lorient": "Lorient", "Paris Saint-Germain": "PSG", "Marseille": "Marsylia",
                        "St Etienne": "St. Etienne",
                        "RC Lens": "Lens"}

# dict with skySport addresses to skysport page for each league
SkySport: dict = {'LaLiga': ["https://www.skysports.com/la-liga-results/", LaLigaSkySport],
                  'Bundesliga': ["https://www.skysports.com/bundesliga-results", BundesligaSkySport],
                  'PremierLeague': ["https://www.skysports.com/premier-league-results", PremierLeagueSkySport],
                  'Championship': ["https://www.skysports.com/championship-results", ChampionshipSkySport],
                  'SerieA': ["https://www.skysports.com/serie-a-results", SerieASkySport],
                  'Ligue1': ["https://www.skysports.com/ligue-1-results", Ligue1SkySport]}

LaLigaTheGuardian: dict = {"A Bilbao": "Ath. Bilbao", "Atlético": "Atl. Madryt", "Rayo Vallecano": "Vallecano",
                           "Real Betis": "Betis",
                           "Real Madrid": "Real Madryt"}

BundesligaTheGuardian: dict = {"M'gladbach": "B. Moenchengladbach", "Bayern": "Bayern Monachium",
                               "Dortmund": "Borussia Dortmund",
                               "Hoffenheim": "TSG Hoffenheim", "Stuttgart": "VfB Stuttgart",
                               "Greuther Furth": "Furth", "Union Berlin": "1. FC Union Berlin",
                               "Wolfsburg": "VfL Wolfsburg", "RB Leipzig": "RB Lipsk",
                               "Mainz": "1. FSV Mainz 05", "Cologne": "1. FC Koeln", "VfL Bochum": "Bochum",
                               "Hertha": "Hertha Berlin", "Freiburg": "SC Freiburg", "Leverkusen": "Bayer Leverkusen",
                               "Augsburg": 'FC Augsburg'}

PremierLeagueTheGuardian: dict = {"C Palace": "Crystal Palace", "Brighton": "Brighton", "Spurs": "Tottenham",
                                  "Man Utd": "Manchester Utd", "Man City": "Manchester City"}

ChampionshipTheGuardian: dict = {"Nottm Forest": "Nottingham", "Preston North End": "Preston",
                                 "Sheff Utd": "Sheffield Utd", "AFC Bournemouth": "Bournemouth"}

SerieATheGuardian: dict = {"Roma": "AS Roma"}

Ligue1TheGuardian: dict = {"FC Lorient": "Lorient", "Clermont Foot": "Clermont", "Marseille": "Marsylia",
                           "St Etienne": "St. Etienne"}

# dict with skySport addresses to theguardian page for each league
TheGuardian: dict = {'LaLiga': ["https://www.theguardian.com/football/laligafootball/fixtures", LaLigaTheGuardian],
                     'Bundesliga': ["https://www.theguardian.com/football/bundesligafootball/fixtures",
                                    BundesligaTheGuardian],
                     'PremierLeague': ["https://www.theguardian.com/football/premierleague/fixtures",
                                       PremierLeagueTheGuardian],
                     'Championship': ["https://www.theguardian.com/football/championship/fixtures",
                                      ChampionshipTheGuardian],
                     'SerieA': ["https://www.theguardian.com/football/serieafootball/fixtures", SerieATheGuardian],
                     'Ligue1': ["https://www.theguardian.com/football/ligue1football/fixtures", Ligue1TheGuardian]}
