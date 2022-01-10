from tkinter import *
from tkinter import ttk
from outcome import leagues, prediction
from Flashscore import getUpcomingFlashscore, updateCSVFlashscore
from datetime import date
import datetime
import numpy as np
from SkySport import updateCSVSkySport
from theGuardian import getUpcomingTheGuardian
from bettingTips import getLines
import classes
from Base import loadExcel
from Forbet import getUpcomingForbet

window = Tk()
window.title('Combobox')
window.geometry('500x400')

Label(window, text="Predictions", background='green', foreground="white", font=("Times New Roman", 15)).grid(row=0,
                                                                                                             column=1)
Label(window, text="Select the League :", font=("Times New Roman", 10)).grid(column=0, row=5, padx=10, pady=25)
Label(window, text="Select Home Team :", font=("Times New Roman", 10)).grid(column=0, row=6, padx=10, pady=25)
Label(window, text="Select Away Team :", font=("Times New Roman", 10)).grid(column=0, row=7, padx=10, pady=25)


def callbackLeague(eventObject):
    # changes list of teams to choose from and change settings for both teams' comboboxes
    global league
    league = classes.League(leagueChosen.get())
    HomeChosen.config(values=league.teams)
    AwayChosen.config(values=league.teams)
    HomeChosen.current(0)
    AwayChosen.current(1)
    global homeTeam
    homeTeam = classes.Team(league, HomeChosen.get())
    global awayTeam
    awayTeam = classes.Team(league, AwayChosen.get())


# combobox bound to callback function to choose the league
# state readonly do not allow to enter some random value
leagueChosen = ttk.Combobox(window, width=27, values=leagues, state="readonly")
leagueChosen.grid(column=1, row=5)
leagueChosen.current(0)
leagueChosen.bind("<<ComboboxSelected>>", callbackLeague)
league = classes.League(leagueChosen.get())
# at the beginning teams from la liga - current value of leagueChosen
realOdds = False  # default


def callbackHome(eventObject):
    global homeTeam
    homeTeam = classes.Team(league, HomeChosen.get())


def callbackAway(eventObject):
    global awayTeam
    awayTeam = classes.Team(league, AwayChosen.get())


# comboboxes for teams
HomeChosen = ttk.Combobox(window, width=27, values=league.teams, state="readonly")
HomeChosen.grid(column=1, row=6)
HomeChosen.current(0)
homeTeam = classes.Team(league, HomeChosen.get())
HomeChosen.bind("<<ComboboxSelected>>", callbackHome)

AwayChosen = ttk.Combobox(window, width=27, values=league.teams, state="readonly")
AwayChosen.grid(column=1, row=7)
AwayChosen.current(1)
awayTeam = classes.Team(league, AwayChosen.get())
AwayChosen.bind("<<ComboboxSelected>>", callbackAway)


# starts prediction() and gives us result
def buttonActivate():
    if awayTeam.name != homeTeam.name:
        print("checking")
        match = classes.Match(league, homeTeam, awayTeam)
        if realOdds:
            print(match.predictionOdds)
            print(getLines(league, homeTeam, awayTeam)[1])
        else:
            print(match.prediction)


# button check to activate prediction()
buttonCheck = Button(window, text="check", width=20, state=NORMAL, command=buttonActivate)
buttonCheck.grid(column=1, row=8)


# defines whether programs gives back real odds
def selection():
    global realOdds
    if var1.get() == 1:
        realOdds = True
    else:
        realOdds = False


# 1 - program tries to scrape real odds, 0 - only prediction
var1 = IntVar()
odds = Checkbutton(window, text="Real Odds", variable=var1, onvalue=1, offvalue=0, command=selection)
odds.grid(column=1, row=9)


def update():
    try:
        print("Updating from Sky Sport:")
        updateCSVSkySport()
        print("Success")
    except:
        try:
            print("Not possible \nUpdating from Flashscore:")
            updateCSVFlashscore()
            print("Success")
        except:
            print("Sorry, it's now impossible")
            return False


buttonUpdate = Button(window, text="update data", width=20, state=NORMAL, command=update)
buttonUpdate.grid(column=0, row=8)


def loadToExcel():
    try:
        loadExcel()
        print("Success")
    except:
        print("Not possible")


buttonLoad = Button(window, text="load excel", width=20, state=NORMAL, command=loadToExcel)
buttonLoad.grid(column=0, row=9)


def getUpcoming():
    try:
        print("Forbet")
        games = getUpcomingForbet(league.name, given_date=events_date)
        print("Success")
    except(Exception):
        try:
            print("The Guardian:")
            games = getUpcomingTheGuardian(league.name, given_date=events_date)
            print("Success")
        except(Exception):
            try:
                print("There was a problem\nFlashscore:")
                games = getUpcomingFlashscore(league.name, given_date=events_date)
                print("Success")
            except(Exception):
                print("Sorry, it's now impossible")
                return False

    for game in games:
        print('\n' + ' '.join(game) + '\n')
        if realOdds:
            print(prediction(league.name, game[1], game[2], realOdds=True))
            print(getLines(league, classes.Team(league, game[1]), classes.Team(league, game[2]))[1])
        else:
            print(prediction(league.name, game[1], game[2], realOdds=False))


buttonGet = Button(window, text="upcoming", width=20, state=NORMAL, command=getUpcoming)
buttonGet.grid(column=2, row=8)


def date_selection(eventObject):
    global events_date
    events_date = Date.get()


# today, tomorrow, nearest Saturday, nearest Sunday
dates = np.unique(
    np.array([date.today().strftime('%d-%m'), (date.today() + datetime.timedelta(days=1)).strftime('%d-%m'),
              (date.today() + datetime.timedelta(days=((12 - date.today().weekday()) % 7))).strftime('%d-%m'),
              (date.today() + datetime.timedelta(days=((13 - date.today().weekday()) % 7))).strftime(
                  '%d-%m')])).tolist()

Date = ttk.Combobox(window, width=15, values=dates, state="readonly")
Date.grid(column=2, row=10)
Date.current(0 if dates[0] == date.today().strftime('%d-%m') else len(dates) - 1)
Date.bind("<<ComboboxSelected>>", date_selection)
events_date = Date.get()


def Lines():
    try:
        print("The Guardian:")
        games = getUpcomingTheGuardian(league.name, given_date=events_date)
        print("Success\n")
    except:
        try:
            print("There was a problem\nFlashscore:")
            games = getUpcomingFlashscore(league.name, given_date=events_date)
            print("Success\n")
        except:
            print("Sorry, it's now impossible")
            return False
    for game in games:
        print('\n' + ' '.join(game) + '\n')
        print(getLines(league, classes.Team(league, game[1]), classes.Team(league, game[2]))[1])


buttonLines = Button(window, text="Tips", width=20, state=NORMAL, command=Lines)
buttonLines.grid(column=2, row=9)

window.mainloop()
