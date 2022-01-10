from outcome import prediction

descriptions = ['1', 'X', '2', 'BTTS', 'NBTTS', '-2.5', '+2,5', '1X', '2X']


def getLines(league, homeTeam, awayTeam):
    analysis = prediction(league.name, homeTeam.name, awayTeam.name, betting=True)
    line = [round((analysis[i] * analysis[i + 1]) / 100, 2) for i in range(0, len(analysis), 2)]
    chances = [analysis[i] for i in range(1, len(analysis), 2)]
    details = list(zip(["bet: " + description for description in descriptions], [f"value: {x}" for x in line],
                       [f"real: {analysis[x]}" for x in range(0, len(analysis), 2)], [f"{x} %" for x in chances]))
    return details, [detail for detail in details if float(detail[1][-4:]) > 1.2 and float(detail[3][:-2]) > 30]

