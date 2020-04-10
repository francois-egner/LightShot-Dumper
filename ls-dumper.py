import string
import itertools
import requests
from bs4 import BeautifulSoup
import time
import os.path
from os import path as fs
import os
import datetime
import sys


path = sys.argv[1]
id_length = 6
totalIDs = 0
processedIDs = 0
skippedIDs = 0
downloadedIDs = 0
existingIDs = [file.split(".")[0] for file in os.listdir(path)]
failedIDs = []
#Generate all possible IDs
alphabet = list(string.ascii_lowercase)
for number in range (0,10):
	alphabet.append(str(number))

file = open("failedIDs.txt",'r')
failedIDs = [id.rstrip("\n") for id in file.readlines()]
file.close()

combinations = list(itertools.combinations(alphabet, id_length));
ids = []
for comb in combinations:
	ids.append(''.join(comb))

totalIDs = len(combinations)

def clearScreen():
   if os.name == 'posix':
      os.system('clear')
   else:
      os.system('cls')

def downloadImage(url, path):
	content = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}).content
	soup = BeautifulSoup(content, "html.parser")
	urls = [img["src"] for img in soup.findAll("img")]
	if(str(urls[0]).startswith('https://i.imgur.com/')):
		picture = requests.get(urls[0])
		with open(path, 'wb') as f:
			f.write(picture.content)
			return 1
	else:
		return -1


print('Skipping already downloaded images...')
start = time.time()
for counter, id in enumerate(ids):
	timeForPic = 1
	processedIDs +=1
	url = 'https://prnt.sc/' + id
	finalPath = path + id + '.png'
	if(id in existingIDs):
		end = time.time()
		timeForPic = (end-start)/downloadedIDs
		pass
	elif id in failedIDs:
		end = time.time()
		timeForPic = (end-start)/downloadedIDs
		pass
	else:
		
		if downloadImage(url, finalPath) == 1:
			downloadedIDs +=1
		else:
			failedIDs.append("")
			file = open("failedIDs.txt","a")
			file.write(id + "\n")
			file.close()
		end = time.time()
		timeForPic = (end-start)/downloadedIDs
		
	
	if downloadedIDs != 0:
		clearScreen()
		remaining = totalIDs - len(existingIDs) -downloadedIDs - len(failedIDs)
		downloaded = len(existingIDs) + downloadedIDs
		failed = len(failedIDs)
		
		imagesPerSecond = 1/timeForPic
		TimeTillCompletion = (remaining / imagesPerSecond)
		percent = (totalIDs - remaining)/totalIDs * 100
		print("Downloaded: %d (%f%s) | Remaining: %d | FAILED: %d | Avg. Rate: %f img/s | Est. TTC: %s" % ( downloaded, percent,"%", remaining, failed,imagesPerSecond , str(datetime.timedelta(seconds=TimeTillCompletion))))
	