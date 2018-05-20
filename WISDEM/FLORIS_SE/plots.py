import matplotlib.pyplot as plt
#import NREL5_calc.py as c
import pandas as pd

file = "1526680660.csv"

dataRead = pd.read_csv(file, sep=",", header=None)

data = dataRead.values

episodes = data[:, 0]

res = []
ojas = []


for row in data:
    episode = row[0]
    oja = row[1] + row[2] + row[3]
    res.append([episode, oja])
    ojas.append(oja)

print res

plt.plot(range(1, len(ojas)), ojas)
plt.show()
