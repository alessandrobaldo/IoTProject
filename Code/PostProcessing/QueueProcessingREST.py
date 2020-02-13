import cherrypy
import requests
import json
import time
import socket
import paho.mqtt.client as PahoMQTT
from QueueProcessingUnit import QueueProcessingUnit

q=QueueProcessingUnit()

class QueueProcessingRESTMQTT(object):
	exposed=True
	
	'''TIME SHIFT REQUEST DATA'''
	def GET(*uri,**params):
		if(uri[0]=="retrieve"):
			q.askDataSensors(params["pressure_id"],params["heart_id"],params["glucose_id"])

	'''iHEALTH ADAPTER PUTTING DATA INTO DB'''
	def PUT(*uri,**params):

		body=cherrypy.request.body.read()
		try:
			json_body=json.loads(body.decode('utf-8'))

		except:
			raise cherrypy.HTTPError(400,"ERROR body is empty")
		
		parameter=list(json_body.values())
		keys=list(json_body.keys())
		
		attributes=q.getInfoDb()["data_sensors"]

		for i in range(len(keys)):
			if(keys[i]!=attributes[i]):
				return json.dumps(return_res)
		print(json_body)
		q.sendDataDatabase("sensors",json_body)
		

	'''REGISTRY CATALOG REQUESTS INFORMATION'''
	def POST(*uri,**params):
		body=cherrypy.request.body.read()
		try:
			json_body=json.loads(body.decode('utf-8'))

		except:
			raise cherrypy.HTTPError(400,"ERROR body is empty")
		
		q.setData(json_body)
		print(json_body)
		return json.dumps(q.getData())

	def DELETE(*uri,**params):
		pass

	def __init__(self, clientID):
		self._paho_mqtt = PahoMQTT.Client(clientID, False)#false to avoud some errors 
		# register the callback
		self._paho_mqtt.on_connect = self.myOnConnect
		self._paho_mqtt.on_message = self.myOnMessageReceived
		#when you connect don't do the thing coded in the library, but my method of connection
		self.topic=q.getTopicPublisher()
		self.broker="iot.eclipse.org"
		self.subscribed=False

	def start(self):
		self._paho_mqtt.connect(self.broker, 1883)
		self._paho_mqtt.loop_start()

	def myOnConnect(self, paho_mqtt,userdata,flags,rc):
		print (f"Connected to {self.broker} with result code: {rc}")

	def stop(self):
		self._paho_mqtt.loop_stop()
		self._paho_mqtt.disconnect()

	'''PUBLISHING ON TELEGRAM CHANNEL'''
	def myPublish(self,message):
		self._paho_mqtt.publish(self.topic, json.dumps(message))
		

	def mySubscribe(self):
		if(self.subscribed==False):
			try:
				topic=q.getTopicsSubscriber()["telegram_triage"]
				print(topic)
				self._paho_mqtt.subscribe(topic, 2)
				self.subscribed=True
			except:
				print("The server you want to subscribe is not still online")

	def myUnsubscribe(self):
		topic=q.getTopicsSubscriber()["telegram_triage"]
		self._paho_mqtt.unsubscribe(topic)
		self.subscribed=False

	def myOnMessageReceived(self, paho_mqtt , userdata, msg):
			'''RECEIVING DATA FROM TELEGRAM ABOUT A NEW PATIENT'''
			
			message=json.loads(msg.payload)
			print(message)
			message["id_patient"]=q.getCurrentPatient()

			id1=message["pressure_id"]
			id2=message["heart_id"]
			id3=message["glucose_id"]
			time_stamp=message["time_stamp"]
			code=message["code"]
			data={
			"pressure_id":id1,
			"heart_id":id2,
			"glucose_id":id3,
			"code":code,
			"time_stamp":time_stamp
			}
			q.askDataSensors(id1,id2,id3)
			q.sendDataDatabase("patients",message)

			'''NOTIFYING TIME SHIFT OF THE ARRIVAL OF A NEW PATIENT'''
			r=requests.put("http://"+self.ip_others["time_shift"][0]+":"+self.ip_others["time_shift"][1],json.dumps(data))
			
if __name__=='__main__':
	conf = { '/': { 'request.dispatch': cherrypy.dispatch.MethodDispatcher(), 'tools.sessions.on': True } }
	# building the web service
	server=QueueProcessingRESTMQTT("queue_server")
	cherrypy.tree.mount(server, '/', conf)
	cherrypy.config.update({"server.socket_host": q.getAddress(), "server.socket_port": 8082})
	cherrypy.engine.start()

	server.start()
	
	q.configure()
	i=0
	while True:
		server.mySubscribe()
		q.processData()
		time.sleep(10)
		i+=1
		if(i==2):
			server.myPublish(q.getQueue())
			q.processPatient()
			i=0
	server.myUnsubscribe()
	server.stop()
	cherrypy.engine.block()