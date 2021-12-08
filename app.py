#my API KEY: AIzaSyDyiSclZPTIWJyVB2B1BSMWOs9Z6e6v1dM
  
# importing required modules
import requests, json
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk 
import PIL 
from io import BytesIO
# global variables
Restaurants = {}
city = ""
foodType = ""
restaurantLabels = {}

# url for API call
url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
photo_url = "https://maps.googleapis.com/maps/api/place/photo?"
api_key = 'AIzaSyAOkl_9l3DVkO2RtDEmp_F4mpUdDKm6AVc'


def printLabels():
    global restaurantLabels
    # FIXME: NEED TO CLEAR OLD LABELS BEFORE PRINTING NEW ONES

    for i in range(len(restaurantLabels)):
        restaurantLabels[i].pack() # FIX FORMATTING LATER


def createLabels():
    global city, foodType, Restaurants, restaurantLabels
    restaurantLabels = [] # erases restaurantLabels list

    # Key for Labels:
    # restaurantLabels[0] : Name of Restaurant OR Error Message if No More Available Restaurants
    # restaurnatLabels[1] : Address
    # restaurantLabels[2] : Star Rating
    # restaurantLabels[3] : $$$ indicating Price Level
    # restaurantLabels[4] : Number of results left
    for widget in root.winfo_children():
       widget.pack_forget()

    try:
        restaurantLabels.append(Label(root, text=Restaurants[0]['name']))
    except:
        restaurantLabels.append(Label(root, text="Sorry, there are no " + foodType + " restaurants in " + city)) # Error Message 

    # MAKE CODE MORE EFFICIENT USING ARRAY STORING 'name', 'formatted_address', 'rating', etc. #
     
    # creates $$$ text
    try:
        dollarSignsText = ""
        numDollarSigns = Restaurants[0]['price_level']
        for i in range (0, numDollarSigns):
            dollarSignsText = dollarSignsText + "$"
        restaurantLabels.append(Label(root, text=dollarSignsText))
    except:
        restaurantLabels.append(Label(root, text=""))

    # creates photo
    photo_data = Restaurants[0]['photos']
    full_photo_url = photo_url + "maxwidth=400&maxheight=400&photo_reference=" + photo_data[0]['photo_reference'] + "&key=" + api_key
    response = requests.get(full_photo_url)
    img = Image.open(BytesIO(response.content))
    img = ImageTk.PhotoImage(img)
    image_label = tk.Label(image=img)
    image_label.image = img

    restaurantLabels.append(image_label)

    

    # creates Address text
    try: 
        restaurantLabels.append(Label(root, text=Restaurants[0]['formatted_address']))
    except:
        restaurantLabels.append(Label(root, text="Address Unavailable"))

    # creates star Rating text
    try:
        restaurantLabels.append(Label(root, text="Rating: " + str(Restaurants[0]['rating'])))
    except:
        restaurantLabels.append(Label(root, text="Rating: N/A"))



    # creates text showing number of remaining results
    restaurantLabels.append(Label(root, text=str(len(Restaurants)) + " Results"))

    # deletes current restaurant from array
    try:
        del Restaurants[0]
    except:
        pass

    rerenderTextBoxes()
    printLabels()
    displayYNButtons()

def displayYNButtons():
    yesButton = Button(root, text="Yes")
    yesButton.pack() # FIX FORMATTING LATER

    noButton = Button(root, text="No", command=createLabels)
    noButton.pack() # FIX FORMATTING LATER

def makeAPICall(cityLocation, restaurantType):
    # calls API, stores requests in 'req'
    req = requests.get(url + 'query=' + restaurantType + 'restaurants in ' + cityLocation + '&key=' + api_key)
    reqJSON = req.json() # converts req to json type

    return reqJSON['results']

def handleSubmit():
    global city, foodType, Restaurants # calls global variables

    # assigns proper inputs to 'city' and 'foodType' variables
    city = locationTextBox.get()
    foodType = typeFoodTextBox.get()

    Restaurants = makeAPICall(city, foodType)
    createLabels()

def rerenderTextBoxes():   
    locationLabel.pack() # FIX FORMATTING LATER
    locationTextBox.pack() # FIX FORMATTING LATER
    typeFoodLabel.pack() # FIX FORMATTING LATER
    typeFoodTextBox.pack() # FIX FORMATTING LATER
    submitButton.pack() # FIX FORMATTING LATER

# creating GUI
root = Tk()
root.title('Restaurant Finder')
root.geometry("600x600")

locationLabel = Label(root, text="Location:")
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
