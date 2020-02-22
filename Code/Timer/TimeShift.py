import json
import datetime
import socket
import requests

class TimeShift(object):
	def __init__(self):
		s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		s.connect(('8.8.8.8',80))
		self.address=s.getsockname()[0]

		'''SAVING NEXT PROCESSING TIME FOR EACH PATIENT'''
		self.scheduling={
		"2":[],
		"3":[],
		"4":[],
		"5":[],
		}

		#self.catalog="http://192.168.1.103:8080"
		self.catalog=json.loads(open("catalog.json").read())["catalog"]
		'''
		self.my_data={
		"time_shift":
		{	
		"ip":socket.gethostbyname(socket.gethostname()),
		"port":8087
		}
		}'''
		self.my_data=json.loads(open("timeShiftData.json").read())
		self.my_data["time_shift"]["ip"]=self.address

	def getAddress(self):
		return self.address

	def getData(self):
		return self.my_data

	def setData(self,data):
		self.ip_others=data


	def configure(self):
		self.result=requests.post(self.catalog,json.dumps(self.my_data))
		self.ip_others=self.result.json()

	def sendAlert(self):

		for key in self.scheduling.keys():
			if(key=="2"):
				for elem in self.scheduling[key]:
					if((datetime.datetime.now()-datetime.datetime.strptime(elem["last_measurement"],'%Y-%m-%d %H:%M:%S')).total_seconds()>=60):
						r=requests.get("http://"+self.ip_others["queue_server"][0]+":"+self.ip_others["queue_server"][1]+"/retrieve?pressure_id="+elem["pressure_id"]+"&heart_id="+elem["heart_id"]+"&glucose_id="+elem["glucose_id"])
			elif(key=="3"):
				for elem in self.scheduling[key]:
					if((datetime.datetime.now()-datetime.datetime.strptime(elem["last_measurement"],'%Y-%m-%d %H:%M:%S')).total_seconds()>=240):
						r=requests.get("http://"+self.ip_others["queue_server"][0]+":"+self.ip_others["queue_server"][1]+"/retrieve?pressure_id="+elem["pressure_id"]+"&heart_id="+elem["heart_id"]+"&glucose_id="+elem["glucose_id"])
			elif(key=="4"):
				for elem in self.scheduling[key]:
					if((datetime.datetime.now()-datetime.datetime.strptime(elem["last_measurement"],'%Y-%m-%d %H:%M:%S')).total_seconds()>=480):
						r=requests.get("http://"+self.ip_others["queue_server"][0]+":"+self.ip_others["queue_server"][1]+"/retrieve?pressure_id="+elem["pressure_id"]+"&heart_id="+elem["heart_id"]+"&glucose_id="+elem["glucose_id"])
			elif(key=="5"):
				for elem in self.scheduling[key]:
					if((datetime.datetime.now()-datetime.datetime.strptime(elem["last_measurement"],'%Y-%m-%d %H:%M:%S')).total_seconds()>=960):
						r=requests.get("http://"+self.ip_others["queue_server"][0]+":"+self.ip_others["queue_server"][1]+"/retrieve?pressure_id="+elem["pressure_id"]+"&heart_id="+elem["heart_id"]+"&glucose_id="+elem["glucose_id"])

	
	def addToScheduling(self, data):
		data=json.loads(data)
		obj={
		"pressure_id":data["pressure_id"],
		"heart_id":data["heart_id"],
		"glucose_id":data["glucose_id"],
		"last_measurement":data["time_stamp"]
		}

		self.scheduling[data["code"]].append(obj)

	def removeFromScheduling(self,code,pressure_id,heart_id,glucose_id):
		for i in range(len(self.scheduling[str(code)])):
			if(self.scheduling[str(code)][i]["pressure_id"]==pressure_id and self.scheduling[str(code)][i]["heart_id"]==heart_id and self.scheduling[str(code)][i]["glucose_id"]==glucose_id):
				del self.scheduling[str(code)][i]

