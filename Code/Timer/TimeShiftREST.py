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
		
	def PUT(*uri,**params):
		body=cherrypy.request.body.read()
		try:
			json_body=json.loads(body.decode('utf-8'))

		except:
			raise cherrypy.HTTPError(400,"ERROR body is empty")
		
		parameter=list(json_body.values())
		keys=list(json_body.keys())
		
		t.addToScheduling(json.dumps(json_body))
	def POST(*uri,**params):
		pass
		
	def DELETE(*uri,**params):
		pass
		

if __name__=='__main__':
	conf = { '/': { 'request.dispatch': cherrypy.dispatch.MethodDispatcher(), 'tools.sessions.on': True } }
	# building the web service
	cherrypy.tree.mount(TimeShiftREST(), '/', conf)
	cherrypy.config.update({"server.socket_host": socket.gethostbyname(socket.gethostname()), "server.socket_port": 8087})
	cherrypy.engine.start()
	
	while True:
		t.configure()
		t.sendAlert()
		time.sleep(2)
		

	cherrypy.engine.block()
