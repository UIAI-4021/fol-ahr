import sys
import tkinter
import tkinter.messagebox
from tkintermapview import TkinterMapView
from pyswip import Prolog
import csv


def checkValue(value):
    if len(value.split(" ")) > 1:
        value = value.replace(" ", "_")
    if value.count("-") > 0:
        # print(value)
        # input()
        value = value.replace("-", "_")
    return value.lower()


def readCsv(prolog):
    destinationFile = open("Destinations.csv", encoding="utf8")
    destinations = list(csv.reader(destinationFile))

    prolog.retractall("destination(_,_,_,_,_,_,_,_,_,_,_,_,_)")

    for i in range(1, len(destinations)):
        value = "destination('"
        my_destination = str(destinations[i][0])
        my_destination = my_destination.replace("'", "")
        value += checkValue(my_destination) + "','"
        value += checkValue(str(destinations[i][1])) + "','"
        value += checkValue(str(destinations[i][2])) + "','"
        value += checkValue(str(destinations[i][3])) + "','"
        value += checkValue(str(destinations[i][4])) + "','"
        value += checkValue(str(destinations[i][5])) + "','"
        value += checkValue(str(destinations[i][6])) + "','"
        value += checkValue(str(destinations[i][7])) + "','"
        value += checkValue(str(destinations[i][8])) + "','"
        value += checkValue(str(destinations[i][9])) + "','"
        value += checkValue(str(destinations[i][10])) + "','"
        value += checkValue(str(destinations[i][11])) + "','"
        value += checkValue(str(destinations[i][12])) + "')"
        prolog.assertz(value)

    return destinations


def getFeatures(destinations):
    mapValues = {
        "my_destination": set({}), "country": set({}), "region": set({}),
        "climate": set({}), "budget": set({}), "activity": set({}),
        "demographic": set({}), "duration": set({}), "cuisine": set({}),
        "history": set({}), "natural_wonder": set({}), "accommodation": set({}),
        "language": set({})
    }
    for i in range(1, len(destinations)):
        destinationKey = mapValues["my_destination"]
        destinationKey.add(checkValue(destinations[i][0]))
        destinationKey = mapValues["country"]
        destinationKey.add(checkValue(destinations[i][1]))
        destinationKey = mapValues["region"]
        destinationKey.add(checkValue(destinations[i][2]))
        destinationKey = mapValues["climate"]
        destinationKey.add(checkValue(destinations[i][3]))
        destinationKey = mapValues["budget"]
        destinationKey.add(checkValue(destinations[i][4]))
        destinationKey = mapValues["activity"]
        destinationKey.add(checkValue(destinations[i][5]))
        destinationKey = mapValues["demographic"]
        destinationKey.add(checkValue(destinations[i][6]))
        destinationKey = mapValues["duration"]
        destinationKey.add(checkValue(destinations[i][7]))
        destinationKey = mapValues["cuisine"]
        destinationKey.add(checkValue(destinations[i][8]))
        destinationKey = mapValues["history"]
        destinationKey.add(checkValue(destinations[i][9]))
        destinationKey = mapValues["natural_wonder"]
        destinationKey.add(checkValue(destinations[i][10]))
        destinationKey = mapValues["accommodation"]
        destinationKey.add(checkValue(destinations[i][11]))
        destinationKey = mapValues["language"]
        destinationKey.add(checkValue(destinations[i][12]))
    return mapValues


def checkLanguage(languagesList, language):
    for languages in languagesList:
        splitLanguage = languages.split(",")
        if language in splitLanguage:
            return True

    return False


def extractData(mapValues, text):
    text = text.replace(".", "")
    splitedText = text.split(" ")
    extractValues = ["" for _ in range(12)]
    for word in splitedText:
        word = word.lower()
        # print(word)
        if word in mapValues["country"]:
            extractValues[0] = word
        if word in mapValues["region"]:
            extractValues[1] = word
        if word in mapValues["climate"]:
            extractValues[2] = word
        if word in mapValues["budget"]:
            extractValues[3] = word
        if word in mapValues["activity"]:
            extractValues[4] = word
        if word in mapValues["demographic"]:
            extractValues[5] = word
        if word in mapValues["duration"]:
            extractValues[6] = word
        if word in mapValues["cuisine"]:
            extractValues[7] = word
        if word in mapValues["history"]:
            extractValues[8] = word
        if word in mapValues["natural_wonder"]:
            extractValues[9] = word
        if word in mapValues["accommodation"]:
            extractValues[10] = word
        if checkLanguage(list(mapValues["language"]), word):
            extractValues[11] = word
    return extractValues


def connectCities(connectionMatrix, prolog):
    cities = connectionMatrix[0]
    prolog.retractall("connected(_,_)")
    prolog.retractall("check_first_connection(_,_)")
    prolog.retractall("check_second_connection(_,_)")

    for i in range(1, len(connectionMatrix)):
        cityI = str(cities[i])
        cityI = cityI.replace("'", "")
        for j in range(i + 1, len(connectionMatrix[i])):
            cityJ = str(cities[j])
            cityJ = cityJ.replace("'", "")
            if connectionMatrix[i][j] == "1" or connectionMatrix[j][i] == "1":
                prolog.assertz("connected('" + checkValue(cityI) + "','" + checkValue(cityJ) + "')")
                prolog.assertz("connected('" + checkValue(cityJ) + "','" + checkValue(cityI) + "')")


def getConnectionList(connections, key="X"):
    connectionSet = set()
    for connection in connections:
        connectionSet.add(connection[key])
    return connectionSet


def getConnections(city, prolog):
    firstConnections = list(prolog.query("check_first_connection('" + city + "',X)"))
    secondConnections = list(prolog.query("check_second_connection('" + city + "',X)"))

    return getConnectionList(firstConnections), getConnectionList(secondConnections)


def getSecondConnectedCity(firstCityConnections, city2):
    secondCityConnections = list(prolog.query("check_first_connection('" + city2 + "',X)"))
    secondCityConnections = getConnectionList(secondCityConnections)

    for city in firstCityConnections:
        if city in secondCityConnections:
            return city


def getSimilarCities(cityConnection, key, cities):
    firstConnection = set(cityConnection[key][0])
    secondConnection = set(cityConnection[key][1])

    connections = firstConnection | secondConnection
    return connections & cities


def checkRepeatTour(tours, value):
    value = set(value)
    for tour in tours:
        if set(tour) == value:
            return True
    return False


def search(baseCity, city, desCity, value, visited, cityConnections, cityValues, tours, complete):
    if city not in cityConnections[city][0]:
        value.append(getSecondConnectedCity(cityConnections[desCity][0], desCity))
    value.append(desCity)
    cities = list(cityValues[desCity])
    temp = value
    for city in cities:
        if city not in visited:
            visited.add(city)
            similarCities = cityValues[city]
            similarBaseCity = cityValues[baseCity]

            similarity = similarCities & similarBaseCity
            similarity = similarity.difference(visited)

            if len(similarity) > 0:
                search(baseCity, desCity, city, value, visited, cityConnections, cityValues, tours, False)
                return
            elif complete:
                if city not in cityConnections[desCity][0]:
                    temp.append(getSecondConnectedCity(cityConnections[desCity][0], city))
                temp.append(city)
                if not checkRepeatTour(tours, temp):
                    tours.append(temp)

    tours.append(value)


def checkCitiesSimilarity(results, cityConnection):
    for city in results:
        firstConnection, secondConnection = getConnections(city, prolog)
        cityConnection[city] = (firstConnection, secondConnection)

    cityValues = dict()
    cities = set(results)

    selectedCities = cityConnection.keys()

    check = False
    for key in selectedCities:
        temp = getSimilarCities(cityConnection, key, cities)
        if len(temp) > 0:
            check = True
        cityValues[key] = temp

    if not check:
        return None

    tours = []
    for key, value in cityValues.items():
        temp = [key]
        for city in value:
            visited = {key, city}
            values = [key]
            if city in cityConnection[key][1]:
                secondCity = getSecondConnectedCity(cityConnection[key][0], city)
                temp.append(secondCity)
                # values.append(secondCity)
            search(key, key, city, values, visited, cityConnection, cityValues, tours, True)
            temp.append(city)
            tours.append(temp)

    return tours


def getQuery(locations, prolog):
    check = set()
    query = "destination(City,"
    for i in range(0, len(locations)):
        if locations[i] != "":
            temp = query
            temp += locations[i] + ","
            for j in range(i + 1, len(locations)):
                temp += "_"
                if j != len(locations) - 1:
                    temp += ","
                else:
                    temp += ")"
            if i == len(locations) - 1:
                temp += ")"

            featuresCities = list(prolog.query(temp))
            check = check | set(getConnectionList(featuresCities, "City"))
        query += "_"
        if i != len(locations) - 1:
            query += ","
        else:
            query += ")"
    return check


def checkDifferentQueries(locations, cityConnection, city, prolog):
    check = []
    query = "destination(City,"
    for i in range(0, len(locations)):
        if locations[i] != "":
            query += locations[i]
            temp = query + ","
            for j in range(i + 1, len(locations)):
                temp += "_"
                if j != len(locations) - 1:
                    temp += ","
                else:
                    temp += ")"
            if i == len(locations) - 1:
                temp += ")"

            featuresCities = list(prolog.query(temp))
            similarCities = getSimilarCities(cityConnection, city,
                                             set(getConnectionList(featuresCities, "City")))
            check.append(similarCities)
        else:
            query += "_"
        if i != len(locations) - 1:
            query += ","
        else:
            query += ")"
    return check


def getApproximateCities(cityNames, locations, prolog, cityConnection):
    cityValues = dict()
    check = getQuery(locations, prolog)
    for city in cityNames:
        cityValues[city] = len(getSimilarCities(cityConnection, city, check))
    cityValues = dict(sorted(cityValues.items(), key=lambda item: item[1], reverse=True))

    selectedCity = list(cityValues.keys())[0]
    tour = [selectedCity]

    check = checkDifferentQueries(locations, cityConnection, selectedCity, prolog)
    check = check[::-1]
    for values in check:
        counter = 5 - len(tour)
        for city in values:
            if city not in tour:
                tour.append(city)
                counter -= 1
            if counter == 0:
                break
        if len(tour) == 5:
            break

    return tour


def getBestTour(tours, cities):
    max = -1
    selectedTour = 0
    cities = set(cities)
    for tour in tours:
        size = len(set(tour) & cities)
        if size > max:
            max = size
            selectedTour = tour
    return selectedTour


class App(tkinter.Tk):
    APP_NAME = "map_view_demo.py"
    WIDTH = 800
    HEIGHT = 750  # This is now the initial size, not fixed.

    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)

        self.title(self.APP_NAME)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        # Configure the grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Text area and submit button combined row
        self.grid_rowconfigure(1, weight=4)  # Map row

        # Upper part: Text Area and Submit Button
        self.text_area = tkinter.Text(self, height=5)  # Reduced height for text area
        self.text_area.grid(row=0, column=0, pady=(10, 0), padx=10, sticky="nsew")

        self.submit_button = tkinter.Button(self, text="Submit", command=self.process_text)
        self.submit_button.grid(row=0, column=0, pady=(0, 10), padx=10,
                                sticky="se")  # Placed within the same cell as text area

        # Lower part: Map Widget
        self.map_widget = TkinterMapView(self)
        self.map_widget.grid(row=1, column=0, sticky="nsew")

        self.marker_list = []  # Keeping track of markers
        self.marker_path = None

    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)

        self.title(self.APP_NAME)
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        # Configure the grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Text area can expand/contract.
        self.grid_rowconfigure(1, weight=0)  # Submit button row; doesn't need to expand.
        self.grid_rowconfigure(2, weight=3)  # Map gets the most space.

        # Upper part: Text Area and Submit Button
        self.text_area = tkinter.Text(self)
        self.text_area.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")

        self.submit_button = tkinter.Button(self, text="Submit", command=self.process_text)
        self.submit_button.grid(row=1, column=0, pady=10, sticky="ew")

        # Lower part: Map Widget
        self.map_widget = TkinterMapView(self)
        self.map_widget.grid(row=2, column=0, sticky="nsew")

        self.marker_list = []  # Keeping track of markers

    def check_connections(self, results, text):
        matrixFile = open("Adjacency_matrix.csv", encoding="utf8")
        matrixConnection = list(csv.reader(matrixFile))
        print('result2 ', results)

        connectCities(matrixConnection, prolog)
        prolog.assertz("check_first_connection(X,Y) :- connected(X,Y)")
        prolog.assertz("check_second_connection(X,Y) :- connected(X,Z),connected(Z,Y) , X\=Y")

        temp = []
        for result in results:
            temp.append(result['City'])
        results = temp

        cityConnection = dict()
        tours = checkCitiesSimilarity(results, cityConnection)
        if tours is None:
            locations = getApproximateCities(results, text, prolog, cityConnection)
            pass
        else:
            locations = getBestTour(tours, results)

        return locations

        # TODO 5: create the knowledgebase of the city and its connected destinations using Adjacency_matrix.csv

    def process_text(self):
        """Extract locations from the text area and mark them on the map."""
        text = self.text_area.get("1.0", "end-1c")  # Get text from text area
        locations = self.extract_locations(text)  # Extract locations (you may use a more complex method here)

        # TODO 4: create the query based on the extracted features of user desciption
        query = "destination(City,"
        for i in range(0, len(locations)):
            if locations[i] != "":
                query += locations[i]
            else:
                query += "_"
            if i != len(locations) - 1:
                query += ","
            else:
                query += ")"
        print(query)
        ################################################################################################
        #
        results = list(prolog.query(query))
        if len(results) > 5:
            print("Enter more features about tour that you want to go!!")
            locations = []
        elif len(results) != 0:
            locations = self.check_connections(results, locations)
        else:
            locations = []
        # TODO 6: if the number of destinations is less than 6 mark and connect them 
        ################################################################################################
        print(locations)
        # locations = ['mexico_city', 'rome', 'brasilia']
        self.mark_locations(locations)

    def mark_locations(self, locations):
        """Mark extracted locations on the map."""
        for address in locations:
            marker = self.map_widget.set_address(address, marker=True)
            if marker:
                self.marker_list.append(marker)
        self.connect_marker()
        self.map_widget.set_zoom(1)  # Adjust as necessary, 1 is usually the most zoomed out

    def connect_marker(self):
        print(self.marker_list)
        position_list = []

        for marker in self.marker_list:
            position_list.append(marker.position)

        if hasattr(self, 'marker_path') and self.marker_path is not None:
            self.map_widget.delete(self.marker_path)

        if len(position_list) > 0:
            self.marker_path = self.map_widget.set_path(position_list)

    def extract_locations(self, text):
        """Extract locations from text. A placeholder for more complex logic."""
        # Placeholder: Assuming each line in the text contains a single location name
        # TODO 3: extract key features from user's description of destinations
        ###############################################################################################
        return extractData(features, text)

        # return [line.strip() for line in text.split('\n') if line.strip()]

    def start(self):
        self.mainloop()


# TODO 1: read destinations' descriptions from Destinations.csv and add them to the prolog knowledge base
################################################################################################
# STEP1: Define the knowledge base of illnesses and their symptoms

prolog = Prolog()
destinations = readCsv(prolog)
features = getFeatures(destinations)

# TODO 2: extract unique features from the Destinations.csv and save them in a dictionary
################################################################################################


if __name__ == "__main__":
    app = App()
    app.start()
