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
		pass

	def PUT(*uri,**params):
		pass

	def POST(*uri,**params):
		return "online"

	def DELETE(*uri,**params):
		pass

	def __init__(self, clientID):
		self._paho_mqtt = PahoMQTT.Client(clientID, False)#false to avoud some errors 
		# register the callback
		self._paho_mqtt.on_connect = self.myOnConnect
		#when you connect don't do the thing coded in the library, but my method of connection
		self.topic=s.getTopicPublisher()
		self.broker="eclipse.mosquitto.org"

	def start(self):
		self._paho_mqtt.connect(self.broker, 1883)
		self._paho_mqtt.loop_start()

	def myOnConnect(self, paho_mqtt,userdata,flags,rc):
		print (f"Connected to {self.broker} with result code: {rc}")

	def stop(self):
		self._paho_mqtt.loop_stop()
		self._paho_mqtt.disconnect()

	def myPublish(self,message):
		# publish a message with a certain topic
		self._paho_mqtt.publish(self.topic, json.dumps(message))
		


if __name__=='__main__':
	conf = { '/': { 'request.dispatch': cherrypy.dispatch.MethodDispatcher(), 'tools.sessions.on': True } }
	# building the web service
	server=StatisticProcessingRESTMQTT("statistic_server")
	cherrypy.tree.mount(server, '/', conf)
	cherrypy.config.update({"server.socket_host": socket.gethostbyname(socket.gethostname()), "server.socket_port": 8083})
	cherrypy.engine.start()

	server.start()

	while True:
		s.configure()
		time.sleep(5)
	server.stop()
	cherrypy.engine.block()