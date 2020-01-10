import json
import time
import socket
import requests
import random

class QueueProcessingUnit(object):
	
	def __init__(self):
		
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
		self.my_data["queue_server"]["ip"]=socket.gethostbyname(socket.gethostname())

	def configure(self):
		
		self.result=requests.post(self.catalog,json.dumps(self.my_data))

		self.mqtt=self.result.json()[0]
		self.ip_others=self.result.json()[1]
		self.thresh=self.result.json()[2]
		self.tables=self.result.json()[3]

		#print(json.dumps(self.mqtt,indent=4))
		#print(json.dumps(self.ip_others,indent=4))
		#print(json.dumps(self.thresh,indent=4))		
		#print(json.dumps(self.tables,indent=4))

	def getQueue(self):
		return self.queue
	
	def processData(self):
		self.r=requests.get("http://"+self.ip_others["db_server"][0]+":"+self.ip_others["db_server"][1]+"/process")
		dataToProcess=self.r.json()


		position={}
		i=1
		for key in dataToProcess.keys():
			position[key]=i
			i+=1
		
		for i in range(len(dataToProcess.keys())-1):
			for j in range(1,len(dataToProcess.keys())):
				key1=dataToProcess.keys()[i]
				key2=dataToProcess.keys()[j]

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

		
		position={k: v for k, v in sorted(position.items(), key=lambda item: item[1])}

		for key in position.keys():
			self.queue[key]=dataToProcess[key]

		print(self.queue)
		
		

	def manageQueueInit(self, key,age, minPres,maxPres,glucose,rate):
		flag=0
		if(age<=25):
			#min pressure
			minMinPres=thresh["UNDER25"][0]
			maxMinPres=thresh["UNDER25"][1]

			#max pressure
			minMaxPres=thresh["UNDER25"][4]
			maxMaxPres=thresh["UNDER25"][5]

			#gluc
			minGluc=thresh["UNDER25"][6]
			maxGluc=thresh["UNDER25"][7]

			#rate
			maxRate=208-0.7*int(age)

			if(minPres<minMinPres or minPres>maxMinPres):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(queue[key]["pressure_min"])-int(minPres))>0.6(maxMinPres-minMinPres)):
						flag+=1


			if(maxPres<minMaxPres or maxPres>maxMaxPres):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(queue[key]["pressure_max"])-int(maxPres))>0.6(maxMaxPres-minMaxPres)):
						flag+=1


			if(glucose<minGluc or glucose>maxGluc):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(queue[key]["glucose"])-int(glucose))>0.6(maxGluc-minGluc)):
						flag+=1


			if(rate>maxRate):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(queue[key]["rate"])-int(rate))>0.25(maxRate)):
						flag+=1



		elif(age>25 and age<=45):
			#min pressure
			minMinPres=thresh["UNDER45"][0]
			maxMinPres=thresh["UNDER45"][1]

			#max pressure
			minMaxPres=thresh["UNDER45"][4]
			maxMaxPres=thresh["UNDER45"][5]

			#gluc
			minGluc=thresh["UNDER45"][6]
			maxGluc=thresh["UNDER45"][7]

			#rate
			maxRate=208-0.7*age

			if(minPres<minMinPres or minPres>maxMinPres):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(queue[key]["pressure_min"])-int(minPres))>0.6(maxMinPres-minMinPres)):
						flag+=1


			if(maxPres<minMaxPres or maxPres>maxMaxPres):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(queue[key]["pressure_max"])-int(maxPres))>0.6(maxMaxPres-minMaxPres)):
						flag+=1


			if(glucose<minGluc or glucose>maxGluc):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(queue[key]["glucose"])-int(glucose))>0.6(maxGluc-minGluc)):
						flag+=1


			if(rate>maxRate):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(queue[key]["rate"])-int(rate))>0.25(maxRate)):
						flag+=1

		elif(age>45 and age<=55):
			#min pressure
			minMinPres=thresh["UNDER55"][0]
			maxMinPres=thresh["UNDER55"][1]

			#max pressure
			minMaxPres=thresh["UNDER55"][4]
			maxMaxPres=thresh["UNDER55"][5]

			#gluc
			minGluc=thresh["UNDER55"][6]
			maxGluc=thresh["UNDER55"][7]

			#rate
			maxRate=208-0.7*age

			if(minPres<minMinPres or minPres>maxMinPres):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(queue[key]["pressure_min"])-int(minPres))>0.6(maxMinPres-minMinPres)):
						flag+=1


			if(maxPres<minMaxPres or maxPres>maxMaxPres):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(queue[key]["pressure_max"])-int(maxPres))>0.6(maxMaxPres-minMaxPres)):
						flag+=1


			if(glucose<minGluc or glucose>maxGluc):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(queue[key]["glucose"])-int(glucose))>0.6(maxGluc-minGluc)):
						flag+=1


			if(rate>maxRate):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(queue[key]["rate"])-int(rate))>0.25(maxRate)):
						flag+=1
		elif(age>55 and age<=65):
			#min pressure
			minMinPres=thresh["UNDER65"][0]
			maxMinPres=thresh["UNDER65"][1]

			#max pressure
			minMaxPres=thresh["UNDER65"][4]
			maxMaxPres=thresh["UNDER65"][5]

			#gluc
			minGluc=thresh["UNDER65"][6]
			maxGluc=thresh["UNDER65"][7]

			#rate
			maxRate=208-0.7*age

			if(minPres<minMinPres or minPres>maxMinPres):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(queue[key]["pressure_min"])-int(minPres))>0.6(maxMinPres-minMinPres)):
						flag+=1


			if(maxPres<minMaxPres or maxPres>maxMaxPres):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(queue[key]["pressure_max"])-int(maxPres))>0.6(maxMaxPres-minMaxPres)):
						flag+=1


			if(glucose<minGluc or glucose>maxGluc):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(queue[key]["glucose"])-int(glucose))>0.6(maxGluc-minGluc)):
						flag+=1


			if(rate>maxRate):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(queue[key]["rate"])-int(rate))>0.25(maxRate)):
						flag+=1
		else:
			#min pressure
			minMinPres=thresh["OVER65"][0]
			maxMinPres=thresh["OVER65"][1]

			#max pressure
			minMaxPres=thresh["OVER65"][4]
			maxMaxPres=thresh["OVER65"][5]

			#gluc
			minGluc=thresh["OVER55"][6]
			maxGluc=thresh["OVER65"][7]

			#rate
			maxRate=208-0.7*age

			if(minPres<minMinPres or minPres>maxMinPres):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(queue[key]["pressure_min"])-int(minPres))>0.6(maxMinPres-minMinPres)):
						flag+=1


			if(maxPres<minMaxPres or maxPres>maxMaxPres):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(queue[key]["pressure_max"])-int(maxPres))>0.6(maxMaxPres-minMaxPres)):
						flag+=1


			if(glucose<minGluc or glucose>maxGluc):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(queue[key]["glucose"])-int(glucose))>0.6(maxGluc-minGluc)):
						flag+=1


			if(rate>maxRate):
				flag+=1
				if key in self.queue.keys():
					if(abs(int(queue[key]["rate"])-int(rate))>0.25(maxRate)):
						flag+=1
		return flag

	def processPatient(self):
		n=random.randint(1,4)

		try:
			for i in range(n):
				patient={"key":queue.keys()[i]}
				r=requests.delete("http://"+self.ip_others["db_server"][0]+":"+self.ip_others["db_server"][1],json.dumps(patient))

		except:
			print("No patient to process")



	def sendDataDatabase(self,command, data):
		r=requests.put("http://"+self.ip_others["db_server"][0]+":"+self.ip_others["db_server"][1]+"/"+command,json.dumps(data))

	def askDataSensors(self,id1,id2,id3):
		sensors={
		"pressure":id1,
		"heart":id2,
		"glucose":id3
		}

		r=requests.put("http://"+self.ip_others["ihealth_adapter"][0]+":"+self.ip_others["ihealth_adapter"][1],json.dumps(sensors))

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