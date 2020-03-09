import cherrypy
import requests
import json
import time
import socket
import paho.mqtt.client as PahoMQTT
from StatisticProcessingUnit import StatisticProcessingUnit

s=StatisticProcessingUnit()

class StatisticProcessingRESTMQTT(object):
	exposed=True


	def GET(*uri,**params):
		return s.getStatistics()

	def PUT(*uri,**params):
		pass

	'''DATA REQUESTED BY CATALOG'''
	def POST(*uri,**params):
		body=cherrypy.request.body.read()
		try:
			json_body=json.loads(body.decode('utf-8'))

		except:
			raise cherrypy.HTTPError(400,"ERROR body is empty")
		
		s.setData(json_body)
		return json.dumps(s.getData())

	def DELETE(*uri,**params):
		pass

	def __init__(self, clientID):
		self._paho_mqtt = PahoMQTT.Client(clientID, False)#false to avoud some errors 
		# register the callback
		self._paho_mqtt.on_connect = self.myOnConnect
		#when you connect don't do the thing coded in the library, but my method of connection
		self.topic=s.getTopicPublisher()
		self.broker="192.168.1.156"

	def start(self):
		self._paho_mqtt.connect(self.broker, 1883)
		self._paho_mqtt.loop_start()

	def myOnConnect(self, paho_mqtt,userdata,flags,rc):
		print (f"Connected to {self.broker} with result code: {rc}")

	def stop(self):
		self._paho_mqtt.loop_stop()
		self._paho_mqtt.disconnect()

	'''PUBLISHING ON BOT CHAT'''
	def myPublish(self,message):
		self._paho_mqtt.publish(self.topic, json.dumps(message))
		


if __name__=='__main__':
	conf = { '/': { 'request.dispatch': cherrypy.dispatch.MethodDispatcher(), 'tools.sessions.on': True } }
	# building the web service
	server=StatisticProcessingRESTMQTT("statistic_server")
	cherrypy.tree.mount(server, '/', conf)
	cherrypy.config.update({"server.socket_host": s.getAddress(), "server.socket_port": 8083})
	cherrypy.engine.start()

	server.start()
	s.configure()

	while True:
		time.sleep(10)
		s.processData()
		
	server.stop()
	cherrypy.engine.block()