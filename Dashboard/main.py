import json,requests,time
from urllib import response

# Function to convert time to date format DDMMYY and to return it
def	Convert_time_To_DdMmYy():
	timestamp = time.time()
	Datetime = time.strftime("%d%m%y", time.localtime(timestamp))
	return Datetime

# Function to connect to API
def Get_Api_Response(departStation,arrivalStation,datetime):
	date = Convert_time_To_DdMmYy()
	url = 'https://api.irail.be' 
	request = "/connections/?from="+departStation+"&to="+arrivalStation+"&date="+date+"&time="+datetime+"&timesel=departure&format=json&lang=en&typeOfTransport=all&alerts=false"
	response = requests.get(url+request).json()
	return response

# Function to subtract two hours
def Sub_Two_Hours():
	timestamp = time.time() - 7200
	subDatetime = time.strftime('%H%M', time.localtime(timestamp))
	return subDatetime

# Function to convert timestamp to time HHMM for request
def Convert_Timestamp_To_HhMm():
	timestamp = time.time()
	datetime = time.strftime('%H%M', time.localtime(timestamp))
	return datetime

# Function to add one hour in timestamp
def Add_One_Hour():
	expiration_time = time.time() + 3600
	return expiration_time

# Function to return the percentage of trains in operation.
def Pourcent_Trains_Circulation():
	pourcentTrain = dict()
	count1 = 0
	count2 = 0
	# Convert time to %HH%MM
	datetime = Convert_Timestamp_To_HhMm()
	# Get response from the API from Nivelles to Charleroi
	response_1= Get_Api_Response("Nivelles","Charleroi",datetime)
	#print(response_1)
	# Do a for loop to calculate the number of trains in circulation for the next hour from Nivelles to Charleroi
	for i in range(len(response_1['connection'])):
		if response_1['connection'][i]['departure']['time'] < str(Add_One_Hour()):
			count1 += 1
	# Calculate the percentage of trains in circulation from Nivelles to Charleroi
	pourcentTrain['pourcentTrainNivelles_To_Charleroi'] = (int((count1/len(response_1['connection']))*100))
	# Get response from the API from Charleroi to Nivelles
	response_2 = Get_Api_Response("Charleroi","Nivelles",datetime)
	# Do a for loop to calculate the number of trains in circulation for the next hour from Charleroi to Nivelles
	for i in range(len(response_2['connection'])):
		if response_1['connection'][i]['departure']['time'] < str(Add_One_Hour()):
			count2 += 1
	# Calculate the percentage of trains in circulation from Charleroi to Nivelles
	pourcentTrain['pourcentTrainCharleroi_To_Nivelles'] = (int((count2/len(response_2['connection']))*100))
	# Return a dictionary of the percentage of trains in circulation. 
	return pourcentTrain

# Function to return the average delay of trains
def Average_Delay_Trains():
	mylistDeparture_1 = list()
	mylistArrival_1 = list()
	mylistDeparture_2 = list()
	mylistArrival_2 = list()
	averageDelay = dict()
	# Convert timestamp to time format %HH%MM
	datetime = Convert_Timestamp_To_HhMm()
	# Get response from the API from Nivelles to Charleroi
	response_1= Get_Api_Response("Nivelles","Charleroi",datetime)
	# Do a for loop to add in a list the delay of the trains in circulation for the next hour from Nivelles to Charleroi
	for i in range(len(response_1['connection'])):
		if response_1['connection'][i]['departure']['time'] < str(Add_One_Hour()):
			# I calculated the train delays for the departures and the arrivals for each destination. I'm not sure if I have to just calculate the delays of departures!
			mylistDeparture_1.append(int(response_1['connection'][i]['departure']['delay']))
			mylistArrival_1.append(int(response_1['connection'][i]['arrival']['delay']))
	#print(mylistDeparture_1)
	#print(mylistArrival_1)
	# Calculate the average delay of trains from Nivelles to Charleroi and add it into dictionary.
	averageDelay['averageDelay_Departure_Nivelles_To_Charleroi'] = sum(mylistDeparture_1)/len(mylistDeparture_1)
	averageDelay['averageDelay_Arrival_Nivelles_To_Charleroi'] = sum(mylistArrival_1)/len(mylistArrival_1)
	# Get response from the API from Charleroi to Nivelles
	response_2= Get_Api_Response("Charleroi","Nivelles",datetime)
	# Do a for loop to add in a list the delays of trains in circulation for the next hour from Charleroi to Nivelles
	for i in range(len(response_2['connection'])):
		if response_2['connection'][i]['departure']['time'] < str(Add_One_Hour()):
			mylistDeparture_2.append(int(response_2['connection'][i]['departure']['delay']))
			mylistArrival_2.append(int(response_2['connection'][i]['arrival']['delay']))
	#print(mylistDeparture_2)
	#print(mylistArrival_2)
	# Calculate the average delay of the trains from Charleroi to Nivelles and add it into dictionary.
	averageDelay['averageDelay_Departure_Charleroi_To_Nivelles'] = sum(mylistDeparture_2)/len(mylistDeparture_2)
	averageDelay['averageDelay_Arrival_Charleroi_To_Nivelles'] = sum(mylistArrival_2)/len(mylistArrival_2)
	# Return a dictionary of the average train delay for the next hour 
	return averageDelay

# Function to return the number of cancelled trains
def Number_Of_Cancelled_Trains():
	mylist1 = list()
	mylist2 = list()
	NumberCanceledTrains = dict()
	# Subtract two hours from real time
	datetimePast = Sub_Two_Hours()
	# Get response from the API from Nivelles to Charleroi
	response_1= Get_Api_Response("Nivelles","Charleroi",datetimePast)
	# Do a for loop to add in a list the number of cancelled trains in circulation for the two previous hours from Nivelles to Charleroi
	for i in range(len(response_1['connection'])):
		if response_1['connection'][i]['departure']['time'] < str(time.time()):
			mylist1.append(int(response_1['connection'][i]['departure']['canceled']) + int(response_1['connection'][i]['arrival']['canceled']))
	# Calculate the sum of the cancelled trains and add it into a dictionary.
	NumberCanceledTrains['NumberCanceledTrainsNivelles_To_Charleroi'] = int(sum(mylist1))
	# Get response from the API from Charleroi to Nivelles
	response_2= Get_Api_Response("Charleroi","Nivelles",datetimePast)
	# Do a for loop to add in a list the number of cancelled trains in circulation for the two previous hours from Charleroi to Nivelles
	for i in range(len(response_2['connection'])):
		if response_2['connection'][i]['departure']['time'] < str(time.time()):
			mylist2.append(int(response_2['connection'][i]['departure']['canceled']) + int(response_2['connection'][i]['arrival']['canceled']))
	# Calculate the sum of the cancelled trains and add it into a dictionary
	NumberCanceledTrains['NumberCanceledTrainsCharleroi_To_Nivelles'] = int(sum(mylist2))
	# Return a dictionary with the number of cancelled trains
	return NumberCanceledTrains
 
# Create a jsonFile and add to it the final dictionary
def Create_Json_File(dictionary):
	json_object = json.dumps(dictionary, indent=4)
	with open('data.json','w') as file:
		file.write(json_object)

def main():	
	# Create a dictionary and add all the different dictionaries to it
	finalDict = dict()
	finalDict['percentage'] = Pourcent_Trains_Circulation()
	finalDict['averageDelay'] = Average_Delay_Trains()
	finalDict['numberOfCancelled'] = Number_Of_Cancelled_Trains()
	# Create a jsonFile and add to it the final dictionary
	Create_Json_File(finalDict)
	print(finalDict)
main()