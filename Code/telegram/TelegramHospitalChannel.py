import time
import telepot
import json
import requests
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from threading import Timer
import socket


class TelegramHospitalChannel(object):
	def __init__(self):
		
		s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		s.connect(('8.8.8.8',80))
		self.address=s.getsockname()[0]
		#self.catalog="http://192.168.1.103:8080"
		self.catalog=json.loads(open("catalog.json").read())["catalog"]
		'''
		self.my_data={
		"telegram_hospital":
			{	
			"ip":socket.gethostbyname(socket.gethostname()),
			"port":8085,
			"chatId": "-1001154374015",
			"token":"907874511:AAHOw03gFpIn4qcza8Emz88FLJd3xNbX9r4",
			}
		}'''
		self.my_data=json.loads(open("channelData.json").read())
		self.my_data["telegram_hospital"]["ip"]=self.address

		self.bot = telepot.Bot(self.my_data["telegram_hospital"]["token"])
		MessageLoop(self.bot, {'chat': self.on_chat_message}).run_as_thread()

	def getAddress(self):
		return self.address

	def getData(self):
		return self.my_data

	def setData(self,data):
		self.mqtt=data[0]
		self.ip_others=data[1]


	def configure(self):
		self.result=requests.post(self.catalog,json.dumps(self.my_data))

		self.mqtt=self.result.json()[0]
		self.ip_others=self.result.json()[1]
		
	def send_message(self, message):
		self.bot.sendMessage(self.my_data["telegram_hospital"]["chatId"],message,parse_mode="Markdown")

	def on_chat_message(self, msg):
		content_type, chat_type, chat_id = telepot.glance(msg)
		if (content_type == 'text'):
			txt = msg['text']
			if '/stop' in txt:
				self.bot.sendMessage(self.my_data["telegram_hospital"]["chatId"], "Program stopped!")


	def getIps(self):
		return self.ip_others

	def getTopicsSubscriber(self):
		return self.mqtt
	