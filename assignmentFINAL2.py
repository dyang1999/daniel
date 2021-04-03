import pygame
from PIL import Image
import time
import pandas as pd


# load dataset for keyword dictionary - provided
def load_stall_keywords(data_location="canteens.xlsx"):
    # get list of canteens and stalls
    canteen_data = pd.read_excel(data_location)
    canteens = canteen_data['Canteen'].unique()
    canteens = sorted(canteens, key=str.lower)

    stalls = canteen_data['Stall'].unique()
    stalls = sorted(stalls, key=str.lower)

    keywords = {}
    for canteen in canteens:
        keywords[canteen] = {}

    copy = canteen_data.copy()
    copy.drop_duplicates(subset="Stall", inplace=True)
    stall_keywords_intermediate = copy.set_index('Stall')['Keywords'].to_dict()
    stall_canteen_intermediate = copy.set_index('Stall')['Canteen'].to_dict()

    for stall in stalls:
        stall_keywords = stall_keywords_intermediate[stall]
        stall_canteen = stall_canteen_intermediate[stall]
        keywords[stall_canteen][stall] = stall_keywords

    return keywords


# load dataset for price dictionary - provided
def load_stall_prices(data_location="canteens.xlsx"):
    # get list of canteens and stalls
    canteen_data = pd.read_excel(data_location)
    canteens = canteen_data['Canteen'].unique()
    canteens = sorted(canteens, key=str.lower)

    stalls = canteen_data['Stall'].unique()
    stalls = sorted(stalls, key=str.lower)

    prices = {}
    for canteen in canteens:
        prices[canteen] = {}

    copy = canteen_data.copy()
    copy.drop_duplicates(subset="Stall", inplace=True)
    stall_prices_intermediate = copy.set_index('Stall')['Price'].to_dict()
    stall_canteen_intermediate = copy.set_index('Stall')['Canteen'].to_dict()

    for stall in stalls:
        stall_price = stall_prices_intermediate[stall]
        stall_canteen = stall_canteen_intermediate[stall]
        prices[stall_canteen][stall] = stall_price

    return prices


# load dataset for location dictionary - provided
def load_canteen_location(data_location="canteens.xlsx"):
    # get list of canteens
    canteen_data = pd.read_excel(data_location)
    canteens = canteen_data['Canteen'].unique()
    canteens = sorted(canteens, key=str.lower)

    # get dictionary of {canteen:[x,y],}
    canteen_locations = {}
    for canteen in canteens:
        copy = canteen_data.copy()
        copy.drop_duplicates(subset="Canteen", inplace=True)
        canteen_locations_intermediate = copy.set_index('Canteen')['Location'].to_dict()
    for canteen in canteens:
        canteen_locations[canteen] = [int(canteen_locations_intermediate[canteen].split(',')[0]),
                                      int(canteen_locations_intermediate[canteen].split(',')[1])]

    return canteen_locations


# get user's location with the use of PyGame - provided
def get_user_location_interface():
    # get image dimensions
    image_location = 'NTUcampus.jpg'
    pin_location = 'pin.png'
    screen_title = "NTU Map"
    image = Image.open(image_location)
    image_width_original, image_height_original = image.size
    scaled_width = int(image_width_original)
    scaled_height = int(image_height_original)
    pinIm = pygame.image.load(pin_location)
    pinIm_scaled = pygame.transform.scale(pinIm, (60, 60))
    # initialize pygame
    pygame.init()
    # set screen height and width to that of the image
    screen = pygame.display.set_mode([scaled_width, scaled_height])
    # set title of screen
    pygame.display.set_caption(screen_title)
    # read image file and rescale it to the window size
    screenIm = pygame.image.load(image_location)

    # add the image over the screen object
    screen.blit(screenIm, (0, 0))
    # will update the contents of the entire display window
    pygame.display.flip()

    # loop for the whole interface remain active
    while True:
        # checking if input detected
        pygame.event.pump()
        event = pygame.event.wait()
        # closing the window
        if event.type == pygame.QUIT:
            pygame.display.quit()
            mouseX_scaled = None
            mouseY_scaled = None
            break
        # resizing the window
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(
                event.dict['size'], pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
            screen.blit(pygame.transform.scale(screenIm, event.dict['size']), (0, 0))
            scaled_height = event.dict['h']
            scaled_width = event.dict['w']
            pygame.display.flip()
        # getting coordinate
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # get outputs of Mouseclick event handler
            (mouseX, mouseY) = pygame.mouse.get_pos()
            # paste pin on correct position
            screen.blit(pinIm_scaled, (mouseX - 25, mouseY - 45))
            pygame.display.flip()
            # return coordinates to original scale
            mouseX_scaled = int(mouseX * 1281 / scaled_width)
            mouseY_scaled = int(mouseY * 1550 / scaled_height)
            # delay to prevent message box from dropping down
            time.sleep(0.2)
            break

    pygame.quit()
    pygame.init()
    return mouseX_scaled, mouseY_scaled


# function to add locations to a empty set based on a choice (keyword)
def locate_food(choice):
    location = set()
    for canteen, stall in canteen_stall_keywords.items():  # in will return western options if west is entered
        for stall_name, cuisine in stall.items():
            if choice in cuisine.lower():
                place = canteen + " - " + stall_name
                location.add(place)
    return location


def intersection_lists(result_lists):
    return list(set.intersection(*map(set, result_lists)))


def union_lists(result_lists):
    return list(set.union(*map(set, result_lists)))


# Keyword-based Search Function - to be implemented
# def search_by_keyword(keywords)
def search_by_keyword(keywords):
    if "and" in keywords:
        final_location = []
        for x in keywords:
            if x == "and":
                continue
            else:
                location = locate_food(x)
                final_location.append(location)
        final_location = intersection_lists(final_location)

    elif len(keywords) == 1:
        final_location = list(locate_food(keywords[0]))

    elif "or" in keywords:
        final_location = []
        for x in keywords:
            if x == "or":
                continue
            else:
                location = locate_food(x)
                final_location.append(location)
        final_location = union_lists(final_location)

    else:
        print("Please ensure and/or is not placed in the first or last term and ensure that you have keyed in your\
        choices in a  grammatically correctly manner")

    for x in keywords:
        if x == "rice" and ("Shan Shan Chinese" or "88 Cai Fan" in final_location):
            final_location.remove("Food Court 11 - 88 Cai Fan")
            final_location.remove("North Hill Food Court - Shan Shan Chinese")
    return final_location


# Price-based Search Function - to be implemented
def search_by_price(keywords, max_price):
    inprice = []
    for x in search_by_keyword(keywords):
        x = x.split(" - ")
        if canteen_stall_prices[x[0]][x[1]] <= max_price:
            inprice.append(str(x[0]) + " - " + str(x[1]) + " - " + "S$" + "%.2f" % (canteen_stall_prices[x[0]][x[1]]))
            inprice.sort(key=lambda x: x.split(" - ")[2])
        else:
            continue
    if len(inprice) == 0:
        inprice.append(str(x[0]) + " - " + str(x[1]) + " - " + "%.2f" % (canteen_stall_prices[x[0]][x[1]]))
        inprice.sort(key=lambda x: x.split(" - ")[2])
        inprice = [inprice[0]]  # if no options within price range run this block to return the nearest cost food option
    return inprice

def hypo(canteen,user):
    distance = ((canteen[0]-user[0])**2+(canteen[1]-user[1])**2)**0.5
    return distance
# Location-based Search Function - to be implemented

def search_nearest_canteens(userA_location,userB_location, k):
    distance = []
    for canteen in canteen_locations:
        canteen_loc = canteen_locations[canteen]
        distanceA = hypo(canteen_loc, userA_location)
        distanceB = hypo(canteen_loc, userB_location)
        average_distance = int((distanceA+distanceB)/2)
        distance.append(canteen + " - " + str(average_distance) + "m")

    distance.sort(key=lambda x: x.split(" - ")[1])
    distance = distance[:k]

    return distance


# Any additional function to assist search criteria

# Main Python Program Template
# dictionary data structures
canteen_stall_keywords = load_stall_keywords("canteens.xlsx")
canteen_stall_prices = load_stall_prices("canteens.xlsx")
canteen_locations = load_canteen_location("canteens.xlsx")


# main program template - provided
def main():
    loop = True

    while loop:
        print("=======================")
        print("F&B Recommendation Menu")
        print("1 -- Display Data")
        print("2 -- Keyword-based Search")
        print("3 -- Price-based Search")
        print("4 -- Location-based Search")
        print("5 -- Exit Program")
        print("=======================")
        option = int(input("Enter option [1-5]: "))

        if option == 1:
            # print provided dictionary data structures
            print("1 -- Display Data")
            print("Keyword Dictionary: ", canteen_stall_keywords)
            print("Price Dictionary: ", canteen_stall_prices)
            print("Location Dictionary: ", canteen_locations)

        elif option == 2:
            # keyword-based search
            print("Keyword-based Search")
            keywords = input("Enter Food Type:")
            if "or" not in keywords:
                if "and" not in keywords:
                    keywords = keywords.replace(" ", " and ")  # implement single space as an equivalent to "and" function
            keywords = keywords.lower().split()
            if keywords == []:
                print("No input found. Please try again.")
            for x in keywords:
                if x == "and" or x == "or":
                    continue
                if x not in cuisine_type:
                    print("No food stall found with input keyword. Please check input!")
                    break
                else:
                    # call keyword-based search function
                    print("Food stores found:", len(search_by_keyword(keywords)))
                    [print(x) for x in search_by_keyword(keywords)]
                    break

        elif option == 3:
            # price-based search
            print("Price-based Search")
            keywords = input("Enter Food Type:")
            while True:
                try:
                    max_price = float(input("Enter maximum meal price:"))
                except ValueError:
                    print("Please enter a number!")
                else:
                    if max_price < 0:
                        print("Meal price cannot be a negative number. Please try again.")
                    else:
                        break
            if "or" not in keywords:
                if "and" not in keywords:
                    keywords = keywords.replace(" ", " and ")  # implement single space as an equivalent to "and" function
            keywords = keywords.lower().split()
            if keywords == []:
                print("No input found. Please try again.")
            else:
                for x in keywords:
                    if x == "and" or x == "or":
                        continue
                    if x not in cuisine_type:
                        print("No food stall found with input keyword.")
                        break
                    else:
                        print("Food stores found:", len(search_by_price(keywords, max_price)))
                        [print(a) for a in search_by_price(keywords, max_price)]
                        break

            # call price-based search function
            # search_by_price(keywords, max_price)
        elif option == 4:
            # location-based search
            print("Location-based Search")
            # call PyGame function to get two users' locations
            userA_location = get_user_location_interface()
            print("User A's location (x, y): ", userA_location)
            userB_location = get_user_location_interface()
            print("User B's location (x, y): ", userB_location)  # tuples
            try:
                number = int(input("Number of canteens:"))
            except ValueError:
                number = 1
            while True:
                if number < 0:
                    number = int(input("Number of canteens:"))
                else:
                    break
            if number == 0 or number == " ":
                number = 1
            nearest_canteens = search_nearest_canteens(userA_location, userB_location, number)
            [print(x) for x in nearest_canteens]

        elif option == 5:
            # exit the program
            print("Exiting F&B Recommendation")
            loop = False


# unique cuisines in the entire dictionary (runs at the start of the program)
cuisine_type = []
for canteen, stall in canteen_stall_keywords.items():
    for stall_name, cuisine in stall.items():
        cuisine = cuisine.split(", ")
        for x in cuisine:
            x = x.lower()
            cuisine_type.append(x)
cuisine_type = list(set(cuisine_type))

main()
