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

	'''TELEGRAM RESPONSE'''
	def PUT(*uri,**params):
		body=cherrypy.request.body.read()
		try:
			json_body=json.loads(body.decode('utf-8'))
		except:
			raise cherrypy.HTTPError(400,"ERROR body is empty")
		parameter=list(json_body.values())
		keys=list(json_body.keys())
		
		r.updateSensors(json_body)

		return r.readAvailableSensors()

	'''RESPONE TO THE INITIALIZATION OF ALL THE SERVERS'''
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
				r.insertIP(key,json_body[key]["ip"],json_body[key]["port"])
				r.insertTopic(json_body[key],key)
				mqtt_topics=r.readTopics(key)
				ips=r.readMappings(key)
				thresh=r.readThresholds()
				tables=r.readTables()
				return_list=[json.loads(mqtt_topics),json.loads(ips),json.loads(thresh),json.loads(tables)]
				return json.dumps(return_list)
				
			elif key=="db_server":
				r.insertIP(key,json_body[key]["ip"],json_body[key]["port"])
				r.insertTable(json_body[key]["tables"])
				ips=r.readMappings(key)
				return ips

			elif key=="statistic_server":
				r.insertIP(key,json_body[key]["ip"],json_body[key]["port"])
				ips=r.readMappings(key)
				return ips

			elif key=="ihealth_adapter":
				r.insertIP(key,json_body[key]["ip"],json_body[key]["port"])
				ips=r.readMappings(key)
				return ips

			elif key=="telegram_hospital":
				r.insertIP(key,json_body[key]["ip"],json_body[key]["port"])
				r.insertInfoChat(key,json_body[key]["chatId"],json_body[key]["token"])
				ips=r.readMappings(key)
				mqtt_topics=r.readTopics(key)

				return_list=[json.loads(mqtt_topics),json.loads(ips)]
				return json.dumps(return_list)

			elif key=="telegram_triage":
				r.insertIP(key,json_body[key]["ip"],json_body[key]["port"])
				r.insertInfoChat(key,json_body[key]["chatId"],json_body[key]["token"])
				r.insertTopic(json_body[key],key)
				ips=r.readMappings(key)
				available_sensors=r.readAvailableSensors()

				return_list=[json.loads(ips),json.loads(available_sensors)]
				return json.dumps(return_list)

			elif key=="time_shift":
				r.insertIP(key,json_body[key]["ip"],json_body[key]["port"])
				ips=r.readMappings(key)
				return json.dumps(json.loads(ips))

			else:
				raise cherrypy.HTTPError(400,"Invalid key")
				

	


	'''TELEGRAM SENSORS RELEASE'''
	def DELETE(*uri,**params):
		if(len(uri)!=0):
			try:
				pressure_id=uri[1]
				heart_id=uri[2]
				glucose_id=uri[3]
			except:
				raise cherrypy.HTTPError(400,"Invalid parameters passed")
		else:
			raise cherrypy.HTTPError(400,"Invalid parameters passed")

		r.releaseSensors(pressure_id,heart_id,glucose_id)




if __name__=='__main__':
	conf = { '/': { 'request.dispatch': cherrypy.dispatch.MethodDispatcher(), 'tools.sessions.on': True } }
	# building the web service
	cherrypy.tree.mount(RegistryCatalogREST(), '/', conf)
	cherrypy.config.update({"server.socket_host": r.getAddress(), "server.socket_port": 8080})
	cherrypy.engine.start()
	while True:
		r.onlineServers()
		time.sleep(1)

	cherrypy.engine.block()


	