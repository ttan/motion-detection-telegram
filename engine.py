import glob, os, psutil, sys, subprocess
from telegram.ext import Updater, CommandHandler
import logging
print("---")
print("Starting Telegram bot for home surveillance")
print("v. 0.1 by @ttan_")
print("---")
print("daemonising...")

if os.fork(): exit(0)
os.umask(0) 
os.setsid() 
if os.fork(): exit(0)

sys.stdout.flush()
sys.stderr.flush()
si = file('/dev/null', 'r')
so = file('/dev/null', 'a+')
se = file('/dev/null', 'a+', 0)
os.dup2(si.fileno(), sys.stdin.fileno())
os.dup2(so.fileno(), sys.stdout.fileno())
os.dup2(se.fileno(), sys.stderr.fileno())

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(token='xx:xxxx') #Telegram bot token here
dispatcher = updater.dispatcher
chat_id = 12345 #telegram chat_id (user or group)

def take_snap(bot, update):
	bot.send_message(chat_id, text="Taking a snapshot, please wait...")
	res = subprocess.Popen(["fswebcam", "-r 1280x720", "grab.jpeg"], shell=False, stdout=subprocess.PIPE, cwd="/root/motion/pics");
	res.wait()
	bot.send_photo(chat_id, photo=open("/root/motion/pics/grab.jpeg", "rb"))
	
def clean(bot, update):
	directory='/root/motion/pics'
	os.chdir(directory)
	files=glob.glob('*.jpg')
	for filename in files:
	    os.remove(filename)
	bot.send_message(chat_id, text="All pictures deleted!")

def start(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
	print(update.message.chat_id)

def startMotion(bot, update):
	res = subprocess.Popen(["motion", "-c /root/motion/motion.conf"], shell=False, stdout=subprocess.PIPE, cwd="/root/motion")
	bot.send_message(chat_id, text="Motion detection started!")

def stopMotion(bot, update):
	PROCNAME = "motion"

	for proc in psutil.process_iter():
	    # check whether the process name matches
	    if proc.name() == PROCNAME:
	        proc.kill()

	bot.send_message(chat_id, text="Motion detection stopped!")

def checkMotion(bot, update):
	 ps = subprocess.check_output(('ps'))
	 if (ps.find("motion")) == -1:
	 	bot.send_message(chat_id, text="Motion detection not running.")
	 else:
	 	bot.send_message(chat_id, text="Motion detection is running!")

def sendLast(bot, update):
	list_of_files = glob.glob('/root/motion/pics/*.jpg') # * means all if need specific format then *.csv
	latest_file = max(list_of_files, key=os.path.getctime)

	file_handler = open(latest_file, 'rb')
	bot.send_photo(chat_id, photo=file_handler)

sendLast_handler = CommandHandler('sendlast', sendLast)
dispatcher.add_handler(sendLast_handler)

takeSnap_handler = CommandHandler('snap', take_snap)
dispatcher.add_handler(takeSnap_handler)

clean_handler = CommandHandler('cleanpics', clean)
dispatcher.add_handler(clean_handler)

startMotion_handler = CommandHandler('startmotion', startMotion)
dispatcher.add_handler(startMotion_handler)

stopMotion_handler = CommandHandler('stopmotion', stopMotion)
dispatcher.add_handler(stopMotion_handler)

checkMotion_handler = CommandHandler('checkmotion', checkMotion)
dispatcher.add_handler(checkMotion_handler)

if __name__ == '__main__':
    updater.start_polling()
    updater.idle()