import cherrypy
import json
import time
from iHealthAdapter import iHealthAdapter
import socket

i=iHealthAdapter()

class iHealthAdapterREST(object):
	exposed=True
	
	def GET(*uri,**params):
		pass

	def PUT(*uri,**params):
		#Receiving request from queue server to send data about sensors with id1,id2,id3
		body=cherrypy.request.body.read()
		try:
			json_body=json.loads(body.decode('utf-8'))

		except:
			raise cherrypy.HTTPError(400,"ERROR body is empty")
		
		parameter=list(json_body.values())
		keys=list(json_body.keys())
		
		pressure_id=json_body["pressure"]
		heart_id=json_body["heart"]
		glucose_id=json_body["glucose"]

		data=json.loads(i.getDataFromCloud(pressure_id,heart_id,glucose_id))
		print(data)
		i.sendDataQueue(data)

	def POST(*uri,**params):
		return "online"

	def DELETE(*uri,**params):
		pass

if __name__=='__main__':
	conf = { '/': { 'request.dispatch': cherrypy.dispatch.MethodDispatcher(), 'tools.sessions.on': True } }
	# building the web service
	cherrypy.tree.mount(iHealthAdapterREST(), '/', conf)
	cherrypy.config.update({"server.socket_host": socket.gethostbyname(socket.gethostname()), "server.socket_port": 8084})
	cherrypy.engine.start()
	while True:
		i.configure()
		time.sleep(10)
	

	cherrypy.engine.block()