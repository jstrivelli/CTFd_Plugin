import requests
from subprocess import STDOUT, check_output

#output = check_output(cmd, stderr=STDOUT, timeout=seconds)

class SmartTable():
       
        def __init__(self, building, color, image):
                self.building = building
                self.color = color
                self.image = image

	def getColor():
		return color
	def getImage():
		return image
	def getBuilding():
		return building

	def createSmartCityTableSession(self):

        	# API_URL = 'http://127.0.0.1:9080/api'
       		API_URL = 'http://192.168.2.25:9080/api'


        	query = """
        	mutation UpdateBuildings($input: [BuildingInput]!) {
       		updateBuildings(input: $input) {
                	id
               		mode
        	 }
       		}
       		"""

        	buildings = [
                	{"id": self.building, "mode": self.color},
        	]

        	variables = {'input': buildings}
        	json = {'query': query, 'variables': variables}

        	# usage without auth token
                print("Sending request for " + self.building + " with color " + self.color)
		try:
			request = check_output(requests.post(API_URL, json=json), stderr=STDOUT, timeout=0.1)
      			print("TEST")
		except:
			print("didnt work")
		if request.status_code == 200:
                	response = request.json()
                	print('response', response)
        	else:
                	raise Exception(request.status_code)

# usage with auth token
# api_token = 'YOUR_API_TOKEN_HERE'
# headers = {'Authorization': 'token %s' % api_token}
# request = requests.post(API_URL, json=json, headers=headers)

