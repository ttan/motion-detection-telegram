import requests, glob, os
import sys

list_of_files = glob.glob('/root/motion/pics/*.jpg') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)

url = 'https://api.telegram.org/botxx:xxxx/' #REPLACE WITH BOT TOKEN, leaving 'bot' in the url
r1 = requests.post(url+'sendMessage', data={"chat_id": 12345678, "text": 'Motion detected'}) #REPLACE CHAT ID
fileName = latest_file
r3 = requests.post(url+'sendPhoto', files={'photo': open(fileName, 'rb')}, data={"chat_id": 12345678}) #REPLACE CHAT ID
