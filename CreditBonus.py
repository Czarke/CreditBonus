import requests
import json

typedict = {
    "food" : ["bakery", "bar", "cafe", "meal_delivery", "meal_takeaway", "restaurant"],
    "travel" : ["airport", "hotel", "bus_station", "car_rental", "subway_station", "travel_agency"],
    "gas" : ["gas_station"],
    "grocery" : ["grocery", "grocery_or_supermarket", "supermarket", "convenience_store"]
}

food = ["bakery", "bar", "cafe", "meal_delivery", "meal_takeaway", "restaurant"]

travel = ["airport", "hotel", "bus_station", "car_rental", "subway_station", "travel_agency"]

gas = ["gas_station"]

grocery = ["grocery", "grocery_or_supermarket", "supermarket", "convenience_store"]

cards = {
    "Discover It Gas & Restaurant":{
        "gas":2,
        "restaurant":2,
        "all":1,
        "type":"Discover"
    },
    "Uber Visa Card":{
        "restaurant":4,
        "bakery":4,
        "bar":4,
        "cafe":4,
        "hotel":3,
        "airfare":3,
        "online":2,
        "all":1,
        "type":"Visa"
    },
    "Amazon Prime Rewards Visa Card":{
        "Amazon":5,
        "Whole Foods Market":5,
        "dining":2,
        "gas":2,
        "drugstore":2,
        "all":1,
        "type":"Visa"
    }

}

def latlong(name):
    # api-endpoint
    URL = "https://maps.googleapis.com/maps/api/geocode/json?address=" + name + "&key=AIzaSyC-KV06-_bl1FaE68-YXlydtcq53EDC75Y"
    # location given here
    location = name
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'address':location, 'key':'AIzaSyC-KV06-_bl1FaE68-YXlydtcq53EDC75Y'}
    # sending get request and saving the response as response object
    r = requests.get(url = URL, params = PARAMS)
    # extracting data in json format
    data = r.json()

    # extracting latitude, longitude and formatted address
    # of the first matching location
    latitude = data['results'][0]['geometry']['location']['lat']
    longitude = data['results'][0]['geometry']['location']['lng']
    formatted_address = data['results'][0]['formatted_address']

    # printing the output
    print("Latitude:%s\nLongitude:%s\nFormatted Address:%s"
        %(latitude, longitude,formatted_address))

def estType(name):
    #api-endpoint
    URL = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + name + "&key=AIzaSyC-KV06-_bl1FaE68-YXlydtcq53EDC75Y"

    PARAMS = {'address':name, 'key':'AIzaSyC-KV06-_bl1FaE68-YXlydtcq53EDC75Y'}

    r = requests.get(url = URL, params = PARAMS)

    data = r.json()

    #extracts establishment type from json data
    checkName = data['results'][0]['name']
    types = data['results'][0]['types']


    print("Name:", checkName, "\nTypes:", types)

    return types

def bingLatlong(name):
    #api-endpoint
    URL = "http://dev.virtualearth.net/REST/v1/Locations?query=" + name + "&includeNeighborhood=0&maxResults=1&key=Al6EkyXVZzsE-2yMd30z56LyZrYLZS_K077Gpqw44MO_5UMEYru83027pvCw-_N-"

    r = requests.get(url = URL)

    data = r.json()

    latitude = data['resourceSets']['resources']['geocodePoints']['coordinates'][0]
    longitude = data['resourceSets']['resources']['geocodePoints']['coordinates'][1]

    # printing the output
    print("Latitude:%s\nLongitude:%s"
        %(latitude, longitude))


def whichCard(types):
    #function built to determine which kind of card to use based on establishment types
    max = 0
    #run through the types of the search
    for i in types:
        #run through the credit card dict
        for j in cards:
            #if the current type is within cards, max is equal to the value of the type within card
            if types[i] in cards[j]:
                if cards[j][types[i]] > max:
                    max = cards[j][types[i]]

    print("Max:", max)


whichCard(estType("Trader Joe's Boulder"))
#estType("Akita International University")
#latlong("Trader Joe's Boulder")
#bingLatlong("Trader Joe's Boulder")
