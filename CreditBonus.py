import requests
import json

from tkinter import *


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

#considered organizing types differently, not in use currently but saving for now


cards = {
    #Discover It Gas & Restaurant
    "Discover It Gas & Restaurant":{
        "gas_station":2,
        "restaurant":2,
        "all":1,
    },
    #Uber Visa card
    "Uber Visa card":{
        "restaurant":4,
        "bakery":4,
        "bar":4,
        "cafe":4,
        "hotel":3,
        "airport":3,
        "online":2,
        "all":1,
    },
    #Amazon Prime Rewards Visa Card
    "Amazon Prime Rewards Visa Card":{
        "Amazon":5,
        "Whole Foods Market":5,
        "restaurant":2,
        "gas_station":2,
        "drugstore":2,
        "all":1,
    }

}

def geoloc():
    #api-endpoint
    URL = "https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyBD4t8rfqbiV-Q8ThUjSWRBJKHNY-RQFQw"
    #defining a params dict for the parameters of the pull to be sent to the API
    PARAMS = {'key':'AIzaSyBD4t8rfqbiV-Q8ThUjSWRBJKHNY-RQFQw'}
    #get request
    data = requests.get(url = URL, params = PARAMS)



    print (data)


def latlong(name):
    # api-endpoint
    URL = "https://maps.googleapis.com/maps/api/geocode/json?address=" + name + "&key=AIzaSyBD4t8rfqbiV-Q8ThUjSWRBJKHNY-RQFQw"
    # location given here
    location = name
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'address':location, 'key':'AIzaSyBD4t8rfqbiV-Q8ThUjSWRBJKHNY-RQFQw'}
    # sending get request and saving the response as response object
    r = requests.get(url = URL, params = PARAMS)
    # json format
    data = r.json()

    # extracting latitude, longitude and formatted address
    # of the first matching location
    latitude = data['results'][0]['geometry']['location']['lat']
    longitude = data['results'][0]['geometry']['location']['lng']
    formatted_address = data['results'][0]['formatted_address']

    # printing the output
    print("Latitude:%s\nLongitude:%s\nFormatted Address:%s"
        %(latitude, longitude,formatted_address))
    return formatted_address



def estType(name):
    #api-endpoint
    URL = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + name + "&key=AIzaSyBD4t8rfqbiV-Q8ThUjSWRBJKHNY-RQFQw"

    PARAMS = {'address':name, 'key':'AIzaSyBD4t8rfqbiV-Q8ThUjSWRBJKHNY-RQFQw'}
    #import data from the api-endpoint
    r = requests.get(url = URL, params = PARAMS)
    #format data in JSON
    data = r.json()
    #extracts establishment type from json data
    checkName = data['results'][0]['name']
    types = data['results'][0]['types']


    #print("Name:", checkName, "\nTypes:", types)

    return types

def bingLatlong(name):
    #api-endpoint
    URL = "http://dev.virtualearth.net/REST/v1/Locations?query=" + name + "&includeNeighborhood=0&maxResults=1&key=AIzaSyBD4t8rfqbiV-Q8ThUjSWRBJKHNY-RQFQw"

    r = requests.get(url = URL)

    data = r.json()

    latitude = data['resourceSets']['resources']['geocodePoints']['coordinates'][0]
    longitude = data['resourceSets']['resources']['geocodePoints']['coordinates'][1]

    # printing the output
    print("Latitude:%s\nLongitude:%s"
        %(latitude, longitude))


def searchCard(types):
    #function built to determine which kind of card to use based on establishment types
    max = 0
    altmax = 0
    #for case that types value is empty/null, use best "all" card
    if types == None:
        for cardID, cardType in cards.items():
            if "all" in cardType:
                if cards[cardID]["all"] > altmax:
                    altmax = cards[cardID]["all"]
                    altID = cardID
    #run through the types of the search
    for i in range(len(types)):
        #run through the credit card dict
        for cardID, cardType in cards.items():
            #if the current type is within cards, max is equal to the value of the type within card
            if types[i] in cards[cardID]:
                if cards[cardID][types[i]] > max:
                    max = cards[cardID][types[i]]
                    maxID = cardID
            #account for types not matching
            if "all" in cardType:
                if cards[cardID]["all"] > altmax:
                    altmax = cards[cardID]["all"]
                    altID = cardID



    #return specific max vs all depending on larger value
    if max <= altmax:
        max = altmax
        maxID = altID
        print("Max Percentage: ", max)
        print("Best Card: ", maxID)
    else:
        print("Max Percentage: ", max)
        print("Best Card: ", maxID)
    return [max, maxID]

def execute(name):
    result = searchCard(estType(name))
    info1 = Label(master, text=result[0])
    info1.place(x = 170, y = 200)
    info2 = Message(master, text=result[1])
    info2.place(x = 170, y = 220)




#experimenting with tkinter here
import tkinter as tk
from tkinter import *
from tkinter import ttk
master = tk.Tk()
master.geometry("300x300")
master.title('CreditBonus')


maxtext = Label(master, text='Max Percentage: ')
maxtext.place(x = 60, y = 200)
cardtext = Label(master, text='Best Card: ')
cardtext.place(x = 60, y = 220)

prompt = Label(master, text='Location: ')
prompt.place(x=90, y=100)
e1 = tk.Entry(master)
e1.place(x = 90, y = 125)

button = tk.Button(master, text='Find Card', width=25, command= lambda: execute(e1.get()))
button.place(x=60, y=160)


mainloop()





#searchCard(estType('Black Eye Coffee'))
#estType("Akita International University")
#searchCard(latlong("Akita International University"))
#bingLatlong("Trader Joe's Boulder")
#geoloc()
