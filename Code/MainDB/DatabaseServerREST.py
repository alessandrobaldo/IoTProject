import cherrypy
import json
import time
from DatabaseServer import DatabaseServer
import socket

d=DatabaseServer()

class DatabaseServerREST(object):
	exposed=True
	
	def GET(*uri,**params):
		
		if(uri[1]=="process"):
			print(json.loads(d.readDataQueue()))
			return d.readDataQueue()
		elif(uri[1]=="statistics"):
			return d.readStatistics()
	#Receiving data from QueueProcessing to insert them
	def PUT(*uri,**params):

		body=cherrypy.request.body.read()
		try:
			json_body=json.loads(body.decode('utf-8'))

		except:
			raise cherrypy.HTTPError(400,"ERROR body is empty")
		parameter=list(json_body.values())
		keys=list(json_body.keys())
		if(uri[1]=="sensors"):
			print("SENSORS")
			d.insertDataSensors(json_body)
		elif(uri[1]=="patients"):
			d.insertDataTelegram(json_body)
			print("PATIENT")

	def POST(*uri,**params):
		json_obj={"db_server":"online"}
		return json.dumps(json_obj)

	def DELETE(*uri,**params):
		body=cherrypy.request.body.read()
		try:
			json_body=json.loads(body.decode('utf-8'))
		except:
			raise cherrypy.HTTPError(400,"ERROR body is empty")
		parameter=list(json_body.values())
		keys=list(json_body.keys())
		d.removePatient(self,json_body["key"])

if __name__=='__main__':
	conf = { '/': { 'request.dispatch': cherrypy.dispatch.MethodDispatcher(), 'tools.sessions.on': True } }
	# building the web service
	cherrypy.tree.mount(DatabaseServerREST(), '/', conf)
	cherrypy.config.update({"server.socket_host": d.getAddress(), "server.socket_port": 8081})
	cherrypy.engine.start()
	
	while True:
		d.configure()
		time.sleep(10)

	cherrypy.engine.block()
