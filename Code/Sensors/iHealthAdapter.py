
import json
import datetime
import socket
import requests
import time
from EmulatedSensors import GlucoseSensor, PressureSensor, HeartSensor
import apiconfig as cfg
from flask import request, redirect


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

		#API

		self.client_id = cfg.CLIENT_ID
		self.client_secret = cfg.CLIENT_SECRET
		self.callback = cfg.CALLBACK_URI
		self.access_token = ''
		self.refresh_token = ''
		self.user_id = ''
		self.auth_url = cfg.AUTH_URL
		self.user_url = cfg.USER_DATA_URL
		self.app_url = cfg.ALL_DATA_URL
		self.response_type = 'code'  # default value for response_type
		self.APIName = 'OpenApiBP OpenApiSpO2 OpenApiUserInfo'  # an array of target API
		self.RequiredAPIName = 'OpenApiBP OpenApiSpO2 OpenApiUserInfo'  # it is must be selected for the authentication page
		self.IsNew = 'true'  # the system will be auto redirected to the sign up page

	def authorize(self):
		payload = {'client_id': self.client_id, 'response_type': self.response_type,
				   'redirect_uri': self.redirect_uri, 'APIName': self.APIName,
				   'RequiredAPIName': self.RequiredAPIName, 'IsNew': self.IsNew}
		r = requests.get(self.auth_url, params=payload)
		return r

	def callback(self):
		code = self.get_code()
		grant_type = 'authorization_code'   # is currently the only supported value
		payload = {'code': code, 'client_id': self.client_id, 'grant_type': grant_type,
				   'client_secret': self.client_secret, 'redirect_uri': self.redirect_uri}
		r = requests.get(self.auth_url, params=payload)
		self.access_token, self.refresh_token = self.get_tokens(r.text)
		self.user_id = self.get_user_id(r.text)
		return r.text

	def get_code(self):
		if 'code' not in request.args:
			return None
		return request.args['code']

	def get_tokens(self, data):
		resp = json.loads(data)
		if resp['AccessToken'] and resp['RefreshToken']:
			return resp['AccessToken'], resp['RefreshToken']
		else:
			return None, None # this should be handled as an error

	def get_user_id(self, data):
		resp = json.loads(data)
		if resp['UserID']:
			return resp['UserID']
		else:
			return None

	def get_blood_pressure(self):
		base_url = self.user_url+str(self.user_id)+'/bp/'
		BP = cfg.DATA_TYPES['OpenApiBP']
		payload = {'client_id': self.client_id, 'client_secret': self.client_secret,
				   'access_token': self.access_token, 'redirect_uri': self.redirect_uri,
				   'sc': BP['sc'], 'sv': BP['sv']}
		r = requests.get(base_url, params=payload)
		return r.text

	def get_blood_oxygen(self):
		base_url = self.user_url+str(self.user_id)+'/spo2/'
		spO2 = cfg.DATA_TYPES['OpenApiSpO2']
		print(sp02)
		payload = {'client_id': self.client_id, 'client_secret': self.client_secret,
				   'access_token': self.access_token, 'redirect_uri': self.redirect_uri,
				   'sc': spO2['sc'], 'sv': spO2['sv']}
		r = requests.get(base_url, params=payload)
		return r

	def getData(self):
		return self.my_data

	def getAddress(self):
		return self.address

	def setData(self,data):
		self.ip_others=data

	def configure(self):
		self.result=requests.post(self.catalog,json.dumps(self.my_data))
		self.ip_others=self.result.json()


	def getIps(self):
		return self.ip_others

	def sendDataQueue(self,data):
		r=requests.put("http://"+self.ip_others["queue_server"][0]+":"+self.ip_others["queue_server"][1],json.dumps(data))
		
	def getDataFromCloud(self, pressure_id,heart_id,glucose_id):
		now=datetime.datetime.now()
		timestamp=now.strftime('%Y-%m-%d %H:%M:%S')#,time.localtime(time.time()))
		
		try:
			rate=self.get_blood_oxygen
			print(rate)
		except:
			print("No value")
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
