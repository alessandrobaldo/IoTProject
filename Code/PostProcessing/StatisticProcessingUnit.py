import json
import time
import socket
import requests

class StatisticProcessingUnit(object):
	
	def __init__(self):
		s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		s.connect(('8.8.8.8',80))
		self.address=s.getsockname()[0]
		#self.catalog="http://192.168.1.103:8080"
		self.catalog=json.loads(open("catalog.json").read())["catalog"]
		'''
		self.my_data={
		"statistic_server":
		{	
		"ip":socket.gethostbyname(socket.gethostname()),
		"port":8083,
		"topic":["statistic"],
		"subscriber":["telegram_triage"]
		}
		}'''
		self.statistics={}
		self.recall=0

		self.my_data=json.loads(open("statisticData.json").read())
		self.my_data["statistic_server"]["ip"]=self.address

	def getAddress(self):
		return self.address

	def getData(self):
		return self.my_data

	def setData(self,data):
		self.mqtt=data[0]
		self.ip_others=data[1]

		print(json.dumps(self.mqtt,indent=4))
		print(json.dumps(self.ip_others,indent=4))

	def configure(self):
		
		self.result=requests.post(self.catalog,json.dumps(self.my_data))

		self.mqtt=self.result.json()[0]
		self.ip_others=self.result.json()[1]

		print(json.dumps(self.mqtt,indent=4))
		print(json.dumps(self.ip_others,indent=4))
	
	'''PROCESSING STATISTICS READ FROM DB'''
	def processData(self, data):
		r=requests.get("http://"+self.ip_others["db_server"][0]+":"+self.ip_others["db_server"][1]+"/statistics")
		self.dataToProcess=r.json()
		if not self.statistics:
			self.statistics=self.dataToProcess
			self.recall+=1
		else:
			self.statistics["age"]["under25"]=self.statistics["age"]["under25"]*self.recall/(self.recall+1)+self.dataToProcess["age"]["under25"]/(self.recall+1)
			self.statistics["age"]["under45"]=self.statistics["age"]["under45"]*self.recall/(self.recall+1)+self.dataToProcess["age"]["under45"]/(self.recall+1)
			self.statistics["age"]["under55"]=self.statistics["age"]["under55"]*self.recall/(self.recall+1)+self.dataToProcess["age"]["under55"]/(self.recall+1)
			self.statistics["age"]["under65"]=self.statistics["age"]["under65"]*self.recall/(self.recall+1)+self.dataToProcess["age"]["under65"]/(self.recall+1)
			self.statistics["age"]["over65"]=self.statistics["age"]["over65"]*self.recall/(self.recall+1)+self.dataToProcess["age"]["over65"]/(self.recall+1)

			for key in self.statistics["unit"]:
				self.statistics["unit"][key]=self.statistics["unit"][key]*self.recall/(self.recall+1)+self.dataToProcess["unit"][key]/(self.recall+1)

			for key in self.statistics["gender"]:
				self.statistics["gender"][key]=self.statistics["gender"][key]*self.recall/(self.recall+1)+self.dataToProcess["gender"][key]/(self.recall+1)

			for key in self.statistics["code"]:
				self.statistics["code"][key]=self.statistics["code"][key]*self.recall/(self.recall+1)+self.dataToProcess["code"][key]/(self.recall+1)

			self.statistics["obesity"]=self.statistics["obesity"]*self.recall/(self.recall+1)+self.dataToProcess["obesity"]/(self.recall+1)

			self.recall+=1

		return self.statistics


	def getIps(self):
		return self.ip_others

	def getTopicsSubscriber(self):
		return self.mqtt

	def getTopicPublisher(self):
		return self.my_data["statistic_server"]["topic"][0]