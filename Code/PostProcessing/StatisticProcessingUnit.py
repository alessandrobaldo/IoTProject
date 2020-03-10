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
		self.statistics={
			"age":{
				"under25":0,
				"under45":0,
				"under55":0,
				"under65":0,
				"over65":0,
			},
			"gender":{
				"M":0,
				"F":0,
				"O":0,
			},
			"code":{
				"2":0,
				"3":0,
				"4":0,
				"5":0,
			},
			"unit":{

			},
			"obesity":0

		}
		self.last_call=0
		self.recall=0

		self.my_data=json.loads(open("statisticData.json").read())
		self.my_data["statistic_server"]["ip"]=self.address

	def getAddress(self):
		return self.address

	def getData(self):
		return self.my_data

	def setData(self,data):
		self.ip_others=data
		

	def configure(self):
		
		self.result=requests.post(self.catalog,json.dumps(self.my_data))

		self.ip_others=self.result.json()
	
	'''PROCESSING STATISTICS READ FROM DB'''
	def processData(self):
		try:
			r=requests.get("http://"+self.ip_others["db_server"][0]+":"+self.ip_others["db_server"][1]+"/statistics")
			self.dataToProcess=r.json()
			
			if bool(self.dataToProcess)==False:
				print("Statistic didn't change from the previous ones")
			else:
				try:
					self.statistics["age"]["under25"]=(self.statistics["age"]["under25"]*self.recall/(self.recall+1))+self.dataToProcess["age"]["under25"]/(self.recall+1)
				except:
					pass
				try:
					self.statistics["age"]["under45"]=(self.statistics["age"]["under45"]*self.recall/(self.recall+1))+self.dataToProcess["age"]["under45"]/(self.recall+1)
				except:
					pass
				try:
					self.statistics["age"]["under55"]=(self.statistics["age"]["under55"]*self.recall/(self.recall+1))+self.dataToProcess["age"]["under55"]/(self.recall+1)
				except:
					pass
				try:
					self.statistics["age"]["under65"]=(self.statistics["age"]["under65"]*self.recall/(self.recall+1))+self.dataToProcess["age"]["under65"]/(self.recall+1)
				except:
					pass
				try:
					self.statistics["age"]["over65"]=(self.statistics["age"]["over65"]*self.recall/(self.recall+1))+self.dataToProcess["age"]["over65"]/(self.recall+1)
				except:
					pass

				for key in self.dataToProcess["unit"]:
					try:
						self.statistics["unit"][key]=(self.statistics["unit"][key]*self.recall/(self.recall+1))+self.dataToProcess["unit"][key]/(self.recall+1)
					except:
						if(len(list(self.statistics["unit"].keys()))==0):
							self.statistics["unit"]={key:self.dataToProcess["unit"][key]/(self.recall+1)}
						else:
							list(self.statistics["unit"].keys()).append(key)
							self.statistics["unit"][key]=self.dataToProcess["unit"][key]/(self.recall+1)

				for key in self.dataToProcess["gender"]:
					try:
						self.statistics["gender"][key]=(self.statistics["gender"][key]*self.recall/(self.recall+1))+self.dataToProcess["gender"][key]/(self.recall+1)
					except:
						pass
				for key in self.dataToProcess["code"]:
					try:
						self.statistics["code"][key]=(self.statistics["code"][key]*self.recall/(self.recall+1))+self.dataToProcess["code"][key]/(self.recall+1)
					except:
						pass
				try:
					self.statistics["obesity"]=(self.statistics["obesity"]*self.recall/(self.recall+1))+self.dataToProcess["obesity"]/(self.recall+1)
				except:
					pass
				self.recall+=1

		except:
			print("Impossible to process data, DB server is not online")


	def getStatistics(self):
		return json.dumps(self.statistics)

	def getIps(self):
		return self.ip_others
