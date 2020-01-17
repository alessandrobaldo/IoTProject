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
		
		try:
			self.conn=mysql.connector.connect(user='root',password='',host='127.0.0.1',database='PatientsData')
			self.cursor=self.conn.cursor()
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
					) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;\
					DROP TABLE IF EXISTS `info_patients`;\
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
					) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
			self.cursor.execute(query,multi=True)
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
		print(json.dumps(self.ip_others,indent=4))

	def configure(self):
		self.result=requests.post(self.catalog,json.dumps(self.my_data))
		self.ip_others=self.result.json()
		print(json.dumps(self.ip_others,indent=4))

	def getIps(self):
		return self.ip_others

	def insertDataSensors(self,data):
		
		add_sensors_data=("INSERT INTO data_sensors (pressure_id,heart_id,glucose_id,pressure_min,pressure_max,rate,glucose,time_stamp) VALUES (%s,%s,%s,%s,%s,%s,%s)")
		data_patient=(data["pressure_id"],data["heart_id"],data["glucose_id"],data["pressure_min"],data["pressure_max"],data["rate"],data["glucose"],data["time_stamp"])
		self.cursor.execute(add_sensors_data,data_patient)
		self.conn.commit()
		

	def insertDataTelegram(self,data):
		
		add_patients_data=("INSERT INTO info_patients (id_patient,pressure_id,heart_id,glucose_id,name,surname,age,height,weight,gender,code,unit,time_stamp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
		patient_registry=(data["id_patient"],data["pressure_id"],data["heart_id"],data["glucose_id"],data["name"],data["surname"],data["age"],data["height"],data["weight"],data["gender"],data["code"],data["unit"],data["time_stamp"])
		self.cursor.execute(add_patients_data,patient_registry)
		self.conn.commit()

	def removePatient(self, key):
		query="SELECT pressure_id,heart_id,glucose_id FROM info_patient WHERE id_patient=%(key)s"
		self.cursor.execute(query,{"key":key})
		self.conn.commit()

		result=self.cursor.fetchall()

		sensors={}

		for row in result:
			sensors["pressure"]=row[0]
			sensors["heart"]=row[1]
			sensors["glucose"]=row[2]

		r=requests.delete(self.catalog,json.dumps(sensors))



		query="DELETE FROM info_patients WHERE id_patient=%(key)s"
		self.cursor.execute(query,{"key":key})
		self.conn.commit()

		query="DELETE FROM data_sensors WHERE id_patient=%(key)s"
		self.cursor.execute(query,{"key":key})
		self.conn.commit()


	def readDataQueue(self):
		query="SELECT i.id_patient, d.pressure_min, d.pressure_max, d.rate, d.glucose, i.code, i.age, i.time_stamp FROM data_sensors d, info_patients i WHERE d.pressure_id=i.pressure_id AND d.heart_id=i.heart_id AND d.glucose_id=i.glucose_id ORDER BY i.code ASC"
		self.cursor.execute(query)
		result=self.cursor.fetchall()

		queue={}
		for row in result:
			queue[row[0]]["pressure_min"]=row[1]
			queue[row[0]]["pressure_max"]=row[2]
			queue[row[0]]["rate"]=row[3]
			queue[row[0]]["glucose"]=row[4]
			queue[row[0]]["code"]=row[5]
			queue[row[0]]["age"]=row[6]
			queue[row[0]]["time_stamp"]=row[7]

		return json.dumps(queue)

	def readStatistics(self):

		statistics={}
		queryage1="SELECT DISTINCT COUNT(*) as under25 FROM info_patients WHERE age<=25 GROUP BY age"
		queryage2="SELECT DISTINCT COUNT(*) as under45 FROM info_patients WHERE age<=45 AND age>25 GROUP BY age"
		queryage3="SELECT DISTINCT COUNT(*) as under55 FROM info_patients WHERE age<=55 and age>45 GROUP BY age"
		queryage4="SELECT DISTINCT COUNT(*) as under65 FROM info_patients WHERE age<=65 and age>55 GROUP BY age"
		queryage5="SELECT DISTINCT COUNT(*) as over65 FROM info_patients WHERE age>65 GROUP BY age"
		query2="SELECT DISTINCT unit, COUNT(*) as diff_units FROM info_patients GROUP BY unit"
		query3="SELECT DISTINCT gender, COUNT(*) as diff_genders FROM info_patients GROUP BY gender"
		query4="SELECT DISTINCT code, COUNT(*) as diff_codes FROM info_patients GROUP BY code"
		query5="SELECT COUNT(*) as obesity FROM info_patients WHERE CAST(weight as INT)/(CAST(height as INT)*CAST(height as INT)*0.0001)>30"

		self.cursor.execute(queryage1)
		result=self.cursor.fetchall()

		for row in result:
			statistics["age"]["under25"]=row[0]

		self.cursor.execute(queryage2)
		result=self.cursor.fetchall()

		for row in result:
			statistics["age"]["under45"]=row[0]

		self.cursor.execute(queryage3)
		result=self.cursor.fetchall()

		for row in result:
			statistics["age"]["under55"]=row[0]

		self.cursor.execute(queryage4)
		result=self.cursor.fetchall()

		for row in result:
			statistics["age"]["under65"]=row[0]

		self.cursor.execute(queryage5)
		result=self.cursor.fetchall()

		for row in result:
			statistics["age"]["over65"]=row[0]

		self.cursor.execute(query2)
		result=self.cursor.fetchall()

		for row in result:
			statistics["unit"][row[0]]=row[1]

		self.cursor.execute(query3)
		result=self.cursor.fetchall()

		for row in result:
			statistics["gender"][row[0]]=row[1]

		self.cursor.execute(query4)
		result=self.cursor.fetchall()

		for row in result:
			statistics["code"][row[0]]=row[1]

		self.cursor.execute(query5)
		result=self.cursor.fetchall()

		for row in result:
			statistics["obesity"]=[row[0]]


		return json.dumps(statistics)

	def closeconn(self):
		self.conn.close()
		self.cursor.close()