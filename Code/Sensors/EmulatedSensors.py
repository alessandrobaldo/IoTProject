import random
import json


class GlucoseSensor(object):
	def __init__(self):
		pass

	def getMeasurement(self):
		glucose_level={
		"glucose":random.randint(30,190)
		}
		return json.dumps(glucose_level)

class PressureSensor(object):
	def __init__(self):
		pass

	def getMeasurement(self):
		minim=random.randint(50,128)
		pressure={
		"min":minim,
		"max":random.randint(minim,170)
		}

		return json.dumps(pressure)

class HeartSensor(object):
	def __init__(self):
		pass

	def getMeasurement(self):
		heart={
		"rate":random.randint(35,180),
		}

		return json.dumps(heart)
