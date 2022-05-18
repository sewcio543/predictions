from tkinter import *
from tkinter import ttk
from Scraping import getUpcomingFlashscore, updateCSVFlashscore, getUpcomingTheGuardian, updateCSVSkySport
from datetime import date
import datetime
import numpy as np
from classes import Team, League, Match
from Base import loadExcel, leagues
import threading

# a simple GUI in tkinter


window = Tk()
window.title('Predictions')
window.geometry('500x350')

Label(window, text="Predictions", background='green', foreground="white", font=("Times New Roman", 15)).grid(row=0,
                                                                                                             column=1)
Label(window, text="Select the League :", font=(
    "Times New Roman", 10)).grid(column=0, row=5, padx=10, pady=25)
Label(window, text="Select home Team :", font=("Times New Roman", 10)).grid(
    column=0, row=6, padx=10, pady=25)
Label(window, text="Select Away Team :", font=("Times New Roman", 10)).grid(
    column=0, row=7, padx=10, pady=25)


def callbackLeague(a):
    # changes list of teams to choose from and change settings for both teams' comboboxes
    global league
    league = League(leagueCombo.get())
    homeCombo.config(values=league.teams)
    AwayCombo.config(values=league.teams)
    homeCombo.current(0)
    AwayCombo.current(1)
    global homeTeam
    homeTeam = Team(league, homeCombo.get())
    global awayTeam
    awayTeam = Team(league, AwayCombo.get())


# combobox bound to callback function to choose the league
# state readonly do not allow to enter some random value
leagueCombo = ttk.Combobox(window, width=27, values=leagues, state="readonly")
leagueCombo.grid(column=1, row=5)
leagueCombo.current(0)
leagueCombo.bind("<<ComboboxSelected>>", callbackLeague)
league = League(leagueCombo.get())


def callbackHome(a):
    global homeTeam
    homeTeam = Team(league, homeCombo.get())


def callbackAway(a):
    global awayTeam
    awayTeam = Team(league, AwayCombo.get())


# comboboxes for teams
homeCombo = ttk.Combobox(
    window, width=27, values=league.teams, state="readonly")
homeCombo.grid(column=1, row=6)
homeCombo.current(0)
homeTeam = Team(league, homeCombo.get())
homeCombo.bind("<<ComboboxSelected>>", callbackHome)

AwayCombo = ttk.Combobox(
    window, width=27, values=league.teams, state="readonly")
AwayCombo.grid(column=1, row=7)
AwayCombo.current(1)
awayTeam = Team(league, AwayCombo.get())
AwayCombo.bind("<<ComboboxSelected>>", callbackAway)


def buttonActivate():
    if awayTeam.name != homeTeam.name:
        match = Match(homeTeam, awayTeam)
        print(match.fullPrediction())


# button check to activate prediction()
buttonCheck = Button(window, text="check", width=20,
                     state=NORMAL, command=lambda: runAsync(buttonActivate))
buttonCheck.grid(column=1, row=8)


def runAsync(function):
    threading.Thread(target=function).start()


def update():
    try:
        print("Updating from Sky Sport:")
        updateCSVSkySport()
        print("Success")
    except Exception as exception:
        try:
            print(f"Not possible\n{exception}\nFlashscore:")
            updateCSVFlashscore()
            print("Success")
        except Exception as exception:
            print(f"Sorry, it's now impossible\n{exception}")
            return False


buttonUpdate = Button(window, text="update data",
                      width=20, state=NORMAL, command=lambda: runAsync(update))
buttonUpdate.grid(column=0, row=8)


def loadToExcel():
    try:
        loadExcel()
        print("Success")
    except Exception as exception:
        print(f"Not possible\n{exception}")


buttonLoad = Button(window, text="load excel", width=20,
                    state=NORMAL, command=lambda: runAsync(loadToExcel))
buttonLoad.grid(column=0, row=9)


def getUpcoming():
    try:
        print("The Guardian:")
        games = getUpcomingTheGuardian(league.name, given_date=events_date)
        if len(games):
            print("Success")
        else:
            print('not found')
    except Exception as exception:
        print(f"There was a problem\n{exception}\nFlashscore:")
        try:
            games = getUpcomingFlashscore(league.name, given_date=events_date)
            if len(games):
                print("Success")
            else:
                print('not found')
        except Exception as exception:
            print(f"Sorry, it's now impossible\n{exception}")
            return False

    for game in games:
        try:
            print(game[0], end=': ')
            match = Match(Team(league, game[1]), Team(league, game[2]))
            print(match.fullPrediction())
            print(match.valueBets(), "\n")
        except Exception as exc:
            print("We cannot get this game \n")
            print(exc)


buttonGet = Button(window, text="upcoming", width=20,
                   state=NORMAL, command=lambda: runAsync(getUpcoming))
buttonGet.grid(column=2, row=8)


def date_selection(a):
    global events_date
    events_date = Date.get()


# today, tomorrow, nearest Saturday, nearest Sunday
dates = np.unique(
    np.array([date.today().strftime('%d-%m'), (date.today() + datetime.timedelta(days=1)).strftime('%d-%m'),
              (date.today() + datetime.timedelta(days=((12 -
               date.today().weekday()) % 7))).strftime('%d-%m'),
              (date.today() + datetime.timedelta(days=((13 - date.today().weekday()) % 7))).strftime(
                  '%d-%m')])).tolist()

Date = ttk.Combobox(window, width=15, values=dates, state="readonly")
Date.grid(column=2, row=9)
Date.current(0 if dates[0] == date.today().strftime(
    '%d-%m') else len(dates) - 1)
Date.bind("<<ComboboxSelected>>", date_selection)
events_date = Date.get()

window.mainloop()
