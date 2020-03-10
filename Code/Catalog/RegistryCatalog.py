import mysql.connector
from mysql.connector import errorcode
import json
import time
import requests
import socket

class RegistryCatalog(object):
	def __init__(self):

		#Initialization of the own address
		s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		s.connect(('8.8.8.8',80))
		self.address=s.getsockname()[0]

		#Creation of the database of the Catalog
		try:
			self.conn=mysql.connector.connect(user='root',password='',host='127.0.0.1',database='catalogdatabase')
			self.cursor=self.conn.cursor()
			query="DROP TABLE IF EXISTS `databases`;\
					\
					CREATE TABLE `databases` (\
					  `table` varchar(50) NOT NULL DEFAULT '',\
					  `attribute` varchar(50) NOT NULL DEFAULT ''\
					   PRIMARY KEY (`table`,`attribute`)\
					) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;\
					\
					DROP TABLE IF EXISTS `mappings`; \
					\
					CREATE TABLE `mappings` (\
					  `server` varchar(50) NOT NULL DEFAULT '',\
					  `ip` varchar(50) DEFAULT NULL,\
					  `port` varchar(50) DEFAULT NULL,\
					  PRIMARY KEY (`server`)\
					) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;\
					\
					DROP TABLE IF EXISTS `mqtt`;\
					\
					CREATE TABLE `mqtt` (\
					  `publisher` varchar(50) NOT NULL,\
					  `subscriber` varchar(50) DEFAULT '',\
					  `topic` varchar(50) NOT NULL DEFAULT ''\
					) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;\
					\
					DROP TABLE IF EXISTS `sensors`;\
					\
					CREATE TABLE `sensors` (\
					  `type` varchar(50) NOT NULL DEFAULT '',\
					  `id` int(11) NOT NULL,\
					  `available` int(1) NOT NULL\
					) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;\
					\
					LOCK TABLES `sensors` WRITE;\
					/*!40000 ALTER TABLE `sensors` DISABLE KEYS */;\
					\
					INSERT INTO `sensors` (`type`, `id`, `available`)\
					VALUES\
						('pressure',1,1),\
						('pressure',2,1),\
						('pressure',3,1),\
						('pressure',4,1),\
						('pressure',5,1),\
						('pressure',6,1),\
						('pressure',7,1),\
						('pressure',8,1),\
						('pressure',9,1),\
						('pressure',10,1),\
						('heart',1,1),\
						('heart',2,1),\
						('heart',3,1),\
						('heart',4,1),\
						('heart',5,1),\
						('heart',6,1),\
						('heart',7,1),\
						('heart',8,1),\
						('heart',9,1),\
						('heart',10,1),\
						('glucose',1,1),\
						('glucose',2,1),\
						('glucose',3,1),\
						('glucose',4,1),\
						('glucose',5,1),\
						('glucose',6,1),\
						('glucose',7,1),\
						('glucose',8,1),\
						('glucose',9,1),\
						('glucose',10,1);\
						\
					/*!40000 ALTER TABLE `sensors` ENABLE KEYS */;\
					UNLOCK TABLES;\
					DROP TABLE IF EXISTS `telegram`;\
					\
					CREATE TABLE `telegram` (\
					  `chat` varchar(50) DEFAULT NULL,\
					  `id` varchar(60) NOT NULL,\
					  `token` varchar(60) DEFAULT NULL,\
					  PRIMARY KEY (`id`)\
					) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;\
					\
					DROP TABLE IF EXISTS `thresholds`;\
					\
					CREATE TABLE `thresholds` (\
					  `person` varchar(50) NOT NULL DEFAULT '',\
					  `minMinPres` int(11) DEFAULT NULL,\
					  `maxMinPres` int(11) DEFAULT NULL,\
					  `minAvgPres` int(11) DEFAULT NULL,\
					  `maxAvgPres` int(11) DEFAULT NULL,\
					  `minMaxPres` int(11) DEFAULT NULL,\
					  `maxMaxPres` int(11) DEFAULT NULL,\
					  `minGluc` int(11) DEFAULT NULL,\
					  `maxGluc` int(11) DEFAULT NULL,\
					  PRIMARY KEY (`person`)\
					) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;\
					\
					LOCK TABLES `thresholds` WRITE;\
					/*!40000 ALTER TABLE `thresholds` DISABLE KEYS */;\
					\
					INSERT INTO `thresholds` (`person`, `minMinPres`, `maxMinPres`, `minAvgPres`, `maxAvgPres`, `minMaxPres`, `maxMaxPres`, `minGluc`, `maxGluc`)\
					VALUES\
						('OVER65',83,121,86,134,91,147,60,130),\
						('UNDER25',73,105,79,120,84,133,60,130),\
						('UNDER45',77,110,82,123,87,137,60,130),\
						('UNDER55',80,115,84,128,89,142,60,130),\
						('UNDER65',82,118,86,132,91,142,60,130);\
						\
					/*!40000 ALTER TABLE `thresholds` ENABLE KEYS */;\
					UNLOCK TABLES;"
			self.cursor.execute(query, multi=True)
					
		except mysql.connector.Error as err:
			if err.errno==errorcode.ER_ACCESS_DENIED_ERROR:
				print("Something gone wrong with the credentials")
			elif err.errno==errorcode.ER_BAD_DB_ERROR:
				print("Database does not exist")
			else:
				print(err)
			

		'''
		config={
		'user':'root',
		'password':'root',
		'host':'127.0.0.1'
		'database':'PatientsData'
		'raise_on_warnings':True
		}

		self.conn=mysql.connector.connect(**config)
		'''
		
	def getAddress(self):
		return self.address

	'''DATA MANIPULATION'''

	def readThresholds(self):
		query=("SELECT * FROM thresholds")
		self.cursor.execute(query)
		result=self.cursor.fetchall()
		thresh={}

		for row in result:
			thresh[row[0]]=[row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]]
		return json.dumps(thresh)


		
	def readTopics(self,subscriber):
		query="SELECT publisher,topic FROM mqtt WHERE subscriber=%(subscriber)s"
		self.cursor.execute(query,{"subscriber":subscriber})
		result=self.cursor.fetchall()
		mqtt={}

		for row in result:
			mqtt[row[0]]=row[1]
		return json.dumps(mqtt)

	def readMappings(self,server):
		query="SELECT server,ip,port FROM mappings WHERE server<>%(server)s"
		self.cursor.execute(query,{"server":server})
		
		result=self.cursor.fetchall()

		ips={}
		for row in result:
			ips[row[0]]=[row[1],row[2]]
			
		return json.dumps(ips)
	def readTables(self):
		query="SELECT `table`,`attribute` FROM `databases`"
		self.cursor.execute(query)
		result=self.cursor.fetchall()
		tables={}
		for row in result:
			if(row[0]!=""):
				tables[row[0]]=[]
		for row in result:
			if(row[0]!=""):
				tables[row[0]].append(row[1])

		return json.dumps(tables)

	def readAvailableSensors(self):
		query="SELECT type,id FROM sensors WHERE available=1"
		self.cursor.execute(query)
		result=self.cursor.fetchall()
		sensors={}
		for row in result:
			if(row[0]!=""):
				sensors[row[0]]=[]
		for row in result:
			if(row[0]!=""):
				sensors[row[0]].append(row[1])
		return json.dumps(sensors)

	def closeconn(self):
		self.cursor.close()
		self.conn.close()

	'''DATA UPDATE/INSERT'''

	def insertIP(self,server,ip,port):
		query="INSERT INTO mappings (server,ip,port) VALUES (%s,%s,%s) ON DUPLICATE KEY UPDATE ip=%s"
		values=(server,ip,port,ip)
		self.cursor.execute(query,values)
		
	def insertTopic(self, data, publisher):
		query="INSERT INTO mqtt (publisher,subscriber,topic) VALUES (%s,%s,%s) ON DUPLICATE KEY UPDATE publisher=%s,subscriber=%s,topic=%s"
		for i in range(len(data["topic"])):
			subscriber=data["subscriber"][i]
			topic=data["topic"][i]
			self.cursor.execute(query,(publisher,subscriber,topic,publisher,subscriber,topic))
	def insertTable(self, data):
		for table in data:
			for i in range(len(data[table])):
				query="INSERT INTO `databases` (`table`,`attribute`) VALUES (%s,%s) ON DUPLICATE KEY UPDATE `table`=%s,`attribute`=%s"
				self.cursor.execute(query,(table,data[table][i],table,data[table][i]))

	def insertInfoChat(self,chat,id_chat,token):
		query="INSERT INTO telegram (chat,id,token) VALUES (%s,%s,%s) ON DUPLICATE KEY UPDATE chat=%s,id=%s,token=%s"
		self.cursor.execute(query,(chat,id_chat,token,chat,id_chat,token))

	def removeIP(self,server):
		query="DELETE FROM mappings WHERE server=%(server)s"
		self.cursor.execute(query,{"server":server})

	def onlineServers(self):
		query="SELECT server,ip,port FROM mappings"
		try:
			self.cursor.execute(query)
			result=self.cursor.fetchall()
			for row in result:
				key=row[0]

				try:
					if key=="queue_server":
						mqtt_topics=self.readTopics(key)
						ips=self.readMappings(key)
						thresh=self.readThresholds()
						tables=self.readTables()
						return_list=[json.loads(mqtt_topics),json.loads(ips),json.loads(thresh),json.loads(tables)]
						data=json.dumps(return_list)
						
					elif key=="db_server":
						ips=self.readMappings(key)
						data=ips

					elif key=="statistic_server":
						ips=self.readMappings(key)
						data=ips
					elif key=="ihealth_adapter":
						ips=self.readMappings(key)
						data=json.dumps(json.loads(ips))

					elif key=="telegram_hospital":
						mqtt_topics=self.readTopics(key)
						ips=self.readMappings(key)
						return_list=[json.loads(mqtt_topics),json.loads(ips)]
						data=json.dumps(return_list)

					elif key=="telegram_triage":
						ips=self.readMappings(key)
						available_sensors=self.readAvailableSensors()
						return_list=[json.loads(ips),json.loads(available_sensors)]
						data=json.dumps(return_list)

					elif key=="time_shift":
						ips=self.readMappings(key)
						data=ips

					'''ASKING DATA TO THE SERVERS'''
					r=requests.post("http://"+row[1]+":"+row[2],data)
					json_body=r.json()
					
					
					for key in json_body.keys():
						if key=="queue_server":
							self.insertIP(key,json_body[key]["ip"],json_body[key]["port"])
							self.insertTopic(json_body[key],key)
								
						elif key=="db_server":
							self.insertIP(key,json_body[key]["ip"],json_body[key]["port"])
							self.insertTable(json_body[key]["tables"])

						elif key=="statistic_server":
							self.insertIP(key,json_body[key]["ip"],json_body[key]["port"])
							
						elif key=="ihealth_adapter":
							self.insertIP(key,json_body[key]["ip"],json_body[key]["port"])

						elif key=="telegram_hospital":
							self.insertIP(key,json_body[key]["ip"],json_body[key]["port"])
							self.insertInfoChat(key,json_body[key]["chatId"],json_body[key]["token"])

						elif key=="telegram_triage":
							self.insertIP(key,json_body[key]["ip"],json_body[key]["port"])
							self.insertInfoChat(key,json_body[key]["chatId"],json_body[key]["token"])
							self.insertTopic(json_body[key],key)
							
						elif key=="time_shift":
							self.insertIP(key,json_body[key]["ip"],json_body[key]["port"])

						else:
							raise cherrypy.HTTPError(400,"Invalid key")
					
				except:
					self.removeIP(row[0])
					print("Server "+row[0]+" not online at "+row[1]+":"+row[2]+" anymore")
		except:
			print("No servers online at this moment")
	
	'''SENSORS AVAILABILITY'''

	def updateSensors(self,sensors):#sensors occupied
		query="UPDATE sensors SET available=0 WHERE type=%s AND id=%s"
		self.cursor.execute(query,('pressure',sensors["pressure"]))
		self.cursor.execute(query,('glucose',sensors["glucose"]))
		self.cursor.execute(query,('heart',sensors["heart"]))

		print(json.loads(self.readAvailableSensors()))

	def releaseSensors(self,pressure_id,heart_id,glucose_id):#free sensors
		query="UPDATE sensors SET available=1 WHERE type=%s AND id=%s"
		self.cursor.execute(query,('pressure',pressure_id))
		self.cursor.execute(query,('glucose',glucose_id))
		self.cursor.execute(query,('heart',heart_id))

		print(json.loads(self.readAvailableSensors()))
		
		