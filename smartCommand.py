import requests
import time 
from subprocess import STDOUT, check_output

#output = check_output(cmd, stderr=STDOUT, timeout=seconds)
API_URL = 'http://192.168.35.35:9080/api'

oledList = ["OLED_1", "OLED_2", "OLED_3", "OLED_4", "OLED_5", "OLED_6", "OLED_7", "OLED_8", "OLED_9"]
lightsList = ["MARINA", "STREET_LIGHT", "TRAIN_STATION"]
towerList = ["S1_T1", "S1_T2", "S2_T1", "S4_T1"]
trafficLightsList = ["WEST_EAST","NORTH_SOUTH"]
buildingList = [
"S1_B01", "S1_B02", "S1_B03", "S1_B04", "S1_B05","S2_B01", "S2_B02", "S2_B03", 
"S2_B04", "S2_B05", "S2_B06", "S2_B07", "S2_B08","S2_B09", "S2_B10", "S2_B11", 
"S2_B12", "S2_B13", "S2_B14", "S2_B15", "S2_B16","S2_B17", "S2_B18", "S2_B19", 
"S2_B20", "S2_B21", "S2_B22", "S2_B23", "S2_B24","S2_B25", "S2_B26","S3_B01", 
"S3_B02", "S3_B03", "S3_B04", "S3_B05", "S3_B06", "S3_B07", "S3_B08","S3_B09", 
"S3_B10", "S3_B11", "S3_B12", "S3_B13", "S3_B14","S4_B01", "S4_B02", "S4_B03", 
"S4_B04", "S4_B05", "S4_B06", "S4_B07", "S4_B08","S4_B09", "S4_B10", "S4_B11", 
"S4_B12", "S4_B13", "S4_B14", "S4_B15", "S4_B16","S4_B17","S5_B01", "S5_B02", 
"S5_B03", "S5_B04"
]

class SmartTable():
       
        def __init__(self, building, color, image, sound):
                self.building = building
                self.color = color
                self.image = image
		self.sound = sound

	def getColor(self):
		return self.color
	def getImage(self):
		return self.image
	def getIdList(self):
		return self.building
	def getSound(self):
		return self.sound


def createSmartCityTableSession2(session):
	#print(tableReset())
	queryString = """mutation{
		
	"""
	idList = session.getIdList()
	color = colorRGB(session.getColor())
	image = session.getImage()
	sound = session.getSound()

	i = 1
	queryList = similarList(idList, towerList)
        if queryList:
		queryString = towerQueryGenerate(queryList, queryString, color, image, i, "SOLID")
		i = i+1
		
	queryList = similarList(idList, ["WINDMILL"])
	if queryList:
		queryString = windmillQueryGenerate(queryList, queryString, color, image, i, "ON", "SOLID")
		i += 1
		queryString = windmillQueryFlagsGenerate(queryList, queryString, color, image, i)
		i += 1
	queryList = similarList(idList, ["UTILITY_POLE"])
	if queryList:
		queryString = utilityPoleQueryGenerate(queryList, queryString, "PURPLE", image, i)
		i += 1
	queryList = similarList(idList, lightsList)
	if queryList:
		queryString = lightsQueryGenerate(queryList, queryString, color, image, i, "ON")
		i += 1
		if "TRAIN_STATION" in idList:
			queryString = trainStationFlagQueryGenerate(queryList, queryString, color, image, i)
			i += 1
		if "MARINA" in idList:
			queryString = marinaFlagQueryGenerate(queryList, queryString, color, image, i)
			i += 1
	queryList = similarList(idList, oledList)
	if queryList:
		queryString = oledQueryGenerate(queryList, queryString, color, image, i, "ON")
		i += 1
	queryList = similarList(idList, buildingList)
	if queryList:
		queryString = buildingQueryGenerate(queryList, queryString, color, image, i)
		i += 1
		queryString = buildingFlagQueryGenerate(queryList, queryString, color, image, i)
		i += 1
	if sound:
		queryString = soundQueryGenerate(sound, queryString, i)
		i += 1
	queryString = queryString + "}"		
	print(queryString)
	json = {'query': queryString}
	
	time.sleep(3)
	print("First Request Sent")
	request = requests.post(API_URL, json=json)

	if request.status_code == 200:
    		response = request.json()
    		print('response', response)
	else:
    		raise Exception(request.status_code)
	

	time.sleep(25)
	
	print("Reset Request Sent")

	queryString = chalSolved(idList)

	print(queryString)
	#queryString = tableReset()
	json = {'query': queryString}
	request = requests.post(API_URL, json=json)
	
	if request.status_code == 200:
		response = request.json()
		print('response', response)
	else:
		raise Exception(request.status_code)
		
	
def similarList(a, b):	
	return list(set(a) - (set(a) - set(b)))

def marinaFlagQueryGenerate(queryList, queryString, color, image, i):
	queryString += "m" + str(i) + ": changeWaterColor(rgb: " + color + "),\n"
	return queryString

def soundQueryGenerate(sound, queryString, i):
	queryString += "m" + str(i) + ": playSound(soundId: " + sound + ")\n"
	return queryString

def trainStationFlagQueryGenerate(queryList, queryString, color, image, i):
	queryString += "m" + str(i) + ": createTrainStationFlags(input: "
	stringified = "[{ rgb: " + color  + ", icon: " + image + " },]),\n"
	queryString += stringified
	return queryString

def buildingQueryGenerate(queryList, queryString, color, image, i):
	queryString += "m" + str(i) + ": updateBuildingColors(input: "
	stringified = "["
	for building_id in queryList:
		temp = "{id: " + building_id + ", rgb: " + color + "},"
		stringified += temp
	stringified += "]) { id rgb },\n"
	queryString += stringified
	return queryString

def buildingFlagQueryGenerate(queryList, queryString, color, image, i):
	queryString += "m" + str(i) + ": createBuildingFlags(input: "
	stringified = "["
	for building_id in queryList:
		temp = "{buildingId: " + building_id + ", rgb: " + color + ", icon: " + image + "},"
		stringified += temp
	stringified += "]) { buildingId },\n" 
	queryString += stringified
	return queryString
	
def oledQueryGenerate(queryList, queryString, color, image, i, mode):
	queryString += "m" + str(i) + ": updateOleds(input: "
	stringified = "["
	for building_id in queryList:
		temp = "{id: " + building_id + ", mode: " + mode + ", image: " + image + "}," 
		stringified += temp
	stringified += "]) {id mode image },\n"
	queryString += stringified
	return queryString

def lightsQueryGenerate(queryList, queryString, color, image, i, mode):
        queryString += "m" + str(i) + ": updateLights(input: "
        stringified = "["
        for building_id in queryList:
                temp = "{id: " + building_id+ ", mode: " + mode + "},"
                stringified += temp
        stringified += "]"
        queryString = queryString + stringified + ") { id mode }, \n"
        return queryString
	

def utilityPoleQueryGenerate(queryList, queryString, color, image, i):
	utilityString = "m" + str(i) + ": updateUtilityPole(input: { color: " + color + " }){color},\n"
	return queryString + utilityString

def windmillQueryGenerate(queryList, queryString, color, image, i, mode, ledMode):
	windmillString = "m" + str(i) + ": updateWindmills(input: { mode: " + mode + ", ledMode: " + ledMode + "}) { mode }, \n" 
        queryString += windmillString
	return queryString

def windmillQueryFlagsGenerate(queryList, queryString, color, image, i):
	windmillFlagString = "m" + str(i) + ": createWindmillFlags(input: [{ icon: " + image + ", rgb: " + color + "},]){ icon rgb }\n"
	return queryString + windmillFlagString
	
def towerQueryGenerate(queryList, queryString, color, image, i, mode):
	stringified = "["
	queryString += "m" + str(i) + ": updateTowers(input: "
        stringified = "["
	for building_id in queryList:
    		temp = "{id: " + building_id+ ", mode: " + mode + "},"
    		stringified += temp 
	stringified += "]"
        queryString = queryString + stringified + ") { id mode }, \n"
	return queryString


def chalSolved(idList):
	queryString = """mutation{

	"""
	color = "\"255,255,255\""
	i = 1

	queryList = similarList(idList, buildingList)
	if queryList:
		queryString = buildingQueryGenerate(queryList, queryString, color, "MURRAY_1", i)
 		i += 1

	queryList = similarList(idList, oledList)
	if queryList:
		queryString = oledQueryGenerate(queryList, queryString, color, "MURRAY_1", i, "ON")
		i += 1
	queryString = towerQueryGenerate(towerList, queryString, color, "MURRAY_1", i, "OFF")
	i += 1
	queryString = windmillQueryGenerate(["WINDMILL"], queryString, color, "MURRAY_1", i, "OFF", "OFF")
	i += 1
	queryString = utilityPoleQueryGenerate(["UTILITY_POLE"], queryString, "RED", "MURRAY_1", i)
	i += 1
	queryString = lightsQueryGenerate(lightsList, queryString, color, "MURRAY_1", i, "OFF")
	i += 1
	queryString = marinaFlagQueryGenerate(idList, queryString, "\"255,255,255\"", "MURRAY_1", i)
	queryString += "}"
	return queryString
	
def tableReset():
	query = """mutation{

	"""
	color = "\"0,0,0\""
	query = buildingQueryGenerate(buildingList, query, color, "REGINALD", 1)
	query = oledQueryGenerate(oledList, query, color, "REGINALD", 2, "ON")
	query = towerQueryGenerate(towerList, query, color, "REGINALD", 3, "OFF")
	query = windmillQueryGenerate(["WINDMILL"], query, color, "REGINALD", 4, "OFF", "OFF")
	query = utilityPoleQueryGenerate(["UTILITY_POLE"], query, "RED", "REGINALD", 5)
	query = lightsQueryGenerate(lightsList, query, color, "REGINALD", 6, "OFF")
	query += "}"
	return query	

def colorRGB(color):
	if color == "BLUE":
		color = "\"0,0,255\""
	elif color == "RED":
		color = "\"255,0,0\""
	elif color == "GREEN":
		color = "\"0,255,0\""
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
	elif color == "TURQUOIS":
		color = "\"0,255,109\""
	elif color == "PINK":
		color = "\"255,0,136\""
	else:
		color = "\"173,255,0\""
 	return color
