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
		
		
		pressure_id=json_body["pressure"]
		heart_id=json_body["heart"]
		glucose_id=json_body["glucose"]

		data=json.loads(i.getDataFromCloud(pressure_id,heart_id,glucose_id))
		print(data)
		i.sendDataQueue(data)

	def POST(*uri,**params):
		body=cherrypy.request.body.read()
		try:
			json_body=json.loads(body.decode('utf-8'))

		except:
			raise cherrypy.HTTPError(400,"ERROR body is empty")
		parameter=list(json_body.values())
		keys=list(json_body.keys())

		i.setData(json_body)
		print(json_body)
		return json.dumps(i.getData())

	def DELETE(*uri,**params):
		pass

if __name__=='__main__':
	conf = { '/': { 'request.dispatch': cherrypy.dispatch.MethodDispatcher(), 'tools.sessions.on': True } }
	# building the web service
	cherrypy.tree.mount(iHealthAdapterREST(), '/', conf)
	cherrypy.config.update({"server.socket_host": i.getAddress(), "server.socket_port": 8084})
	cherrypy.engine.start()
	i.configure()
	while True:
		
	

	cherrypy.engine.block()