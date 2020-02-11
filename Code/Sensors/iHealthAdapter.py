
import json
import datetime
import socket
import requests
import time
from EmulatedSensors import GlucoseSensor, PressureSensor, HeartSensor


class iHealthAdapter(object):
	def __init__(self):
		s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		s.connect(('8.8.8.8',80))
		self.address=s.getsockname()[0]

		#self.catalog="http://192.168.1.103:8080"
		self.catalog=json.loads(open("catalog.json").read())["catalog"]
		'''
		self.my_data={
			"ihealth_adapter":
				{	
				"ip":socket.gethostbyname(socket.gethostname()),
				"port":8084
		}
		}'''
		self.emulated_pressure=PressureSensor()
		self.emulated_heart=HeartSensor()
		self.emulated_glucose=GlucoseSensor()

		self.my_data=json.loads(open("iHealthData.json").read())
		self.my_data["ihealth_adapter"]["ip"]=self.address

	def getData(self):
		return self.my_data

	def getAddress(self):
		return self.address

	def setData(self,data):
		self.ip_others=data
		print(json.dumps(self.ip_others,indent=4))

	def configure(self):
		self.result=requests.post(self.catalog,json.dumps(self.my_data))
		self.ip_others=self.result.json()
		print(json.dumps(self.ip_others,indent=4))


	def getIps(self):
		return self.ip_others

	def sendDataQueue(self,data):
		r=requests.put("http://"+self.ip_others["queue_server"][0]+":"+self.ip_others["queue_server"][1],json.dumps(data))
		
	'''OBTAINING DATA FROM BOTH REAL AND EMULATED SENSORS'''
	def getDataFromCloud(self, pressure_id,heart_id,glucose_id):
		timestamp=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
		data={
		"pressure_id":pressure_id,
		"heart_id":heart_id,
		"glucose_id":glucose_id,
		"pressure_min":json.loads(self.emulated_pressure.getMeasurement())["min"],
		"pressure_max":json.loads(self.emulated_pressure.getMeasurement())["max"],
		"rate":json.loads(self.emulated_heart.getMeasurement())["rate"],
		"glucose":json.loads(self.emulated_glucose.getMeasurement())["glucose"],
		"time_stamp":timestamp
		}
		return json.dumps(data)
		#retrieving data from cloud + glucose
