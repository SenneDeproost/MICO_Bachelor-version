import csv as c
import time as t

timeStamp = int(t.time()) # time ins UNIX seconds
extension = '.csv'
directory = './logs/csv/'
fileName = str(timeStamp) + extension

header = [["episode", "OJA", "joint action", "production", "total production"]]

def createCSV():
	4
	#with open(fileName, 'w+') as File:
		#writer = c.writer(File)
	#	writer.writerows(header)

def appendCSV(row):
	4
#	with open(fileName, 'a') as File:
#		writer = c.writer(File)
#		writer.writerows(row)
