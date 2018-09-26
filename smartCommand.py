import requests
import time 
from subprocess import STDOUT, check_output

#output = check_output(cmd, stderr=STDOUT, timeout=seconds)
API_URL = 'http://192.168.2.25:9080/api'

oledList = ["OLED_1", "OLED_2", "OLED_3", "OLED_4", "OLED_5", "OLED_6", "OLED_7", "OLED_8", "OLED_9"]
lightsList = ["MARINA", "STREET_LIGHT", "TRAIN_STATION"]
towerList = ["S1_T1", "S1_T2", "S2_T1", "S4_T1"]
trafficLightsList = ["WEST_EAST","NORTH_SOUTH"]


class SmartTable():
       
        def __init__(self, building, color, image):
                self.building = building
                self.color = color
                self.image = image

	def getColor(self):
		return self.color
	def getImage(self):
		return self.image
	def getIdList(self):
		return self.building



def createSmartCityTableSession2(session):
	queryString = """mutation{
		
	"""
	idList = session.getIdList()
	color = colorRGB(session.getColor())
	image = session.getImage()

	i = 1
	queryList = similarList(idList, towerList)
        if queryList:
		queryString = towerQueryGenerate(queryList, queryString, color, image, i, "SOLID")
		i = i+1
		
	queryList = similarList(idList, ["WINDMILL"])
	if queryList:
		queryString = windmillQueryGenerate(queryList, queryString, color, image, i, "ON")
		i += 1
		queryString = windmillQueryFlagsGenerate(queryList, queryString, color, image, i)
		i += 1
	queryList = similarList(idList, ["UTILITY_POLE"])
	if queryList:
		queryString = utilityPoleQueryGenerate(queryList, queryString, color, image, i)
		i += 1
	queryList = similarList(idList, lightsList)
	if queryList:
		queryString = lightsQueryGenerate(queryList, queryString, color, image, i, "ON")
		i += 1
	queryList = similarList(idList, oledList)
	if queryList:
		queryString = oledQueryGenerate(queryList, queryString, color, image, i, "ON")
		i += 1
	queryString = queryString + "}"		
	print(queryString)
	json = {'query': queryString}

	request = requests.post(API_URL, json=json)

	if request.status_code == 200:
    		response = request.json()
    		print('response', response)
	else:
    		raise Exception(request.status_code)
	
		
def similarList(a, b):	
	return list(set(a) - (set(a) - set(b)))


def oledQueryGenerate(queryList, queryString, color, image, i, mode):
	queryString += "m" + str(i) + ": updateOleds(input: "
	stringified = "["
	for building_id in queryList:
		temp = "{id: " + building_id + ", mode: " + mode + ", image: " + image + "}," 
		stringified += temp
	stringified += "]) {id mode image },"
	queryString += stringified
	return queryString

def lightsQueryGenerate(queryList, queryString, color, image, i, mode):
        queryString += "m" + str(i) + ": updateLights(input: "
        stringified = "["
        for building_id in queryList:
                temp = "{id: " + building_id+ ", mode: " + mode + "},"
                stringified += temp
        stringified += "]"
        queryString = queryString + stringified + ") { id mode }, "
        return queryString
	

def utilityPoleQueryGenerate(queryList, queryString, color, image, i):
	utilityString = "m" + str(i) + ": updateUtilityPole(input: { color: PURPLE }){color},"
	return queryString + utilityString

def windmillQueryGenerate(queryList, queryString, color, image, i, mode):
	windmillString = "m" + str(i) + ": updateWindmills(input: { mode: " + mode + " ledMode: SOLID}) { mode }, \n" 
        queryString += windmillString
	return queryString

def windmillQueryFlagsGenerate(queryList, queryString, color, image, i):
	windmillFlagString = "m" + str(i) + ": createWindmillFlags(input: [{ icon: " + image + ", rgb: " + color + "},]){ icon rgb }"
	return queryString + windmillFlagString
	
def towerQueryGenerate(queryList, queryString, color, image, i, mode):
	stringified = "["
	queryString += "m" + str(i) + ": updateTowers(input: "
        stringified = "["
	for building_id in queryList:
    		temp = "{id: " + building_id+ ", mode: " + mode + "},"
    		stringified += temp 
	stringified += "]"
        queryString = queryString + stringified + ") { id mode }, " 		
	return queryString
 
def colorRGB(color):
	if color == "BLUE":
		color = "\"0,255,0\""
	elif color == "RED":
		color = "\"255,0,0\""
	elif color == "GREEN":
		color = "\"0,0,255\""
	elif color == "PURPLE":
		color =  "\"255,0,255\""
	elif color == "YELLOW":
		color = "\"255,255,0\""
	elif color == "AQUA":
		color = "\"0,255,255\""
	elif color == "WHITE":
		color = "\"255,255,255\""
	elif color == "GOLD":
		color = "\"255,226,0\""
	elif color == "TURQOIUS":
		color = "\"0,255,109\""
	elif color == "PINK":
		color = "\"255,0,136\""
	else:
		color = "\"173,255,0\""
 	return color
