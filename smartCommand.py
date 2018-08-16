import requests
import time 
from subprocess import STDOUT, check_output

#output = check_output(cmd, stderr=STDOUT, timeout=seconds)

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
       	API_URL = 'http://192.168.2.25:9080/api'
	request = ""		

        query = """
        mutation UpdateBuildings($input: [BuildingInput]!) {
       	updateBuildings(input: $input) {
                id
               	mode
        }
       	}
       	"""
	id = session.getBuilding()

	#if id in ["MARINA", "STREET_LIGHT", "TRAIN_STATION"]:
	#	lightsCommand(session)
	
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


def lightsCommand(session):
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

# usage with auth token
# api_token = 'YOUR_API_TOKEN_HERE'
# headers = {'Authorization': 'token %s' % api_token}
# request = requests.post(API_URL, json=json, headers=headers)

