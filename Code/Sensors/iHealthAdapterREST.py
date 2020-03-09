import cherrypy
import json
import time
from iHealthAdapter import iHealthAdapter
import socket

i=iHealthAdapter()

class iHealthAdapterREST(object):
	
	#Receiving request from queue server to send data about sensors with id1,id2,id3

	def GET(*uri,**params):

		if(len(uri)!=0):
			try:
				print(uri)
				pressure_id=uri[1]
				heart_id=uri[2]
				glucose_id=uri[3]
				print(pressure_id)
				print(heart_id)
				print(glucose_id)

			except:
				print("WEEEE")
				raise cherrypy.HTTPError(400,"Invalid parameters")

			data=json.loads(i.getDataFromCloud(pressure_id,heart_id,glucose_id))
			print(data)
			return json.dumps(data)
		else:
			raise cherrypy.HTTPError(400,"Invalid parameters")


	def PUT(*uri,**params):
		pass

	'''DATA REQUESTED BY CATALOG'''
	def POST(*uri,**params):
		body=cherrypy.request.body.read()
		try:
			json_body=json.loads(body.decode('utf-8'))

		except:
			raise cherrypy.HTTPError(400,"ERROR body is empty")
		parameter=list(json_body.values())
		keys=list(json_body.keys())

		i.setData(json_body)
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
		time.sleep(1)
		
	

	cherrypy.engine.block()