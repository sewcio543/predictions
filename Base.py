from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup as Bs
import pandas as pd

leagues = ["LaLiga", "Bundesliga", "PremierLeague", "Championship", "SerieA", "Ligue1"]


def Driver(link):
    opts = Options()
    opts.headless = True
    s = Service("chromedriver.exe")
    driver = webdriver.Chrome(options=opts, service=s)
    driver.get(link)
    soup = Bs(driver.page_source, "lxml")
    driver.quit()
    return soup


# this functions loads all info to excel form csv files
def loadExcel():
    with pd.ExcelWriter('database.xlsx') as writer:
        for league in leagues:
            d = pd.read_csv(league + ".csv")
            d.to_excel(writer, sheet_name=league, index=False)

    with pd.ExcelWriter('Analiza.xlsx') as writer:
        for league in leagues:
            d = pd.read_csv("Analysis" + league + ".csv")
            d.to_excel(writer, sheet_name=league, index=False)


def changeNames(league, teams, urls):
    if teams[0] in urls[league][1].keys():
        teams[0] = urls[league][1][teams[0]]
    if teams[1] in urls[league][1].keys():
        teams[1] = urls[league][1][teams[1]]
    return teams


urlsFlashscore = {'LaLiga': f"https://www.flashscore.pl/pilka-nozna/hiszpania/laliga/",
                  'Bundesliga': f"https://www.flashscore.pl/pilka-nozna/niemcy/bundesliga/",
                  'PremierLeague': f"https://www.flashscore.pl/pilka-nozna/anglia/premier-league/",
                  'Championship': f"https://www.flashscore.pl/pilka-nozna/anglia/championship/",
                  'SerieA': f"https://www.flashscore.pl/pilka-nozna/wlochy/serie-a/",
                  'Ligue1': f"https://www.flashscore.pl/pilka-nozna/francja/ligue-1/"}

# we have to change some teams' names to proceed further as not all of them coincide with flashscore names
LaLigaForbet = {"Ath. Bilbao": "Athletic Bilbao", "Atl. Madryt": "Atletico Madryt", "Barcelona": "FC Barcelona",
                "Elche": "Elche CF", "Cadiz": "Cadiz CF", "Vallecano": "Rayo Vallecano", "Betis": "Real Betis"}

BundesligaForbet = {"B. Moenchengladbach": "Moenchengladbach", "Bayern Monachium": "Bayern", "FC Augsburg": "Augsburg",
                    "TSG Hoffenheim": "Hoffenheim", "SC Freiburg": "Freiburg", "VfB Stuttgart": "Stuttgart",
                    "Furth": "Greuther Furth", "1. FC Union Berlin": "Union Berlin", "Bayer Leverkusen": "Leverkusen",
                    "VfL Wolfsburg": "Wolfsburg", "Bochum": "VfL Bochum", "Borussia Dortmund": "Dortmund",
                    "Eintracht Frankfurt": "Frankfurt", "1. FSV Mainz 05": "Mainz", "1. FC Koeln": "FC Koln",
                    "Hertha Berlin": "Hertha"}

PremierLeagueForbet = {"Manchester Utd": "Manchester United", "Wolves": "Wolverhampton"}

ChampionshipForbet = {}

SerieAForbet = {"Salernitana": "US Salernitana 1919", "Verona": "Hellas Verona", "Venezia": "SSC Venezia"}

Ligue1Forbet = {"Lorient": "FC Lorient"}

# dict with link to webpage to be scraped and dicts of names to be changed in order to scrape properly
urlsForbetOdds = {'LaLiga': ["https://www.iforbet.pl/oferta/8/159", LaLigaForbet],
                  'Bundesliga': ["https://www.iforbet.pl/oferta/8/29975", BundesligaForbet],
                  'PremierLeague': ["https://www.iforbet.pl/oferta/8/199", PremierLeagueForbet],
                  'Championship': ["https://www.iforbet.pl/oferta/8/29927", ChampionshipForbet],
                  'SerieA': ["https://www.iforbet.pl/oferta/8/122", SerieAForbet],
                  'Ligue1': ["https://www.iforbet.pl/oferta/8/29958", Ligue1Forbet]}

# it goes the other way around
urlsForbetScrape = {'LaLiga': ["https://www.iforbet.pl/oferta/8/159", dict((LaLigaForbet[key], key) for key in LaLigaForbet)],
                    'Bundesliga': ["https://www.iforbet.pl/oferta/8/29975", dict((BundesligaForbet[key], key) for key in BundesligaForbet)],
                    'PremierLeague': ["https://www.iforbet.pl/oferta/8/199", dict((PremierLeagueForbet[key], key) for key in PremierLeagueForbet)],
                    'Championship': ["https://www.iforbet.pl/oferta/8/29927", dict((ChampionshipForbet[key], key) for key in ChampionshipForbet)],
                    'SerieA': ["https://www.iforbet.pl/oferta/8/122", dict((SerieAForbet[key], key) for key in SerieAForbet)],
                    'Ligue1': ["https://www.iforbet.pl/oferta/8/29958", dict((Ligue1Forbet[key], key) for key in Ligue1Forbet)]}


LaLigaSkySport = {"Athletic Bilbao": "Ath. Bilbao", "Atletico Madrid": "Atl. Madryt", "FC Barcelona": "Barcelona",
                  "Elche CF": "Elche", "Cadiz CF": "Cadiz", "Rayo Vallecano": "Vallecano", "Real Betis": "Betis",
                  "Real Madrid": "Real Madryt", "Real Mallorca": "Mallorca"}

BundesligaSkySport = {"M'gladbach": "B. Moenchengladbach", "Bayern Munich": "Bayern Monachium",
                      "Hoffenheim": "TSG Hoffenheim", "Stuttgart": "VfB Stuttgart",
                      "Greuther Furth": "Furth", "FC Union Berlin": "1. FC Union Berlin",
                      "Wolfsburg": "VfL Wolfsburg", "RB Leipzig": "RB Lipsk",
                      "Frankfurt": "Eintracht Frankfurt", "Mainz": "1. FSV Mainz 05", "Cologne": "1. FC Koeln",
                      "Hertha": "Hertha Berlin"}

PremierLeagueSkySport = {"Leeds United": "Leeds", "Wolverhampton Wanderers": "Wolves", "Norwich City": "Norwich",
                         "Leicester City": "Leicester", "Brighton and Hove Albion": "Brighton",
                         "Tottenham Hotspur": "Tottenham", "Manchester United": "Manchester Utd",
                         "West Ham United": "West Ham", "Newcastle United": "Newcastle"}

ChampionshipSkySport = {"Blackburn Rovers": "Blackburn", "Hull City": "Hull", "Queens Park Rangers": "QPR",
                        "Huddersfield Town": "Huddersfield", "Birmingham City": "Birmingham",
                        "Nottingham Forest": "Nottingham", "Cardiff City": "Cardiff", "Stoke City": "Stoke",
                        "Coventry City": "Coventry", "Peterborough United": "Peterborough", "Swansea City": "Swansea",
                        "Derby County": "Derby", "Preston North End": "Preston", "West Bromwich Albion": "West Brom",
                        "Luton Town": "Luton", "Sheffield United": "Sheffield Utd"}

SerieASkySport = {"Roma": "AS Roma", "Inter Milan": "Inter"}

Ligue1SkySport = {"FC Lorient": "Lorient", "Paris Saint-Germain": "PSG", "Marseille": "Marsylia",
                  "St Etienne": "St. Etienne",
                  "RC Lens": "Lens"}

# dict with urls addresses to skysport page for each league
urlsSkySport = {'LaLiga': ["https://www.skysports.com/la-liga-results/", LaLigaSkySport],
                'Bundesliga': ["https://www.skysports.com/bundesliga-results", BundesligaSkySport],
                'PremierLeague': ["https://www.skysports.com/premier-league-results", PremierLeagueSkySport],
                'Championship': ["https://www.skysports.com/championship-results", ChampionshipSkySport],
                'SerieA': ["https://www.skysports.com/serie-a-results", SerieASkySport],
                'Ligue1': ["https://www.skysports.com/ligue-1-results", Ligue1SkySport]}

LaLigaTheGuardian = {"A Bilbao": "Ath. Bilbao", "Atlético": "Atl. Madryt", "Rayo Vallecano": "Vallecano",
                     "Real Betis": "Betis",
                     "Real Madrid": "Real Madryt"}

BundesligaTheGuardian = {"M'gladbach": "B. Moenchengladbach", "Bayern": "Bayern Monachium",
                         "Dortmund": "Borussia Dortmund",
                         "Hoffenheim": "TSG Hoffenheim", "Stuttgart": "VfB Stuttgart",
                         "Greuther Furth": "Furth", "Union Berlin": "1. FC Union Berlin",
                         "Wolfsburg": "VfL Wolfsburg", "RB Leipzig": "RB Lipsk",
                         "Mainz": "1. FSV Mainz 05", "Cologne": "1. FC Koeln", "VfL Bochum": "Bochum",
                         "Hertha": "Hertha Berlin", "Freiburg": "SC Freiburg", "Leverkusen": "Bayer Leverkusen",
                         "Augsburg": 'FC Augsburg'}

PremierLeagueTheGuardian = {"C Palace": "Crystal Palace", "Brighton": "Brighton", "Spurs": "Tottenham",
                            "Man Utd": "Manchester Utd", "Man City": "Manchester City"}

ChampionshipTheGuardian = {"Nottm Forest": "Nottingham", "Preston North End": "Preston",
                           "Sheff Utd": "Sheffield Utd", "AFC Bournemouth": "Bournemouth"}

SerieATheGuardian = {"Roma": "AS Roma"}

Ligue1TheGuardian = {"FC Lorient": "Lorient", "Clermont Foot": "Clermont", "Marseille": "Marsylia",
                     "St Etienne": "St. Etienne"}

# dict with urls addresses to theguardian page for each league
urlsTheGuardian = {'LaLiga': ["https://www.theguardian.com/football/laligafootball/fixtures", LaLigaTheGuardian],
                   'Bundesliga': ["https://www.theguardian.com/football/bundesligafootball/fixtures",
                                  BundesligaTheGuardian],
                   'PremierLeague': ["https://www.theguardian.com/football/premierleague/fixtures",
                                     PremierLeagueTheGuardian],
                   'Championship': ["https://www.theguardian.com/football/championship/fixtures",
                                    ChampionshipTheGuardian],
                   'SerieA': ["https://www.theguardian.com/football/serieafootball/fixtures", SerieATheGuardian],
                   'Ligue1': ["https://www.theguardian.com/football/ligue1football/fixtures", Ligue1TheGuardian]}
