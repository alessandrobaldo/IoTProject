import time
import telepot
import json
import requests
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from threading import Timer


class TelegramHospitalChannel(object):
	def __init__(self):
		
		self.flagExit=False
		self.bot = telepot.Bot(self.token)
		MessageLoop(self.bot, {'chat': self.on_chat_message}).run_as_thread()

		self.catalog="http://192.168.1.102:8080"
		self.my_data={
		"telegram_hospital":
			{	
			"ip":socket.gethostbyname(socket.gethostname()),
			"port":8085,
			"chatId": "-1001154374015",
			"token":"907874511:AAHOw03gFpIn4qcza8Emz88FLJd3xNbX9r4",
			}
		}

	def configure(self):
		
		self.result=requests.post(self.catalog,json.dumps(self.my_data))

		self.mqtt=self.result.json()[0]
		self.ip_others=self.result.json()[1]
		
		print(json.dumps(self.mqtt,indent=4))
		print(json.dumps(self.ip_others,indent=4))
		
	def getFlag(self):
		return self.flagExit
		
	def send_message(self, message):
		self.bot.sendMessage(self.my_data["chatId"],message)

	def on_chat_message(self, msg):
		content_type, chat_type, chat_id = telepot.glance(msg)
		if (content_type == 'text'):
			txt = msg['text']
			if '/stop' in txt:
				self.bot.sendMessage(self.my_data["chatId"], "Program stopped!")
				self.flagExit=True

	def getIps(self):
		return self.ip_others

	def getTopicsSubscriber(self):
		return self.mqtt
	