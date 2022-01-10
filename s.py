import Base
import bettingTips
import classes
import Forbet

smsContent = ""
for league in Base.leagues:
    games = Forbet.getUpcomingForbet(league, f"22-12")
    if len(games) > 0:
        for game in games:
            tips = bettingTips.getLines(classes.League(league), classes.Team(league, game[1]),
                                        classes.Team(league, game[2]))[1]
            if len(tips) > 0:
                smsContent += " ".join(game) + '\n'
                for tip in tips:
                    smsContent += ' '.join(tip) + ', '
                smsContent += "\n"

    print(smsContent)

