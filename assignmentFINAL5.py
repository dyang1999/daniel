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
# end of given code

# permute initial keywords to identify special keywords with spaces in between ie. "mixed rice"
def permute(keywords):
    temp = keywords.split()
    length = len(temp)
    temp_list = []
    a = 0
    if length == 1:
        return temp_list
    else:
        while a < length:
            if a == length-1:
                return temp_list
            else:
                temp_list.append(temp[a] + " " + temp[a+1])
                a += 1

# function to add matched locations in the form canteen name - stall name to a empty set based on a choice (keyword)
# below function loops through the dictionary to extract the required and matching information
def locate_food(choice):
    location = set()
    for canteen, stall in canteen_stall_keywords.items():
        for stall_name, cuisine in stall.items():
            if choice in cuisine.lower():
                place = canteen + " - " + stall_name
                location.add(place)
    return location

# function takes in a list of lists containing the list of food places that matched with 1 specific keyword
# function intersects and outputs the common stalls in however many lists in (lists)
# address' properties and outputs a list of intended stalls

def intersection_lists(lists):
    return list(set.intersection(*map(set, lists)))

# function takes in a list of lists containing the list of food places that matched with 1 specific keyword
# function unions and output all non repeated unique stalls from however many lists in (lists)
# addresses 'or' properties and outputs a list of intended stalls

def union_lists(lists):
    return list(set.union(*map(set, lists)))

# Keyword-based Search Function - to be implemented
# def search_by_keyword(keywords)
# returns a list of food stall locations separated by ,
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
        return final_location

    elif len(keywords) == 1:
        final_location = list(locate_food(keywords[0]))
        return final_location

    elif "or" in keywords:
        final_location = []
        for x in keywords:
            if x == "or":
                continue
            else:
                location = locate_food(x)
                final_location.append(location)
        final_location = union_lists(final_location)
        return final_location


# Price-based Search Function - to be implemented
# Utilises search_by_keywords() to obtain the canteen and food stall keys which can be used to isolate the respective prices.
# The keys are looped through the dictionary and output in the format: canteen - stall name - price
# Strings are sorted in ascending order by isolating the price in the string
# The sorted locations are placed in a list

def search_by_price(keywords, max_price):
    inprice = []
    # if no such combinations of keywords available
    if search_by_keyword(keywords) == []:
        return inprice
    for x in search_by_keyword(keywords):
        x = x.split(" - ")
        if canteen_stall_prices[x[0]][x[1]] <= max_price:
            inprice.append(str(x[0]) + " - " + str(x[1]) + " - " + "S$ " + "%.2f" % (canteen_stall_prices[x[0]][x[1]]))
        else:
            continue
    inprice.sort(key=lambda x: float(x.split(" - ")[2].split("S$")[1]))

    if len(inprice) == 0:
        for x in search_by_keyword(keywords):
            x = x.split(" - ")
            inprice.append(str(x[0]) + " - " + str(x[1]) + " - " + "S$ " + "%.2f" % (canteen_stall_prices[x[0]][x[1]]))
        inprice.sort(key=lambda x: float(x.split(" - ")[2].split("S$")[1]))
        inprice = [inprice[0]] # if no options within price range run this block to return the nearest cost food option
    return inprice

# Location-based Search Function - to be implemented

# Pythagoras theorem to calculate distance.
def hypo(canteen, user):
    distance = ((canteen[0] - user[0]) ** 2 + (canteen[1] - user[1]) ** 2) ** 0.5
    return distance
# search_nearest_distance takes in 2 tuples containing locations of user A and B.
# the last parameter k dictates the number of outputs
# calls hypo() to obtain respective distances for user A and B to all canteens respectively.
# the average distance between users and the canteens are found and sorted based on ascending distance in a list

def search_nearest_canteens(userA_location, userB_location, k):
    distance = []
    for canteen in canteen_locations:
        canteen_loc = canteen_locations[canteen]
        distanceA = hypo(canteen_loc, userA_location)
        distanceB = hypo(canteen_loc, userB_location)
        average_distance = int((distanceA + distanceB) / 2)
        distance.append(canteen + " - " + str(average_distance) + "m")

    distance.sort(key=lambda x: x.split(" - ")[1])
    distance = distance[:k]

    return distance


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
            if keywords == '':
                print('Please input a value')
                break
            # special keywords management
            temp_list = permute(keywords)
            special_key=[]
            if len(temp_list)>0:
                for x in temp_list:
                    if x in cuisine_type:
                        special_key.append(x)
                    else:
                        continue
            # if 'or' not present in input, all spaces represent 'and'
            if " or " not in keywords:
                keywords = keywords.replace(" ", " and ")  # implement single space as an equivalent to "and" function
            keywords = keywords.lower().split()

            if len(special_key)>0:
                for x in special_key:
                    keywords.append(x)
                    x = x.split()
                    for a in x:
                        keywords.remove(a)
            # preliminary check if inputs by user are found in the dictionary
            for x in keywords:
                if x == "and" or x == "or":
                    continue
                if x not in cuisine_type:
                    print("No food stall found with input keyword. Please check input!")
                    exit()
            # ensures 'and' and 'or' are not found simultaneously in the input
            if len(keywords)>1:
                flag = True
                for x in set(keywords):
                    if x == "or":
                        flag = not(flag)
                    if x == "and":
                        flag = not(flag)
                if flag:
                    print("Please do not input 'and' together with 'or'!")
                    break

            # empty input error handing
            if keywords == []:
                print("No input found. Please try again.")

            # performs 'or' function
            # outputs locations based on the number of unique keywords matched
            if "or" in keywords:
                count = 1
                matches = {1: [], 2: [], 3: [], 4: [], 5: []}
                unique_stalls = search_by_keyword(keywords)
                print("Food stores found:", len(unique_stalls))
                for x in unique_stalls:
                    y = x.split(' - ')
                    stall_keywords = canteen_stall_keywords[y[0]][y[1]].lower()
                    stall_keywords = stall_keywords.split(', ')
                    stall_keywords = (set(stall_keywords)).intersection(set(keywords))
                    matches[len(stall_keywords)].append(x)
                while count<=5:
                    if matches[count] != []:
                        print("Food stalls that match", count ,"keywords:")
                        [print(x) for x in matches[count]]
                        count+=1
                    elif matches[count] == []:
                        count += 1
                    else:
                        break
            # Performs 'and' function and if there is only 1 keyword in the user input
            else:
                print("Food stores found:", len(search_by_keyword(keywords)))
                [print(x) for x in search_by_keyword(keywords)]

        elif option == 3:
            # price-based search
            print("Price-based Search")
            keywords = input("Enter Food Type:")
            if keywords == '':
                print('Please input a value')
                break
            # repeated prompting to ensure user inputs a positive integer, all other values, strings are rejected
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
            # special keywords management
            temp_list = permute(keywords)
            special_key = []
            if len(temp_list) > 0:
                for x in temp_list:
                    if x in cuisine_type:
                        special_key.append(x)
                    else:
                        continue
            # if 'or' not present in input, all spaces represent 'and'
            if " or " not in keywords:
                keywords = keywords.replace(" ", " and ")  # implement single space as an equivalent to "and" function
            keywords = keywords.lower().split()
            # ensures 'and' and 'or' are not found simultaneously in the input
            if len(keywords)>1:
                flag = True
                for x in set(keywords):
                    if x == "or":
                        flag = not(flag)
                    if x == "and":
                        flag = not(flag)
                if flag:
                    print("Please do not input 'and' together with 'or'!")
                    break

            if len(special_key) > 0:
                for x in special_key:
                    keywords.append(x)
                    x = x.split()
                    for a in x:
                        keywords.remove(a)
            # empty input handling and preliminary check if inputs by user are found in the dictionary
            if keywords == []:
                print("No input found. Please try again.")
            else:
                for x in keywords:
                    if x == "and" or x == "or":
                        continue
                    if x not in cuisine_type:
                        print("No food stall found with input keyword.")
                        break
                    # if no errors are found, perform search_by_price
                    else:
                        print("Food stores found:", len(search_by_price(keywords, max_price)))
                        if len(search_by_price(keywords, max_price)) == 0:
                            print("No stalls match input combinations.")
                        [print(a) for a in search_by_price(keywords, max_price)]
                        break

        elif option == 4:
            # location-based search
            print("Location-based Search")
            # call PyGame function to get two users' locations
            userA_location = get_user_location_interface()
            print("User A's location (x, y): ", userA_location)
            userB_location = get_user_location_interface()
            print("User B's location (x, y): ", userB_location)  # tuples

            # all illegal inputs, ie. empty string or '0'or symbols will result in the default search option of 1 output
            # all negative value inputs will re-prompt user to key in a positive integer
            try:
                number = int(input("Number of canteens:"))
                while True:
                    if number < 0:
                        number = int(input("Number of canteens(positive integer please):"))
                    else:
                        break
            except ValueError:
                number = 1
            if number == 0:
                number = 1
            nearest_canteens = search_nearest_canteens(userA_location, userB_location, number)
            print("Number of nearest canteens:", len(nearest_canteens))
            [print(x) for x in nearest_canteens]

        elif option == 5:
            # exit the program
            print("Exiting F&B Recommendation")
            loop = False


# unique keywords in the entire dictionary (runs at the start of the program)
# placed in a list
cuisine_type = []
for canteen, stall in canteen_stall_keywords.items():
    for stall_name, cuisine in stall.items():
        cuisine = cuisine.split(", ")
        for x in cuisine:
            x = x.lower()
            cuisine_type.append(x)
cuisine_type = list(set(cuisine_type))

main()
