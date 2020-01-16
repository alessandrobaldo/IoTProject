import paho.mqtt.client as PahoMQTT
import time
import json
import socket
import cherrypy
from TelegramHospitalChannel import TelegramHospitalChannel
t=TelegramHospitalChannel()

class ChannelRESTMQTT(object):
	def __init__(self, clientID):
		self.clientID = clientID
		self.broker="127.0.0.1"

		self._paho_mqtt = PahoMQTT.Client(clientID, False)
		self._paho_mqtt.on_connect = self.myOnConnect
		self._paho_mqtt.on_message = self.myOnMessageReceived

		self.subscribed=False

	def start (self):
		self._paho_mqtt.connect(self.broker, 1883)
		self._paho_mqtt.loop_start()

	def stop (self):
		self._paho_mqtt.loop_stop()
		self._paho_mqtt.disconnect()

	def myOnConnect (self, paho_mqtt, userdata, flags, rc):
		print ("Connected to %s with result code: %d" % (self.broker, rc))

	def myOnMessageReceived (self, paho_mqtt , userdata, msg):
		message=json.loads(msg.payload)
		t.send_message(message)

	def mySubscribe(self):
		if(self.subscribed==False):
			try:
				topic=t.getTopicsSubscriber()["queue_server"]
				self._paho_mqtt.subscribe(topic, 2)
				self.subscribed=True
			except:
				print("The server you want to subscribe is not still online")

	def myUnsubscribe(self):
		topic=t.getTopicsSubscriber()["queue_server"]
		self._paho_mqtt.unsubscribe(topic)
		self.subscribed=False

	def GET(*uri,**params):
		pass

	def PUT(*uri,**params):
		pass

	def POST(*uri,**params):
		return "online"

	def DELETE(*uri,**params):
		pass

if __name__ == "__main__":
	conf = { '/': { 'request.dispatch': cherrypy.dispatch.MethodDispatcher(), 'tools.sessions.on': True } }
	# building the web service
	server=ChannelRESTMQTT("telegram_hospital")
	cherrypy.tree.mount(server, '/', conf)
	cherrypy.config.update({"server.socket_host": t.getAddress(), "server.socket_port": 8085})
	cherrypy.engine.start()

	server.start()
	server.mySubscribe()

	while True and t.getFlag()==False:
		t.configure()
		time.sleep(10)

	server.myUnsubscribe()
	server.stop()
	cherrypy.engine.block()

