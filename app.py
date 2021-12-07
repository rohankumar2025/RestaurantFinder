#my API KEY: AIzaSyDyiSclZPTIWJyVB2B1BSMWOs9Z6e6v1dM
  
# importing required modules
import requests, json
from tkinter import *

Restaurants = {}
city = ""
foodType = ""

# url for API call
url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
api_key = 'AIzaSyAOkl_9l3DVkO2RtDEmp_F4mpUdDKm6AVc'

def printLists():
    global city, foodType, Restaurants

    if (len(Restaurants) == 0):
        restaurantLabel = Label(root, text="Sorry, there are no more " + foodType + " restaurants in " + city)    
    else: 
        # uses API to print name of restaurant
        restaurantLabel = Label(root, text=Restaurants[0]['name'])
        
        # uses info from API to create $$$ text
        dollarSignsText = ""
        numDollarSigns = Restaurants[0]['price_level']
        for i in range (0, numDollarSigns):
            dollarSignsText = dollarSignsText + "$"
        priceRating = Label(root, text=dollarSignsText)
    
    restaurantLabel.pack() # FIX FORMATTING LATER
    priceRating.pack() # FIX FORMATTING LATER


    # deletes current restaurant from array
    del Restaurants[0]

    displayYNButtons()

def displayYNButtons():
    yesButton = Button(root, text="Yes")
    yesButton.pack() # FIX FORMATTING LATER

    noButton = Button(root, text="No", command=printLists)
    noButton.pack() # FIX FORMATTING LATER

def makeAPICall(cityLocation, restaurantType):
    # calls API, stores requests in 'req'
    req = requests.get(url + 'query=' + restaurantType + 'restaurants in ' + cityLocation + '&key=' + api_key)
    reqJSON = req.json() # converts req to json type

    return reqJSON['results']

def handleSubmit():
    # assigns proper inputs to 'city' and 'foodType' variables
    global city, foodType, Restaurants # calls global variables

    city = locationTextBox.get()
    foodType = typeFoodTextBox.get()

    Restaurants = makeAPICall(city, foodType)
    printLists()

# creating GUI
root = Tk()
root.title('Restaurant Finder')
root.geometry("600x600")

locationLabel = Label(root, text="Where are you right now:")
locationLabel.pack() # FIX FORMATTING LATER

locationTextBox = Entry(root, width=30)
locationTextBox.pack() # FIX FORMATTING LATER

typeFoodLabel = Label(root, text="What type of food do you want:")
typeFoodLabel.pack() # FIX FORMATTING LATER

typeFoodTextBox = Entry(root, width=30)
typeFoodTextBox.pack() # FIX FORMATTING LATER

submitButton = Button(root, text="Submit", command=handleSubmit)
submitButton.pack() # FIX FORMATTING LATER

root.mainloop()
