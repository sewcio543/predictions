import pandas as pd
import numpy as np


class League:
    def __init__(self, name: str):
        from Base import leagues
        self.name = name
        self.id = leagues.index(self.name)
        # csv format contains all the games played in a particular league in season 2021/22
        # records follow a simple pattern: home team,away team,goals scored by home team,goals scored by away team
        self.csvFile = f'csv/{self.name}.csv'
        self.analysisFile = f'csv/Analysis{self.name}.csv'
        self.analysis = pd.read_csv(self.analysisFile).to_numpy()
        self.data = pd.read_csv(self.csvFile).to_numpy()
        self.teams = sorted(list(set(self.data[:, 0])))
        self.homeGoalsAverage = round(self.data[:, 2].sum() / self.data.shape[0], 4)
        self.awayGoalsAverage = round(self.data[:, 3].sum() / self.data.shape[0], 4)
        self.meanError = round(
            sum([abs(row[4] - row[2]) + abs(row[5] - row[3]) for row in self.analysis]) / (self.analysis.shape[0] * 2),
            2)

    def getTeams(self):
        teams_: list[Team] = []
        for team in self.teams:
            teams_.append(Team(self, team))
        return teams_

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Team:
    def __init__(self, league: League, name: str):
        from analyze import predictionAccTeam
        import outcome
        if name in league.teams:
            self.league = league
            self.name = name
            self.predictionAccuracy = predictionAccTeam(self)
            self.strengthAtHomeInAttack, self.strengthAtHomeInDefence, self.strengthAwayInAttack, self.strengthAwayInDefence = outcome.strengths(
                self)
        else:
            raise AttributeError(f'there is not the team named {name} in {league.name}')

    def numberOfMatches(self) -> int:
        return np.sum([self.league.data[:, 0:2].flatten() == self.name], axis=1)[0]

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Match:
    oddsKeys = ['Wynik meczu (z wyłączeniem dogrywki)', 'Gole Powyżej/Poniżej', 'Oba zespoły strzelą gola',
                'Dokładny wynik', 'Podwójna szansa']
    descriptions = ['1', 'X', '2', 'BTTS', 'NBTTS', '-2.5', '+2,5', '1X', '2X']

    def __init__(self, homeTeam: Team, awayTeam: Team):
        import outcome
        import Betclic
        if awayTeam.league.name == homeTeam.league.name:
            self.homeTeam = homeTeam
            self.awayTeam = awayTeam
            self.league = homeTeam.league
        else:
            raise AttributeError('Model can only predict league games')

        # expected home goals = home team strength in attack at home * away team strength away in defence * average of leagues goals scored by home team
        # expected away goals = away team strength in attack away * home team strength home in defence * average of leagues goals scored by away team
        self.expectedHomeScore: float = round(
            homeTeam.strengthAtHomeInAttack * awayTeam.strengthAwayInDefence * self.league.homeGoalsAverage, 3)
        self.expectedAwayScore: float = round(
            awayTeam.strengthAwayInAttack * homeTeam.strengthAtHomeInDefence * self.league.awayGoalsAverage, 3)
        self.realOdds = Betclic.betclicOdds(self)
        self.prediction, self.homeWinProbability, self.tieProbability, self.awayWinProbability, self.bttsProbability, self.under3Probability, self.scoresTable = outcome.prediction(
            self, realOdds=True)
        self.nbttsProbability = round(100 - self.bttsProbability,2 )
        self.over3Probability = round(100 - self.under3Probability, 2)
        self.x1Probability = self.tieProbability + self.homeWinProbability
        self.x2Probability = self.tieProbability + self.awayWinProbability

    def lines(self) -> list[tuple]:
        from outcome import getOdds
        oddsList = getOdds(self)
        probabilities = [self.homeWinProbability, self.tieProbability, self.awayWinProbability, self.bttsProbability,
                         self.nbttsProbability,
                         self.under3Probability, self.over3Probability]
        lines = [round(probability * odds / 100, 2) for probability, odds in zip(probabilities, oddsList)]

        details = list(zip(["bet: " + description for description in self.descriptions], [f"value: {x}" for x in lines],
                           [f"real: {odds}" for odds in oddsList],
                           [f"{probability} %" for probability in probabilities]))
        return details

    def valueBets(self, value: float = 1.2):
        return [detail for detail in self.lines() if float(detail[1][-4:]) > value and float(detail[3][:-2]) > 30]

    def __str__(self):
        return f"{self.league.name}:\n{self.homeTeam.name} vs {self.awayTeam.name}"

    def __repr__(self):
        return f"{self.league.name}:\n{self.homeTeam.name} vs {self.awayTeam.name}"


if __name__ == '__main__':
    ls = League("PremierLeague")
    print(ls.meanError)
    m = Match(Team(ls, 'West Ham'), Team(ls, 'Watford'))
    # t = Team(ls, 'Elche')
    print(m.lines())
    print(m.valueBets())
    # print(m.valueBets())
