#my API KEY: AIzaSyDyiSclZPTIWJyVB2B1BSMWOs9Z6e6v1dM

# restaurantLabels[0] : Name of Restaurant OR Error Message if No More Available Restaurants
# restaurantLabels[1] : $$$ indicating Price Level
# restaurnatLabels[2] : Photo
# restaurnatLabels[3] : Address
# restaurantLabels[4] : Star Rating
# restaurantLabels[5] : Number of results 
  
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

# urls for API calls
url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
photo_url = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&maxheight=400&photo_reference="
api_key = 'AIzaSyAOkl_9l3DVkO2RtDEmp_F4mpUdDKm6AVc'


def printLabels():
    global restaurantLabels
    # Name
    restaurantLabels[0].config(font=("Courier Bold", 30))
    restaurantLabels[0].place(x=600, y=20)
    # $$$ Level
    restaurantLabels[0].config(justify='center')
    restaurantLabels[1].place(x=750, y=475)
    # Photo
    restaurantLabels[2].place(x=575, y=75)
    # Address
    restaurantLabels[3].config(font=("Courier", 10))
    restaurantLabels[3].place(x=525, y=425)
    # Num Results
    restaurantLabels[5].config(bg="#655cb5")
    restaurantLabels[5].place(x=420, y=575)
    

def addLabel(infoIn, ErrorMessage):
    global restaurantLabels

    try:
        restaurantLabels.append(Label(root, text=infoIn, justify="center"))
    except:
        restaurantLabels.append(Label(root, text=(ErrorMessage)))

def getListInfo(typeIn):
    try:
        infoOut=Restaurants[0][typeIn]
    except:
        return ""
    return infoOut


def createLabels():
    global city, foodType, Restaurants, restaurantLabels
    restaurantLabels = [] # erases restaurantLabels list

    for widget in root.winfo_children():
       widget.place_forget()
 
    # adds name of Restaurant
    addLabel(getListInfo('name'), "Sorry there are no " + foodType + " restaurants in " + city)
    
    # adds $$$ text
    dollarSignsText = ""
    try:
        for i in range(0, getListInfo('price_level')):
            dollarSignsText = dollarSignsText + "$"
    except:
        dollarSignsText = ""
    addLabel(dollarSignsText, "")

    # creates photo
    full_photo_url = photo_url + getListInfo('photos')[0]['photo_reference'] + "&key=" + api_key
    response = requests.get(full_photo_url)
    img = Image.open(BytesIO(response.content))

    resized_img = img.resize((350,350))
    
    resized_img = ImageTk.PhotoImage(resized_img)
    image_label = tk.Label(image=resized_img)
    image_label.image = resized_img
    restaurantLabels.append(image_label)

    # creates Address text
    addLabel(getListInfo('formatted_address'), "Address Unavailable")

    # creates star Rating text
    addLabel("Rating: " + str(getListInfo('rating')), "Rating: N/A")

    # creates text showing number of remaining results
    addLabel(str(len(Restaurants)) + " Results", "")

    rerenderTextBoxes()
    printLabels()
    displayNextButton()

def incrementRestaurant():
    global Restaurants
    Restaurants.append(Restaurants.pop(0))
    createLabels()

def unincrementRestaurant():
    global Restaurants
    Restaurants = Restaurants[-1:] + Restaurants[:-1] 
    createLabels()


def displayNextButton():
    prevButton = Button(root, text="Previous", command=(unincrementRestaurant))
    prevButton.place(x=690, y=500) 

    nextButton = Button(root, text="Next", command=(incrementRestaurant))
    nextButton.place(x=765, y=500)

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
    leftFrame.place(x=0, y=0) 

    locationTextBox.place(x=50, y=175) 
    typeFoodTextBox.place(x=50, y=275) 
    submitButton.place(x=250, y=400) 

# creating GUI
root = Tk()
root.title('Restaurant Finder')
root.geometry("1000x600")
root.resizable(False, False)

leftFrame = Frame(root, bg="#655cb5", width=500, height=600) # creates leftside purple UI color

locationTextBox = Entry(root, cursor="xterm white", width=30, font=("Bahnschrift SemiBold Condensed", 20), bg="#453d87", fg="white")
locationTextBox.insert(0, "Location") # sets default text

typeFoodTextBox = Entry(root, cursor="xterm white", width=30, font=("Bahnschrift SemiBold Condensed", 20), bg="#453d87", fg="white")
typeFoodTextBox.insert(0, "What type of food do you want") # sets default text

submitButton = Button(root, text="Submit", command=handleSubmit, bg="#453d87", fg ="white", font=("Helvetica", 10), height=1, width=10)
rerenderTextBoxes()


root.mainloop()
