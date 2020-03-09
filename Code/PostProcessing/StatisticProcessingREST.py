import cherrypy
import requests
import json
import time
import socket
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

	
		


if __name__=='__main__':
	conf = { '/': { 'request.dispatch': cherrypy.dispatch.MethodDispatcher(), 'tools.sessions.on': True } }
	# building the web service
	cherrypy.tree.mount(StatisticProcessingRESTMQTT(), '/', conf)
	cherrypy.config.update({"server.socket_host": s.getAddress(), "server.socket_port": 8083})
	cherrypy.engine.start()

	s.configure()

	while True:
		time.sleep(2)
		s.processData()
		
	cherrypy.engine.block()