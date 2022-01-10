from outcome import findTeams, prediction, strengths
from bettingTips import getLines


class Team:
    def __init__(self, league, name):
        self.league = league
        self.name = name
        #self.accuracy = predictionAcc(self.league)[1][self.name]
        #self.strengths = strengths(self.league.name)[self.name]

    def __str__(self):
        return self.name

class Match:
    def __init__(self, league, homeTeam, awayTeam):
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
        self.league = league
        #self.lines, self.tips = getLines(self.league, self.homeTeam, self.awayTeam)[0], getLines(self.league, self.homeTeam, self.awayTeam)[1]
        self.prediction = prediction(self.league.name, self.homeTeam.name, self.awayTeam.name)
        self.predictionOdds = prediction(self.league.name, self.homeTeam.name, self.awayTeam.name, realOdds=True)
        if not self.predictionOdds[-5:].strip() == "able":
            self.lines = getLines(league, homeTeam, awayTeam)
        else:
            self.lines = None


    def __str__(self):
        return f"{self.league.name}:\n{self.homeTeam.name} vs {self.awayTeam.name}"



class League:
    def __init__(self, name):
        self.name = name
        self.teams, self.data = findTeams(self.name)
        #self.accuracy = predictionAcc(self)[0]


    def __str__(self):
        return self.name



