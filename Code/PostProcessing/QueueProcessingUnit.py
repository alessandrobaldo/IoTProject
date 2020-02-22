import json
import time
import socket
import requests
import random

class QueueProcessingUnit(object):
	
	def __init__(self):
		s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		s.connect(('8.8.8.8',80))
		self.address=s.getsockname()[0]
		#self.catalog="http://192.168.1.103:8080"
		self.catalog=json.loads(open("catalog.json").read())["catalog"]
		'''
		self.my_data={
		"queue_server":
		{	
		"ip":socket.gethostbyname(socket.gethostname()),
		"port":8082,
		"topic":["queue"],
		"subscriber":["telegram_hospital"]
		}
		}'''
		self.id_patient=1
		self.queue={}
		
		self.my_data=json.loads(open("queueData.json").read())
		self.my_data["queue_server"]["ip"]=self.address

	def getAddress(self):
		return self.address

	def getData(self):
		return self.my_data

	def setData(self,data):
		self.mqtt=data[0]
		self.ip_others=data[1]
		self.thresh=data[2]
		self.tables=data[3]


	def configure(self):
		
		self.result=requests.post(self.catalog,json.dumps(self.my_data))

		self.mqtt=self.result.json()[0]
		self.ip_others=self.result.json()[1]
		self.thresh=self.result.json()[2]
		self.tables=self.result.json()[3]


	def getQueue(self):
		return self.queue
	
	def processData(self):
		print(self.queue)
		'''ASKING THE DB SERVER DATA OF CURRENT PATIENTS'''
		self.r=requests.get("http://"+self.ip_others["db_server"][0]+":"+self.ip_others["db_server"][1]+"/process")
		dataToProcess=self.r.json()

		position={}
		history_positions={}
		i=1
		for key in dataToProcess.keys():
			position[key]=i
			history_positions[key]=[]
			history_positions[key].append(i)
			i+=1
		
		for i in range(len(dataToProcess.keys())-1):
			for j in range(i+1,len(dataToProcess.keys())):
				key1=list(dataToProcess.keys())[i]
				key2=list(dataToProcess.keys())[j]

				flag1=0
				flag2=0

				if(dataToProcess[key1]["code"]==dataToProcess[key2]["code"]):
					age1=int(dataToProcess[key1]["age"])
					age2=int(dataToProcess[key2]["age"])

					minPres1=dataToProcess[key1]["pressure_min"]
					maxPres1=dataToProcess[key1]["pressure_max"]
					rate1=dataToProcess[key1]["rate"]
					glucose1=dataToProcess[key1]["glucose"]
					
					minPres2=dataToProcess[key2]["pressure_min"]
					maxPres2=dataToProcess[key2]["pressure_max"]
					rate2=dataToProcess[key2]["rate"]
					glucose2=dataToProcess[key2]["glucose"]

					flag1=self.manageQueueInit(key1,age1,minPres1,maxPres1,glucose1,rate1)
					flag2=self.manageQueueInit(key2,age2,minPres2,maxPres2,glucose2,rate2)

					if(flag2>flag1):
						position2=position[key2]
						position[key2]=position[key1]
						position[key1]=position2

					elif(flag1==flag2):
						time_stamp1=dataToProcess[key1]["time_stamp"]
						time_stamp2=dataToProcess[key2]["time_stamp"]

						if(time_stamp2>time_stamp1):
							position2=position[key2]
							position[key2]=position[key1]
							position[key1]=position2

							history_positions[key1].append(position[key1])
							history_positions[key2].append(position[key2])


		for key in history_positions.keys():
			if(dataToProcess[key]["code"]!=2):
				if(len(history_positions[key])>=5):
					trend=0
					for i in range(1, len(history_positions[key])):
						age=int(dataToProcess[key]["age"])
						minPres=dataToProcess[key]["pressure_min"]
						maxPres=dataToProcess[key]["pressure_max"]
						rate=dataToProcess[key]["rate"]
						glucose=dataToProcess[key]["glucose"]

						if(history_positions[key][i]<history_positions[key][i-1] or (history_positions[key][i]==history_positions[key][i-1] and self.manageQueueInit(key,age,minPres,maxPres,glucose,rate)!=0)):
							trend+=1
					if(trend>=5):
						dataToProcess[key]["code"]=dataToProcess[key]["code"]-1		

		
		position={k: v for k, v in sorted(position.items(), key=lambda item: item[1])}

		for key in position.keys():
			self.queue[key]=dataToProcess[key]

		print(self.queue)
		
		
	'''FUNCTION TO MANAGE POSITION IN THE QUEUE'''
	def manageQueueInit(self, key,age, minPres,maxPres,glucose,rate):
		flag=0
		if(age<=25):
			#min pressure
			minMinPres=self.thresh["UNDER25"][0]
			maxMinPres=self.thresh["UNDER25"][1]

			#max pressure
			minMaxPres=self.thresh["UNDER25"][4]
			maxMaxPres=self.thresh["UNDER25"][5]

			#gluc
			minGluc=self.thresh["UNDER25"][6]
			maxGluc=self.thresh["UNDER25"][7]

			#rate
			maxRate=208-0.7*int(age)

			if(minPres<minMinPres or minPres>maxMinPres):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(self.queue[key]["pressure_min"])-int(minPres))>0.6*(maxMinPres-minMinPres)):
						flag+=1


			if(maxPres<minMaxPres or maxPres>maxMaxPres):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(self.queue[key]["pressure_max"])-int(maxPres))>0.6*(maxMaxPres-minMaxPres)):
						flag+=1


			if(glucose<minGluc or glucose>maxGluc):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(self.queue[key]["glucose"])-int(glucose))>0.6*(maxGluc-minGluc)):
						flag+=1


			if(rate>maxRate):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(self.queue[key]["rate"])-int(rate))>0.25*(maxRate)):
						flag+=1



		elif(age>25 and age<=45):
			#min pressure
			minMinPres=self.thresh["UNDER45"][0]
			maxMinPres=self.thresh["UNDER45"][1]

			#max pressure
			minMaxPres=self.thresh["UNDER45"][4]
			maxMaxPres=self.thresh["UNDER45"][5]

			#gluc
			minGluc=self.thresh["UNDER45"][6]
			maxGluc=self.thresh["UNDER45"][7]

			#rate
			maxRate=208-0.7*age

			if(minPres<minMinPres or minPres>maxMinPres):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(self.queue[key]["pressure_min"])-int(minPres))>0.6*(maxMinPres-minMinPres)):
						flag+=1


			if(maxPres<minMaxPres or maxPres>maxMaxPres):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(self.queue[key]["pressure_max"])-int(maxPres))>0.6*(maxMaxPres-minMaxPres)):
						flag+=1


			if(glucose<minGluc or glucose>maxGluc):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(self.queue[key]["glucose"])-int(glucose))>0.6*(maxGluc-minGluc)):
						flag+=1


			if(rate>maxRate):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(self.queue[key]["rate"])-int(rate))>0.25*(maxRate)):
						flag+=1

		elif(age>45 and age<=55):
			#min pressure
			minMinPres=self.thresh["UNDER55"][0]
			maxMinPres=self.thresh["UNDER55"][1]

			#max pressure
			minMaxPres=self.thresh["UNDER55"][4]
			maxMaxPres=self.thresh["UNDER55"][5]

			#gluc
			minGluc=self.thresh["UNDER55"][6]
			maxGluc=self.thresh["UNDER55"][7]

			#rate
			maxRate=208-0.7*age

			if(minPres<minMinPres or minPres>maxMinPres):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(self.queue[key]["pressure_min"])-int(minPres))>0.6*(maxMinPres-minMinPres)):
						flag+=1


			if(maxPres<minMaxPres or maxPres>maxMaxPres):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(self.queue[key]["pressure_max"])-int(maxPres))>0.6*(maxMaxPres-minMaxPres)):
						flag+=1


			if(glucose<minGluc or glucose>maxGluc):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(self.queue[key]["glucose"])-int(glucose))>0.6*(maxGluc-minGluc)):
						flag+=1


			if(rate>maxRate):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(self.queue[key]["rate"])-int(rate))>0.25*(maxRate)):
						flag+=1
		elif(age>55 and age<=65):
			#min pressure
			minMinPres=self.thresh["UNDER65"][0]
			maxMinPres=self.thresh["UNDER65"][1]

			#max pressure
			minMaxPres=self.thresh["UNDER65"][4]
			maxMaxPres=self.thresh["UNDER65"][5]

			#gluc
			minGluc=self.thresh["UNDER65"][6]
			maxGluc=self.thresh["UNDER65"][7]

			#rate
			maxRate=208-0.7*age

			if(minPres<minMinPres or minPres>maxMinPres):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(self.queue[key]["pressure_min"])-int(minPres))>0.6*(maxMinPres-minMinPres)):
						flag+=1


			if(maxPres<minMaxPres or maxPres>maxMaxPres):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(self.queue[key]["pressure_max"])-int(maxPres))>0.6*(maxMaxPres-minMaxPres)):
						flag+=1


			if(glucose<minGluc or glucose>maxGluc):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(self.queue[key]["glucose"])-int(glucose))>0.6*(maxGluc-minGluc)):
						flag+=1


			if(rate>maxRate):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(self.queue[key]["rate"])-int(rate))>0.25*(maxRate)):
						flag+=1
		else:
			#min pressure
			minMinPres=self.thresh["OVER65"][0]
			maxMinPres=self.thresh["OVER65"][1]

			#max pressure
			minMaxPres=self.thresh["OVER65"][4]
			maxMaxPres=self.thresh["OVER65"][5]

			#gluc
			minGluc=self.thresh["OVER55"][6]
			maxGluc=self.thresh["OVER65"][7]

			#rate
			maxRate=208-0.7*age

			if(minPres<minMinPres or minPres>maxMinPres):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(self.queue[key]["pressure_min"])-int(minPres))>0.6*(maxMinPres-minMinPres)):
						flag+=1


			if(maxPres<minMaxPres or maxPres>maxMaxPres):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(self.queue[key]["pressure_max"])-int(maxPres))>0.6*(maxMaxPres-minMaxPres)):
						flag+=1


			if(glucose<minGluc or glucose>maxGluc):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(self.queue[key]["glucose"])-int(glucose))>0.6*(maxGluc-minGluc)):
						flag+=1


			if(rate>maxRate):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(self.queue[key]["rate"])-int(rate))>0.25*(maxRate)):
						flag+=1
		return flag

	def processPatient(self):
		n=random.randint(1,4)
		m=len(list(self.queue.keys()))

		if(m!=0):
			try:
				for i in range(min(n,m)):
					patient={"key":list(self.queue.keys())[i]}
					sensors={
						"code":self.queue[patient["key"]]["code"],
						"pressure_id":self.queue[patient["key"]]["pressure_id"],
						"heart_id":self.queue[patient["key"]]["heart_id"],
						"glucose_id":self.queue[patient["key"]]["glucose_id"],
					}

					del self.queue[patient["key"]]
					r=requests.delete("http://"+self.ip_others["db_server"][0]+":"+self.ip_others["db_server"][1]+"/"+patient["key"])
					r=requests.delete("http://"+self.ip_others["time_shift"][0]+":"+self.ip_others["time_shift"][1]+"/"+str(sensors["code"])+"/"+str(sensors["pressure_id"])+"/"+str(sensors["heart_id"])+"/"+str(sensors["glucose_id"]))
					r=requests.delete(self.catalog+"/"+str(sensors["pressure_id"])+"/"+str(sensors["heart_id"])+"/"+str(sensors["glucose_id"]))

			except:
				print("Some error occurred")
		else:
			print("No patient to process")



	def sendDataDatabase(self,command, data):
		r=requests.put("http://"+self.ip_others["db_server"][0]+":"+self.ip_others["db_server"][1]+"/"+command,data)

	def askDataSensors(self,id1,id2,id3):
		sensors={
		"pressure":id1,
		"heart":id2,
		"glucose":id3
		}

		r=requests.get("http://"+self.ip_others["ihealth_adapter"][0]+":"+self.ip_others["ihealth_adapter"][1]+"/"+sensors["pressure"]+"/"+sensors["heart"]+"/"+sensors["glucose"])
		self.sendDataDatabase("sensors",json.dumps(r.json()))

	def sendDataTime(self,data):
		r=requests.put("http://"+self.ip_others["time_shift"][0]+":"+self.ip_others["time_shift"][1],data)

	def getCurrentPatient(self):
		self.id_patient+=1
		return self.id_patient-1

	def getIps(self):
		return self.ip_others

	def getTopicsSubscriber(self):
		return self.mqtt
	def getTopicPublisher(self):
		return self.my_data["queue_server"]["topic"][0]
	def getInfoDb(self):
		return self.tables