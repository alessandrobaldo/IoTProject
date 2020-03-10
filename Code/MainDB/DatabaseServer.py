import mysql.connector
from mysql.connector import errorcode
import json
import datetime
import socket
import requests

class DatabaseServer(object):
	def __init__(self):
		s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		s.connect(('8.8.8.8',80))
		self.address=s.getsockname()[0]
		#self.catalog="http://192.168.1.103:8080"
		self.catalog=json.loads(open("catalog.json").read())["catalog"]
		
		
		'''self.my_data={
			"db_server":
				{	
				"ip":socket.gethostbyname(socket.gethostname()),
				"port":8081,
				"tables":{
					"data_sensors":[],
					"info_patients":[]
					}
				}
		}'''

		self.my_data=json.loads(open("dbData.json").read())
		self.my_data["db_server"]["ip"]=self.address
		
		'''CREATION OF THE DATABASE'''
		try:
			self.conn=mysql.connector.connect(user='root',password='',host='127.0.0.1',database='PatientsData')
			self.cursor=self.conn.cursor(buffered=True)
			query="DROP TABLE IF EXISTS `data_sensors`;\
					CREATE TABLE `data_sensors` (\
					  `pressure_id` varchar(50) NOT NULL DEFAULT '',\
					  `heart_id` varchar(50) NOT NULL,\
					  `glucose_id` varchar(50) NOT NULL DEFAULT '',\
					  `pressure_min` int(11) DEFAULT NULL,\
					  `pressure_max` int(11) DEFAULT NULL,\
					  `rate` int(11) DEFAULT NULL,\
					  `glucose` int(11) DEFAULT NULL,\
					  `time_stamp` timestamp NULL DEFAULT NULL\
					) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"

			query2="DROP TABLE IF EXISTS `info_patients`;\
					CREATE TABLE `info_patients` (\
					  `id_patient` varchar(50) NOT NULL DEFAULT,\
					  `pressure_id` varchar(50) NOT NULL DEFAULT,\
					  `heart_id` varchar(50) NOT NULL DEFAULT '',\
					  `glucose_id` varchar(50) NOT NULL DEFAULT '',\
					  `name` varchar(50) DEFAULT NULL,\
					  `surname` varchar(50) DEFAULT NULL,\
					  `age` varchar(50) DEFAULT NULL,\
					  `height` varchar(11) DEFAULT NULL,\
					  `weight` varchar(11) DEFAULT NULL,\
					  `gender` varchar(50) DEFAULT NULL,\
					  `code` int(11) DEFAULT NULL,\
					  `unit` varchar(50) DEFAULT NULL,\
					  `time_stamp` timestamp NULL DEFAULT NULL\
					  `processed` int(1) DEFAULT NULL,\
  					  `analysed` int(1) DEFAULT NULL\
					) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
			self.cursor.execute(query,multi=True)
			self.cursor.execute(query2,multi=True)
		except mysql.connector.Error as err:
			if err.errno==errorcode.ER_ACCESS_DENIED_ERROR:
				print("Something gone wrong with the credentials")
			elif err.errno==errorcode.ER_BAD_DB_ERROR:
				print("Database does not exist")
			else:
				print(err)
		for table in self.my_data["db_server"]["tables"]:
			query="SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=%(table)s"
			self.cursor.execute(query,{"table":table})
			result=self.cursor.fetchall()

			for row in result:
				for i in range(len(row)):
					self.my_data["db_server"]["tables"][table].append(row[i])

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

	def getData(self):
		return self.my_data

	def setData(self,data):
		self.ip_others=data

	def configure(self):
		self.result=requests.post(self.catalog,json.dumps(self.my_data))
		self.ip_others=self.result.json()

	def getIps(self):
		return self.ip_others

	def insertDataSensors(self,data):
		
		add_sensors_data=("INSERT INTO data_sensors (pressure_id,heart_id,glucose_id,pressure_min,pressure_max,rate,glucose,time_stamp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)")
		data_patient=(data["pressure_id"],data["heart_id"],data["glucose_id"],data["pressure_min"],data["pressure_max"],data["rate"],data["glucose"],data["time_stamp"])
		self.cursor.execute(add_sensors_data,data_patient)
		self.conn.commit()
		

	def insertDataTelegram(self,data):
		
		add_patients_data=("INSERT INTO info_patients (id_patient,pressure_id,heart_id,glucose_id,name,surname,age,height,weight,gender,code,unit,time_stamp, processed,analysed) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
		patient_registry=(data["id_patient"],data["pressure_id"],data["heart_id"],data["glucose_id"],data["name"],data["surname"],data["age"],data["height"],data["weight"],data["gender"],data["code"],data["unit"],data["time_stamp"],0,0)
		self.cursor.execute(add_patients_data,patient_registry)
		self.conn.commit()

	def removePatient(self, key):
		query="SELECT pressure_id,heart_id,glucose_id FROM info_patients WHERE id_patient=%(key)s"
		self.cursor.execute(query,{"key":key})
		self.conn.commit()

		result=self.cursor.fetchall()

		sensors={}

		for row in result:
			sensors["pressure_id"]=row[0]
			sensors["heart_id"]=row[1]
			sensors["glucose_id"]=row[2]


		query="UPDATE info_patients SET processed=1 WHERE id_patient=%(key)s"
		self.cursor.execute(query,{"key":key})
		self.conn.commit()

		query="DELETE FROM data_sensors WHERE pressure_id=%s AND heart_id=%s AND glucose_id=%s"
		self.cursor.execute(query,(sensors["pressure_id"],sensors["heart_id"],sensors["glucose_id"]))
		self.conn.commit()

	
	'''DATA QUEUE PROCESSING'''

	def readDataQueue(self):
		query="SELECT i.id_patient, d.pressure_min, d.pressure_max, d.rate, d.glucose, i.code, i.age, i.time_stamp, i.name, i.surname, i.gender, d.pressure_id,d.heart_id,d.glucose_id FROM data_sensors d, info_patients i WHERE d.pressure_id=i.pressure_id AND d.heart_id=i.heart_id AND d.glucose_id=i.glucose_id AND i.processed=0 ORDER BY i.code,i.time_stamp ASC"
		self.cursor.execute(query)
		result=self.cursor.fetchall()

		queue={}
		for row in result:
			queue[row[0]]={
				"pressure_min":row[1],
				"pressure_max":row[2],
				"rate":row[3],
				"glucose":row[4],
				"code":row[5],
				"age":row[6],
				"time_stamp":str(row[7]),
				"name":row[8],
				"surname":row[9],
				"gender":row[10],
				"pressure_id":row[11],
				"heart_id":row[12],
				"glucose_id":row[13]
			}
			
		return json.dumps(queue)

	'''DATA STATISTIC PROCESSING'''

	def readStatistics(self):
		statistics={}
		queryage1="SELECT DISTINCT COUNT(*) as under25 FROM info_patients WHERE age<=25 AND analysed=0"
		queryage2="SELECT DISTINCT COUNT(*) as under45 FROM info_patients WHERE age<=45 AND age>25 AND analysed=0"
		queryage3="SELECT DISTINCT COUNT(*) as under55 FROM info_patients WHERE age<=55 and age>45 AND analysed=0"
		queryage4="SELECT DISTINCT COUNT(*) as under65 FROM info_patients WHERE age<=65 and age>55 AND analysed=0"
		queryage5="SELECT DISTINCT COUNT(*) as over65 FROM info_patients WHERE age>65 AND analysed=0"
		query2="SELECT DISTINCT unit, COUNT(*) as diff_units FROM info_patients WHERE analysed=0 GROUP BY unit"
		query3="SELECT DISTINCT gender, COUNT(*) as diff_genders FROM info_patients WHERE analysed=0 GROUP BY gender"
		query4="SELECT DISTINCT code, COUNT(*) as diff_codes FROM info_patients WHERE analysed=0 GROUP BY code"
		query5="SELECT COUNT(*) as obesity FROM info_patients WHERE CAST(weight as INT)/(CAST(height as INT)*CAST(height as INT)*0.0001)>30 AND analysed=0"

		self.cursor.execute(queryage1)
		result=self.cursor.fetchall()

		for row in result:
			if row[0]!=0:
				statistics["age"]={"under25":row[0]}

		self.cursor.execute(queryage2)
		result=self.cursor.fetchall()

		for row in result:
			if row[0]!=0:
				statistics["age"]={"under45":row[0]}

		self.cursor.execute(queryage3)
		result=self.cursor.fetchall()

		for row in result:
			if row[0]!=0:
				statistics["age"]={"under55":row[0]}

		self.cursor.execute(queryage4)
		result=self.cursor.fetchall()

		for row in result:
			if row[0]!=0:
				statistics["age"]={"under65":row[0]}

		self.cursor.execute(queryage5)
		result=self.cursor.fetchall()

		for row in result:
			if row[0]!=0:
				statistics["age"]={"over65":row[0]}

		self.cursor.execute(query2)
		result=self.cursor.fetchall()

		for row in result:
			if row[0]!=0:
				statistics["unit"]={row[0]:row[1]}

		self.cursor.execute(query3)
		result=self.cursor.fetchall()

		for row in result:
			if row[0]!=0:
				statistics["gender"]={row[0]:row[1]}

		self.cursor.execute(query4)
		result=self.cursor.fetchall()

		for row in result:
			if row[0]!=0:
				statistics["code"]={row[0]:row[1]}

		self.cursor.execute(query5)
		result=self.cursor.fetchall()

		for row in result:
			if row[0]!=0:
				statistics["obesity"]=row[0]

		queryupdate="UPDATE info_patients SET analysed=1"
		self.cursor.execute(queryupdate)
		self.conn.commit()

		return json.dumps(statistics)

	def closeconn(self):
		self.conn.close()
		self.cursor.close()