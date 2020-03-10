import time
import telepot
import json
import requests
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import paho.mqtt.client as PahoMQTT
import socket
from telegram.error import RetryAfter,TimedOut
import matplotlib.pyplot as plt
import matplotlib as mtp
mtp.use('agg')

class botTriage(object):
	def __init__(self):

		s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		s.connect(('8.8.8.8',80))
		self.address=s.getsockname()[0]
		#self.catalog="http://192.168.1.103:8080"
		self.catalog=json.loads(open("catalog.json").read())["catalog"]
		'''
		self.my_data={
		"telegram_triage":
			{	
			"ip":socket.gethostbyname(socket.gethostname()),
			"port":8086,
			"chatId": "359387363",
			"token":"957562924:AAFlHxtAxnFf02QF1U6Phvle2bH_wVEd1ns",
			"topic":["inputdata"],
			"subscriber":["queue_server"],
			}
		}'''

		self.my_data=json.loads(open("triageData.json").read())
		self.my_data["telegram_triage"]["ip"]=self.address


		self.js={}
		self.readyToSend=False

		self.flagName = False
		self.flagSurname = False
		self.flagAge = False
		self.flagGender = False
		self.flagWeight = False
		self.flagHeight = False
		self.flagCod = False
		self.flagRep = False
		self.flagSh = False
		self.flagSg = False
		self.flagSp = False
		self.flagExit= False
		#self.resourceUrl = rU
		self.bot = telepot.Bot(self.my_data["telegram_triage"]["token"])
		# creating the buttons
		self.keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Insert data', callback_data='Insert')],[InlineKeyboardButton(text="Statistics", callback_data='statistics')]])
		
		self.bot.sendMessage(self.my_data["telegram_triage"]["chatId"], 'Welcome! Choose an option:', reply_markup = self.keyboard)
		

		# associating the button with the callbacks
		MessageLoop(self.bot, {'chat': self.on_chat_message,'callback_query': self.on_callback_query}).run_as_thread()

	def getAddress(self):
		return self.address

	def getData(self):
		return self.my_data
	
	def setData(self,data):
		self.ip_others=data[0]
		self.available_sensors=data[1]

	def configure(self):
		
		self.result=requests.post(self.catalog,json.dumps(self.my_data))

		self.ip_others=self.result.json()[0]
		self.available_sensors=self.result.json()[1]

	def on_chat_message(self, msg):
		content_type, chat_type, self.chat_id = telepot.glance(msg)
		self.js={}
		if (content_type == 'text'):
			txt = msg['text']
			if '/exit' in txt:
				self.flagExit=True
		if self.flagName == True and self.flagExit == False:
			self.name = msg['text']
			self.flagName = False
			self.flagSurname = True
			self.bot.sendMessage(self.chat_id, 'Surname:')
		elif self.flagSurname == True and self.flagExit == False:
			self.surname = msg['text']
			self.flagSurname = False
			self.flagAge = True
			self.bot.sendMessage(self.chat_id, 'Age:')
		elif self.flagAge == True and self.flagExit == False:
			self.age = msg['text']
			if self.age.isnumeric():
				self.flagAge = False
				self.flagGender = True
				self.bot.sendMessage(self.chat_id, 'Gender (M, F, O):')
			else:
				self.bot.sendMessage(chat_id, 'Error! Enter a valide age, it must be a number.')
		elif self.flagGender == True and self.flagExit == False:
			self.gender = msg['text']
			if self.gender!='M' and self.gender!='F' and self.gender!='O':
				self.bot.sendMessage(self.chat_id, 'Error! Enter a valide gender, it could be M(male), F(female) or O(other).')
			
			else:
				self.flagGender = False
				self.flagWeight = True
				self.bot.sendMessage(self.chat_id, 'Weight (kg):')
		elif self.flagWeight == True and self.flagExit == False:
			self.weight = msg['text']
			if self.weight.isnumeric():
				self.flagWeight = False
				self.flagHeight = True
				self.bot.sendMessage(self.chat_id, 'Height (cm):')
			else:
				self.bot.sendMessage(self.chat_id, 'Error! Enter a valide weight(kg), it must be a number.')
		elif self.flagHeight == True and self.flagExit == False:
			self.height = msg['text']
			if self.height.isnumeric():
				self.flagHeight = False
				self.flagCod = True
				self.bot.sendMessage(self.chat_id, 'Code (2,3,4, or 5):')
			else:
				self.bot.sendMessage(self.chat_id, 'Error! Enter a valide height(cm), it must be a number.')
		elif self.flagCod == True and self.flagExit == False:
			self.code = msg['text']
			if int(self.code)!=2 and int(self.code)!=3 and int(self.code)!=4 and int(self.code)!=5:
				self.bot.sendMessage(self.chat_id, 'Error! Enter a valide code, it could be 2,3,4 or 5.')
			else:
				self.flagCod = False
				self.flagRep = True
				self.bot.sendMessage(self.chat_id, 'Unit:')
		elif self.flagRep == True and self.flagExit == False:
			self.unit = msg['text']
			self.flagRep = False
			self.flagSp = True
			self.listpr=[]
			for n in self.available_sensors["pressure"]:
				self.listpr.append(n)
			self.bot.sendMessage(self.chat_id, 'Choose a pressure sensors available - '+str(self.listpr))

		elif self.flagSp == True and self.flagExit == False:
			self.IDpressure = msg['text']
			self.pr=0
			print(self.listpr)
			for n in self.listpr:
				if(self.IDpressure==str(n)):
					self.pr=n
			if self.pr==0:
				self.bot.sendMessage(self.chat_id, 'INVALID ID! Choose one of the pressure sensors available - '+str(self.listpr))
			else:
				self.flagSp = False
				self.flagSg = True
				self.listgl=[]
				for n in self.available_sensors["glucose"]:
					self.listgl.append(n)
				self.bot.sendMessage(self.chat_id, 'Choose a glucose sensors available - '+str(self.listgl))

		elif self.flagSg == True and self.flagExit == False:
			self.IDglucose = msg['text']

			self.gl=0
			print(self.listgl)
			for n in self.listgl:
				if(self.IDglucose==str(n)):
					self.gl=n
			if self.gl==0:
				self.bot.sendMessage(self.chat_id, 'INVALID ID! Choose one of the glucose sensors available - '+str(self.listgl))
			else:
				self.flagSg = False
				self.flagSh = True
				self.listhe=[]
				for n in self.available_sensors["heart"]:
					self.listhe.append(n)
				self.bot.sendMessage(self.chat_id, 'Choose a heart sensors available - '+str(self.listhe))

		elif self.flagSh == True and self.flagExit == False:
			self.IDheart = msg['text']

			self.he=0
			print(self.listhe)
			for n in self.listhe:
				if(self.IDheart==str(n)):
					self.he=n
			if self.he==0:
				self.bot.sendMessage(self.chat_id, 'INVALID ID! Choose one of the heart sensors available - '+str(self.listhe))
			else:
				self.sens={
					"pressure":self.pr,
					"glucose":self.gl,
					"heart":self.he
				}
				res=requests.put(self.catalog, json.dumps(self.sens))
				newSensors=res.json()
				self.available_sensors=newSensors
				self.flagSh = False
				self.js = {
					'id_patient':0,
					'name': self.name, 
					'surname': self.surname,
					'age': self.age,
					'gender': self.gender,
					'weight': self.weight,
					'height': self.height,
					'code': self.code,
					'unit': self.unit,
					'pressure_id': self.IDpressure,
					'heart_id': self.IDheart,
					'glucose_id': self.IDglucose,
					'time_stamp':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
					}
				print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
				self.readyToSend=True
				self.bot.sendMessage(self.chat_id, 'Patient registered succesfully!')
				print('REGISTERED')
				# sending a message with buttons
				self.bot.sendMessage(self.chat_id, 'Choose an option:', reply_markup = self.keyboard)
			
		else:
			# sending a message with buttons
			self.bot.sendMessage(self.chat_id, 'Choose an option:', reply_markup = self.keyboard)

	def isReadyToSend(self):
		return self.readyToSend
		
	def readyData(self):
		self.readyToSend=False
		return json.dumps(self.js)

	def on_callback_query(self, msg):
		# data about the pressed button
		self.js={}
		query_id, self.chat_id, query_data = telepot.glance(msg, flavor='callback_query')
		print('callback:', query_id, self.chat_id, query_data)
		# checking what button is been pressed
		if (query_data == 'statistics'):
			self.bot.sendMessage(self.chat_id, 'Print statistics!')
			r=requests.get("http://"+self.ip_others["statistic_server"][0]+":"+self.ip_others["statistic_server"][1])
			stat=r.json()

			print(stat)

			labels=[]
			heights=[]
			for key in stat["age"].keys():
				labels.append(key)
				heights.append(stat["age"][key])

			fig1=plt.figure()
			plt.bar(labels,heights)
			plt.title("Age ranges")
			plt.xlabel("Age")
			plt.ylabel("Frequency")
			plt.savefig("Age.png")
			plt.close()

	
			self.bot.sendPhoto(self.chat_id,open("Age.png","rb"),caption=None)

			labels=[]
			heights=[]
			for key in stat["unit"].keys():
				labels.append(key)
				heights.append(stat["unit"][key])

			fig2=plt.figure()
			plt.bar(labels,heights)
			plt.title("Unit occupancies")
			plt.xlabel("Units")
			plt.ylabel("Frequency")
			plt.savefig("Unit.png")
			plt.close()

			self.bot.sendPhoto(self.chat_id,open("Unit.png","rb"),caption=None)


			labels=[]
			heights=[]
			for key in stat["code"].keys():
				labels.append(key)
				heights.append(stat["code"][key])

			fig3=plt.bar(labels,heights)
			plt.title("Code classes")
			plt.xlabel("Code")
			plt.ylabel("Frequency")
			plt.savefig("Code.png")
			plt.close()

			self.bot.sendPhoto(self.chat_id,open("Code.png","rb"),caption=None)

			labels=[]
			heights=[]
			for key in stat["gender"].keys():
				labels.append(key)
				heights.append(stat["gender"][key])

			fig4=plt.bar(labels,heights)
			plt.title("Gender frequencies")
			plt.xlabel("Gender")
			plt.ylabel("Frequency")
			plt.savefig("Gender.png")
			plt.close()

			self.bot.sendPhoto(self.chat_id,open("Gender.png","rb"),caption=None)



			self.bot.sendMessage(self.chat_id,"Obseity data:"+str(stat["obesity"])+" patients")
			self.bot.sendMessage(self.chat_id, 'Choose an option:', reply_markup = self.keyboard)
		elif (query_data == 'Insert'):
			# insert button pressed, now it's possible to start to insert patient's data
			self.flagName = True
			self.bot.sendMessage(self.chat_id, 'Name:')

	def send_message(self, message):
		self.bot.sendMessage(self.chat_id, message)

	def getIps(self):
		return self.ip_others

	def getTopicPublisher(self):
		return self.my_data["telegram_triage"]["topic"][0]