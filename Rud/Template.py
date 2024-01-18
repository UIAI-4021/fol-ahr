import sys
import tkinter
import tkinter.messagebox
from tkintermapview import TkinterMapView
from pyswip import Prolog
import csv


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
        self.submit_button.grid(row=0, column=0, pady=(0, 10), padx=10, sticky="se")  # Placed within the same cell as text area

        # Lower part: Map Widget
        self.map_widget = TkinterMapView(self)
        self.map_widget.grid(row=1, column=0, sticky="nsew")

        self.marker_list = []  # Keeping track of markers
        self.marker_path = None

        self.unique_features_dict = None


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

    def check_connections(self, results):
        print('result2 ', results)
        locations = []
        for result in results:
            city  = result["City"]
            locations.append(city)
            # TODO 5: create the knowledgebase of the city and its connected destinations using Adjacency_matrix.csv



        return locations

    def process_text(self):
        """Extract locations from the text area and mark them on the map."""
        text = self.text_area.get("1.0", "end-1c")  # Get text from text area
        locations = {}
        locations = self.extract_locations(text)  # Extract locations (you may use a more complex method here)


        # TODO 4: create the query based on the extracted features of user desciption 
        ################################################################################################

        # Construct Prolog query based on extracted features
        if (len(locations["country"])>0):
            country = locations["country"]

        else:
            country = '_'

        if (len(locations["region"])>0):
            region = locations["region"]

        else:
            region = '_'

        if (len(locations["Climate"])>0):
            climate = locations["Climate"]

        else:
            climate = '_'

        if (len(locations["Budget"])>0):
             budget = locations["Budget"]

        else:
            budget = '_'

        if (len(locations["Activity"])>0):
             Activity = locations["Activity"]

        else:
            Activity = '_'    

        if (len(locations["Demographics"])>0):
             Demographics = locations["Demographics"]

        else:
            Demographics = '_'

        if (len(locations["Duration"])>0):
             Duration = locations["Duration"]

        else:
            Duration = '_'    


        if (len(locations["Cuisine"])>0):
             Cuisine = locations["Cuisine"]

        else:
            Cuisine = '_'

        if (len(locations["History"])>0):
             History = locations["History"]

        else:
            History = '_'    

        if (len(locations["Natural Wonder"])>0):
             NaturalWonder = locations["Natural Wonder"]

        else:
            NaturalWonder = '_'

        if (len(locations["Accommodation"])>0):
             Accommodation = locations["Accommodation"]

        else:
            Accommodation = '_'

        if (len(locations["Language"])>0):
             Language = locations["Language"]

        else:
            Language = '_'    

       
        #
        query = f"destination(City, {country}, {region}, {climate}, {budget}, {Activity}, {Demographics}, {Duration}, {Cuisine}, {History}, {NaturalWonder}, {Accommodation}, {Language})"
        results = list(prolog.query(query))
        print(results)
        #locations = self.check_connections(results)
        # TODO 6: if the number of destinations is less than 6 mark and connect them 
        ################################################################################################
        #print(locations)
        #locations = ['mexico_city','rome' ,'brasilia']
        #self.mark_locations(locations)

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
        ################################################################################################
        extracted_features =  {key: "" for key in self.unique_features_dict.keys()}
        #extracted_features = {key: value[0] if value and value[0] != '' else '' for key, value in self.unique_features_dict.items()}
        for column, features_set in self.unique_features_dict.items():
            column_features = [feature for feature in features_set if feature in text]
            if column_features:
                extracted_features[column] = column_features

        
        new_dict = {key: value[0] if value and value[0] != '' else '' for key, value in extracted_features.items()}
        # print(new_dict)
        return new_dict



    def start(self):
        self.mainloop()

# TODO 1: read destinations' descriptions from Destinations.csv and add them to the prolog knowledge base
################################################################################################
# STEP1: Define the knowledge base of illnesses and their symptoms


csv_file_path = "C:\\Users\\qcet\\Desktop\\New folder\\Destinations.csv"

# Open the CSV file and read its contents

prolog = Prolog()
prolog.retractall("destination(_, _, _, _, _, _, _, _, _, _, _, _, _)")

# Open the CSV file and read its contents
with open(csv_file_path, 'r') as csv_file:
    # Create a CSV reader object
    #csv_reader = csv.reader(csv_file)
    csv_reader = csv.reader(csv_file, delimiter=',')
    # Skip header if it exists
    next(csv_reader, None)
    
    # Iterate through each row in the CSV file
    for row in csv_reader:
         
        prolog_assertion = "destination('{}', '{}', '{}', {}, {}, {}, {}, {}, '{}', {}, '{}', {}, {})".format(
            row[0].strip().replace("'", ""),
            #row[0].strip(),
            row[1].strip().lower(),
            row[2].strip().lower(),
            row[3].strip().lower(),
            row[4].strip().lower(),
            row[5].strip().lower(),
            row[6].strip().lower(),
            row[7].strip().lower(),
            row[8].strip().lower(),
            row[9].strip().lower(),
            row[10].strip().lower(),
            row[11].strip().lower(),
            row[12].strip().lower()
        )
 
        prolog.assertz(prolog_assertion)
        # Print or use the Prolog assertion as needed
        #print(prolog_assertion)

#
# query = "destination(City, iran, _, _, low, _, _, _, _, _, _, _, _)"
# results = list(prolog.query(query))

# print(results)
# Print the retrieved facts



#prolog.assertz("destination('Tokyo', japan, 'East Asia', temperate, high, cultural, solo, long, asian, modern, mountains, luxury, japanese)")
#prolog.assertz("destination('Ottawa', canada, 'North America', cold, medium, adventure, family_friendly, medium, european, modern, forests, mid_range, english)")
#prolog.assertz("destination('Mexico City', mexico, 'North America', temperate, low, cultural, senior, short, latin_american, ancient, mountains, budget, spanish)")
#prolog.assertz("destination('Rome', italy, 'Southern Europe', temperate, high, cultural, solo, medium, european, ancient, beaches, luxury, italian)")
#prolog.assertz("destination('Brasilia', brazil, 'South America', tropical, low, adventure, family_friendly, long, latin_american, modern, beaches, budget, portuguese)")



# TODO 2: extract unique features from the Destinations.csv and save them in a dictionary
################################################################################################
with open(csv_file_path, 'r') as csv_file:
    # Create a CSV reader object with ',' as the delimiter
    csv_reader = csv.reader(csv_file, delimiter=',')
    
    # Read the header to get column names
    header = next(csv_reader, None)
    
    # Initialize a dictionary to store unique features for each column
    unique_features_dict = {column: set() for column in header[1:]}  # Exclude the first column
    
    # Iterate through each row in the CSV file
    # for row in csv_reader:
    #     # Iterate through each column and add the feature to the corresponding set in the dictionary
    #     for idx, column in enumerate(header[1:]):  # Exclude the first column
    #         unique_features_dict[column].add(row[idx + 1].strip())  # Skip the first column in the row

    for row in csv_reader:
        # Iterate through each column and add the feature to the corresponding set in the dictionary
        for idx, column in enumerate(header[1:]):  # Exclude the first column
            features = set(row[idx + 1].strip().lower().split(', '))  # Split multiple languages into a set
            unique_features_dict[column].update(features)  # Update the set for the current column

# print(unique_features_dict)

# Print or use the unique features dictionary as needed

#print(len(unique_features_dict.keys()))


if __name__ == "__main__":
    app = App()
    app.unique_features_dict = unique_features_dict
    
    app.start()
