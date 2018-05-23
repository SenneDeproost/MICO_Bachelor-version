import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys
from scipy.interpolate import spline
import matplotlib

matplotlib.rcParams.update({'font.size': 22})

argv = sys.argv

file = argv[1]

dataRead = pd.read_csv(file, sep=",", header=None)

data = dataRead.values

episodes = data[:, 0]

productions = []

maxi = 0
maxiRow = 0

for row in data:
	summ = float(row[-3]) + float(row[-2]) + float(row[-1])
	productions.append(summ)
	if summ > maxi:
		maxi = summ
		maxiRow = row


episodes = episodes[0:2000]
productions = productions[0:2000]



print data
print maxi
print maxiRow

def ExpMovingAverage(values, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a =  np.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
    return a


#x_smooth =  np.linspace(np.array(episodes).min(), np.array(episodes).max(), 300)
#y_smooth = spline(episodes, productions, x_smooth)


plt.plot(episodes, productions, 'ro')

plt.plot(episodes, ExpMovingAverage(productions, int(argv[2])))

plt.xlabel('Episode')
plt.ylabel('Stroomproductie in kW')

#print "hihi"
#print convol


plt.show()
#plt.plot(x_smooth, y_smooth)


