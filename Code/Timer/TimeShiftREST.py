import cherrypy
import json
import time
from TimeShift import TimeShift
import socket

t=TimeShift()

class TimeShiftREST(object):
	exposed=True
	
	def GET(*uri,**params):
		pass
	
	'''DATA TO ADD TO SCHEDULING'''
	def PUT(*uri,**params):
		body=cherrypy.request.body.read()
		try:
			json_body=json.loads(body.decode('utf-8'))

		except:
			raise cherrypy.HTTPError(400,"ERROR body is empty")
		
		t.addToScheduling(json.dumps(json_body))

	'''DATA REQUESTED BY CATALOG'''
	
	def POST(*uri,**params):
		body=cherrypy.request.body.read()
		try:
			json_body=json.loads(body.decode('utf-8'))

		except:
			raise cherrypy.HTTPError(400,"ERROR body is empty")
		parameter=list(json_body.values())
		keys=list(json_body.keys())

		t.setData(json_body)
		print(json_body)
		return json.dumps(t.getData())
		
	def DELETE(*uri,**params):
		pass
		

if __name__=='__main__':
	conf = { '/': { 'request.dispatch': cherrypy.dispatch.MethodDispatcher(), 'tools.sessions.on': True } }
	# building the web service
	cherrypy.tree.mount(TimeShiftREST(), '/', conf)
	cherrypy.config.update({"server.socket_host": t.getAddress(), "server.socket_port": 8087})
	cherrypy.engine.start()
	
	t.configure()
	while True:
		t.sendAlert()
		time.sleep(5)
		

	cherrypy.engine.block()
