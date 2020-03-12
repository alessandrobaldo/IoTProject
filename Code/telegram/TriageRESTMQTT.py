import paho.mqtt.client as PahoMQTT
import time
import json
import cherrypy
import socket
from TelegramTriage import botTriage
import telepot
import urllib3

t=botTriage()

class TriageRESTMQTT(object):
	exposed=True
	def __init__(self, clientID):
		self.clientID = clientID
		self.topic = t.getTopicPublisher()
		self.broker = "192.168.1.103"
		self.status=''

		self._paho_mqtt = PahoMQTT.Client(clientID, False)
		self._paho_mqtt.on_connect = self.myOnConnect
		self.message={}
		
	def start (self):
		self._paho_mqtt.connect(self.broker, 1883)
		self._paho_mqtt.loop_start()

	def stop (self):
		self._paho_mqtt.loop_stop()
		self._paho_mqtt.disconnect()


	def myOnConnect (self, paho_mqtt, userdata, flags, rc):
		print ("Connected to %s with result code: %d" % (self.broker, rc))

		
	'''PUBLISHING DATA TO QUEUE ABOUT NEW PATIENT'''
	def myPublish(self):
		self.message=json.loads(t.readyData())
		for mess in self.message:
			self._paho_mqtt.publish(self.topic, json.dumps(mess), 2)

		

	def GET(*uri,**params):
		pass

	def PUT(*uri,**params):
		pass

	'''DATA REQUESTED BY CATALOG'''
	def POST(*uri,**params):
		body=cherrypy.request.body.read()
		try:
			json_body=json.loads(body.decode('utf-8'))
		except:
			raise cherrypy.HTTPError(400,"ERROR body is empty")
		

		t.setData(json_body)
		return json.dumps(t.getData())

	def DELETE(*uri,**params):
		pass

if __name__ == "__main__":
	conf = { '/': { 'request.dispatch': cherrypy.dispatch.MethodDispatcher(), 'tools.sessions.on': True } }
	# building the web service
	server=TriageRESTMQTT("telegram_triage")
	cherrypy.tree.mount(server, '/', conf)
	cherrypy.config.update({"server.socket_host": t.getAddress(), "server.socket_port": 8086})
	cherrypy.engine.start()
	i=0
	server.start()
	t.configure()
	while True:		
		while(t.isReadyToSend()):
			server.myPublish()
		time.sleep(10)

	server.stop()
	cherrypy.engine.block()
