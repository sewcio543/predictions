import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter


data = pd.read_csv('AnalysisLaLiga.csv')

def addwinner():
    winner = []
    for row in data.values:
        if row[2] > row[3]:
            winner.append('H')
        elif row[2] == row[3]:
            winner.append('D')
        else:
            winner.append('A')

    data['winner'] = winner



