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
    def __init__(self, clientID):
        self.clientID = clientID
        self.topic = t.getTopicPublisher()
        self.broker = "127.0.0.1"
        self.status=''

        self._paho_mqtt = PahoMQTT.Client(clientID, False)
        self._paho_mqtt.on_connect = self.myOnConnect
        self._paho_mqtt.on_message = self.myOnMessageReceived
        self.subscribed=False
        self.message={}
        
    def start (self):
        self._paho_mqtt.connect(self.broker, 1883)
        self._paho_mqtt.loop_start()

    def stop (self):
        self._paho_mqtt.loop_stop()
        self._paho_mqtt.disconnect()

    def mySubscribe(self):
        if(self.subscribed==False):
            try:
                topic=t.getTopicsSubscriber()["statistic_server"]
                self._paho_mqtt.subscribe(topic, 2)
                self.subscribed=True
            except:
                print("The server you want to subscribe is not still online")

    def myUnsubscribe(self):
        topic=t.getTopicsSubscriber()["statistic_server"]
        self._paho_mqtt.unsubscribe(topic)
        self.subscribed=False

    def myOnConnect (self, paho_mqtt, userdata, flags, rc):
        print ("Connected to %s with result code: %d" % (self.messageBroker, rc))

    def myOnMessageReceived (self, paho_mqtt , userdata, msg):
        message=json.loads(msg.payload)
        

    def myPublish(self):
        self.message=json.loads(t.readyData())
        self._paho_mqtt.publish(self.topic, json.dumps(self.message), 2)
        

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
    server=TriageRESTMQTT("telegram_triage")
    cherrypy.tree.mount(server, '/', conf)
    cherrypy.config.update({"server.socket_host": socket.gethostbyname(socket.gethostname()), "server.socket_port": 8086})
    cherrypy.engine.start()
    i=0
    server.start()
    

    while True:
        server.mySubscribe()
        t.configure()
        while(t.isReadyToSend()):
            server.myPublish()
        time.sleep(2)
    server.myUnsubscribe()
    server.stop()
    cherrypy.engine.block()
