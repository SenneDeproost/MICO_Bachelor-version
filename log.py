import csv as c
import time as t
import globals as g

timeStamp = int(t.time()) # time ins UNIX seconds
extension = '.csv'
directory = './logs/csv/'
fileName = str(timeStamp) + extension

#header = [["episode", "OJA", "joint action", "production", "total production"]]
header = [[g.gamma, g.learningRate, g.discount, g.epsilon, g.step, g.nActions]]

def createCSV():
	with open(fileName, 'w+') as File:
		writer = c.writer(File)
		#writer.writerows(header)

def appendCSV(row):
	with open(fileName, 'a') as File:
		writer = c.writer(File)
		writer.writerows(row)
