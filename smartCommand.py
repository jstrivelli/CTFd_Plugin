import requests
import time 
from subprocess import STDOUT, check_output

#output = check_output(cmd, stderr=STDOUT, timeout=seconds)
API_URL = 'http://192.168.2.25:9080/api'

class SmartTable():
       
        def __init__(self, building, color, image):
                self.building = building
                self.color = color
                self.image = image

	def getColor(self):
		return self.color
	def getImage(self):
		return self.image
	def getBuilding(self):
		return self.building

def createSmartCityTableSession(session):

        # API_URL = 'http://127.0.0.1:9080/api'
	request = ""	
 	
	id = session.getBuilding()
        query = """
        mutation UpdateBuildings($input: [BuildingInput]!) {
       	updateBuildings(input: $input) {
                id
               	mode
        }
       	}
       	"""

	if id in ["MARINA", "STREET_LIGHT", "TRAIN_STATION"]:
		lightsCommand(session, API_URL)
	
	elif id in ["OLED_1", "OLED_2", "OLED_3", "OLED_4", "OLED_5", "OLED_6", "OLED_7", "OLED_8", "OLED_9"]:
		oledCommand(session,  API_URL)	
        buildings = [
               	{"id": session.getBuilding(), "mode": session.getColor()},
       	]

        variables = {'input': buildings}
        json = {'query': query, 'variables': variables}

        # usage without auth token
        print("Sending request for " + session.getBuilding() + " with color " + session.getColor())
			
	request = requests.post(API_URL, json=json)
		
	if request.status_code == 200:
                response = request.json()
                print('response', response)
		time.sleep(7)
		print("WE ARE SITTING AFTER THE TIMER")
		buildings = [
			{"id": session.getBuilding(), "mode":"WHITE"},
		]
		variables = {'input':buildings}
		json = {'query':query, 'variables': variables}
		request = requests.post(API_URL, json=json)
        else:
                raise Exception(request.status_code)


def lightsCommand(session, API_URL):
	query = """
		mutation {
  		updateLights(input: [
    		{ id: STREET_LIGHT, mode: OFF },
    		{ id: TRAIN_STATION, mode: ON }
  		]) {
    			id
    			mode
  		}
		}
	"""
	lights = [
		{"id": session.getBuilding(), "mode": "ON"}
	]
	variables = {'input': lights}
	json = {'query' : query, 'variables': variables}
	
	print("Sending request for " + session.getBuilding() + " to be turned ON ")
	
	request = requests.post(API_URL, json=json)
	if request.status_code == 200:
		response = request.json()
		print('response', response)
		time.sleep(20)
		lights=  [
			{"id": session.getBuilding(), "mode": "OFF"}
		]
		variables = {'input': lights}
		json = {'query' : query, 'variables': variables}
		request = requests.post(API_URL, json=json)
	else:
		raise Exception(request.status_code)


def oledCommand(session, API_URL):
	query = """
	mutation {
  		updateOleds(input: [
    		{ id: OLED_1, mode: OFF, image: MURRAY_1 },
    		{ id: OLED_2, mode: ON, image: MURRAY_2 },
    		{ id: OLED_3, mode: OFF, image: MURRAY_3 }
  		]) {
    		id
    		mode
    		image
  		}
	}
	"""
        oleds = [
		{"id": session.getBuilding(), "mode": "ON", "image": session.getImage()}
	]
	variables = {'input': oleds}
	json = {'query': query, 'variables': variables}

	print("Sending request for " + session.getBuilding() + "to be turned ON with image " + session.getImage())
	
	request = requests.post(API_URL, json=json)
	if requests.status_code == 200:
		response = requests.json
		print('response', response)
		time.sleep(20)
		oleds = [
                	{"id": session.getBuilding(), "mode": "ON", "image": session.getImage()}
        	]
		variables = {'input' : oleds}
		json = {'query': query, 'variab;les': variables}
		request = requests.post(API_URL, json=json)
	else:
		raise Exception(requests.status_code)


def trafficLightsCommand(session, API_URL):
	query = """mutation {
  		updateTrafficLights(input: {
    		mode: MANUAL
    		lights: [
      		{ mode: ON, color: RED, direction: WEST_EAST },
      		{ mode: ON, color: YELLOW, direction: WEST_EAST },
      		{ mode: OFF, color: GREEN, direction: NORTH_SOUTH },
      		{ mode: ON, color: YELLOW, direction: NORTH_SOUTH },
    		]
  		}) {
    		mode
    		lights {
      		mode
      		color
      		direction
    		}
  		}
		}

	"""
	trafficLights = [
		{"id"}
	]
