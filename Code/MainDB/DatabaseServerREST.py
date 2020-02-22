import cherrypy
import json
import time
from DatabaseServer import DatabaseServer
import socket

d=DatabaseServer()

class DatabaseServerREST(object):
	exposed=True
	
	'''RETRIEVING DATA FOR THE PROCESSINGS'''
	def GET(*uri,**params):
		
		if(uri[1]=="process"):
			return d.readDataQueue()
		elif(uri[1]=="statistics"):
			return d.readStatistics()

	'''Receiving data from QueueProcessing to insert them'''

	def PUT(*uri,**params):
		body=cherrypy.request.body.read()
		try:
			json_body=json.loads(body.decode('utf-8'))
		except:
			raise cherrypy.HTTPError(400,"ERROR body is empty")

		if(uri[1]=="sensors"):
			print("SENSORS")
			d.insertDataSensors(json_body)
		elif(uri[1]=="patients"):
			d.insertDataTelegram(json_body)
			print("PATIENT")

	'''DATA REQUESTED BY THE REGISTRY CATALOG'''

	def POST(*uri,**params):
		body=cherrypy.request.body.read()
		try:
			json_body=json.loads(body.decode('utf-8'))
		except:
			raise cherrypy.HTTPError(400,"ERROR body is empty")
		d.setData(json_body)
		return json.dumps(d.getData())

	'''PATIENT PROCESSED'''
	def DELETE(*uri,**params):
		if(len(uri)!=0):
			d.removePatient(uri[1])

if __name__=='__main__':
	conf = { '/': { 'request.dispatch': cherrypy.dispatch.MethodDispatcher(), 'tools.sessions.on': True } }
	# building the web service
	cherrypy.tree.mount(DatabaseServerREST(), '/', conf)
	cherrypy.config.update({"server.socket_host": d.getAddress(), "server.socket_port": 8081})
	cherrypy.engine.start()
	d.configure()
	while True:
		time.sleep(1)

	cherrypy.engine.block()
