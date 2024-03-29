import paho.mqtt.client as PahoMQTT
import time
import json
import socket
import cherrypy
from TelegramHospitalChannel import TelegramHospitalChannel

t=TelegramHospitalChannel()

class ChannelRESTMQTT(object):
	exposed=True

	def __init__(self, clientID):
		self.clientID = clientID
		self.broker="192.168.1.103"

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

	'''RECEIVING MESSAGE TO PUBLISH IN THE CHANNEL'''
	def myOnMessageReceived (self, paho_mqtt , userdata, msg):
	
		message=json.loads(msg.payload)
		sending=""
		for key in list(message.keys()):
			sending+="\n**ID**:"+str(key)
			sending+="\n\t\tCode:"+str(message[key]["code"])+"\tArrival:"+str(message[key]["time_stamp"])
			sending+="\n\t\tPres.:"+str(message[key]["pressure_max"])+"-"+str(message[key]["pressure_min"])
			sending+="\tHR:"+str(message[key]["rate"])+"\tGluc.:"+str(message[key]["glucose"])
			sending+="\n-----------------------------------------"
		
		t.send_message(sending)

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

#DATA REQUESTED BY CATALOG
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
	server=ChannelRESTMQTT("telegram_hospital")
	cherrypy.tree.mount(server, '/', conf)
	cherrypy.config.update({"server.socket_host": t.getAddress(), "server.socket_port": 8085})
	cherrypy.engine.start()

	server.start()
	t.configure()
	while True:
		server.mySubscribe()
		time.sleep(10)

	server.myUnsubscribe()
	server.stop()
	cherrypy.engine.block()

