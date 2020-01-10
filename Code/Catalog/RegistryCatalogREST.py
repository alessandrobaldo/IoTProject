import cherrypy
import json
import time
from RegistryCatalog import RegistryCatalog
import socket


r=RegistryCatalog()

class RegistryCatalogREST(object):
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
		
		r.updateSensors(json_body)

	def POST(*uri,**params):
		#Managing the configuration
		
		body=cherrypy.request.body.read()
		try:
			json_body=json.loads(body.decode('utf-8'))

		except:
			raise cherrypy.HTTPError(400,"ERROR body is empty")
		
		parameter=list(json_body.values())
		keys=list(json_body.keys())
		
		
		
		for key in keys:
			if key=="queue_server":
				r.insertIP("queue_server",json_body["queue_server"]["ip"],json_body["queue_server"]["port"])
				r.insertTopic(json_body["queue_server"],"queue_server")
				mqtt_topics=r.readTopics("queue_server")
				ips=r.readMappings("queue_server")
				thresh=r.readThresholds()
				tables=r.readTables()
				return_list=[json.loads(mqtt_topics),json.loads(ips),json.loads(thresh),json.loads(tables)]
				return json.dumps(return_list)
				
			elif key=="db_server":
				r.insertIP("db_server",json_body["db_server"]["ip"],json_body["db_server"]["port"])
				r.insertTable(json_body["db_server"]["tables"])
				ips=r.readMappings("db_server")
				return ips

			elif key=="statistic_server":
				r.insertIP("statistic_server",json_body["statistic_server"]["ip"],json_body["statistic_server"]["port"])
				r.insertTopic(json_body["statistic_server"],"statistic_server")
				mqtt_topics=r.readTopics("statistic_server")
				ips=r.readMappings("statistic_server")

				return_list=[json.loads(mqtt_topics),json.loads(ips)]
				return json.dumps(return_list)

			elif key=="ihealth_adapter":
				r.insertIP("ihealth_adapter",json_body["ihealth_adapter"]["ip"],json_body["ihealth_adapter"]["port"])
				ips=r.readMappings("ihealth_adapter")
				return json.dumps(json.loads(ips))

			elif key=="telegram_hospital":
				r.insertIP("telegram_hospital",json_body["telegram_hospital"]["ip"],json_body["telegram_hospital"]["port"])
				r.insertInfoChat("telegram_hospital",json_body["telegram_hospital"]["chatId"],json_body["telegram_hospital"]["token"])
				ips=r.readMappings("telegram_hospital")
				mqtt_topics=r.readTopics("telegram_hospital")
				print("AAAAAA")
				return_list=[json.loads(mqtt_topics),json.loads(ips)]
				return json.dumps(return_list)

			elif key=="telegram_triage":
				r.insertInfoChat("telegram_triage",json_body["telegram_triage"]["chatId"],json_body["telegram_triage"]["token"])
				r.insertTopic(json_body["telegram_triage"],"telegram_triage")
				ips=r.readMappings("telegram_triage")
				mqtt_topics=r.readTopics("telegram_triage")
				available_sensors=r.readAvailableSensors()

				return_list=[json.loads(mqtt_topics),json.loads(ips),json.loads(available_sensors)]
				return json.dumps(return_list)

			elif key=="time_shift":
				r.insertIP("time_shift",json_body["time_shift"]["ip"],json_body["time_shift"]["port"])
				ips=r.readMappings("time_shift")
				return json.dumps(json.loads(ips))

			else:
				raise cherrypy.HTTPError(400,"Invalid key")
				

	



	def DELETE(*uri,**params):
		body=cherrypy.request.body.read()
		try:
			json_body=json.loads(body.decode('utf-8'))

		except:
			raise cherrypy.HTTPError(400,"ERROR body is empty")
		
		parameter=list(json_body.values())
		keys=list(json_body.keys())

		r.releaseSensors(json_body)


if __name__=='__main__':
	conf = { '/': { 'request.dispatch': cherrypy.dispatch.MethodDispatcher(), 'tools.sessions.on': True } }
	# building the web service
	cherrypy.tree.mount(RegistryCatalogREST(), '/', conf)
	cherrypy.config.update({"server.socket_host": socket.gethostbyname(socket.gethostname()), "server.socket_port": 8080})
	cherrypy.engine.start()
	while True:
		r.onlineServers()
		time.sleep(5)

	cherrypy.engine.block()


	