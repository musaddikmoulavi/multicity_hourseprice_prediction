import pickle
import json
import numpy as np
import os

# Dictionaries to store models, data columns, and location names
__models = {}
__data_columns = {}
__locations = {}

def get_estimated_price(city, location, area_sqft, bedrooms, bathrooms):
    """
    Estimating the price of a home based on input parameters.

    Parameters:
    - city: The city where the home is located.
    - location: Specific location or neighborhood within the city.
    - area_sqft: Area of the home in square feet.
    - bedrooms: Number of bedrooms in the home.
    - bathrooms: Number of bathrooms in the home.

    Returns:
    - The estimated price of the home rounded to 2 decimal places.
    """
    try:
        # Finding the index of the location in the data columns for the city
        loc_index = __data_columns[city].index(location.lower())
    except:
        # If the location is not found, set index to -1
        loc_index = -1

    # Creating a feature vector with zeros
    x = np.zeros(len(__data_columns[city]))
    
    # Setting the features in the vector
    x[0] = area_sqft
    x[1] = bathrooms
    x[2] = bedrooms
    
    # If the location was found, set the corresponding feature to 1
    if loc_index >= 0:
        x[loc_index] = 1
    
    # Using the model to predict the price based on the feature vector
    return round(__models[city].predict([x])[0], 2)

def load_saved_artifacts():
    """
    Load saved models and data columns from files.
    """
    print("Loading saved artifacts...start")
    global __models
    global __data_columns
    global __locations

    # Path to the directory where artifacts are stored
    artifacts_path = "./artifacts"
    
    # Looping through each city's folder in the artifacts directory
    for city in os.listdir(artifacts_path):
        city_path = os.path.join(artifacts_path, city)
        
        # Checking if the path is a directory
        if os.path.isdir(city_path):
            # Loading the data columns from JSON file
            with open(os.path.join(city_path, "columns.json"), "r") as f:
                __data_columns[city] = json.load(f)['data_columns']
                __locations[city] = __data_columns[city][3:]  # Get location names (columns after the first 3)
            
            # Load the model from pickle file
            with open(os.path.join(city_path, "model.pickle"), 'rb') as f:
                __models[city] = pickle.load(f)
    
    print("Loading saved artifacts...done")

def get_location_names(city):
    """
    Getting a list of location names for a given city.

    Parameters:
    - city: The city for which to retrieve location names.

    Returns:
    - A list of location names for the city.
    """
    return __locations.get(city, [])

def get_data_columns(city):
    """
    Getting the data columns used for the given city.

    Parameters:
    - city: The city for which to retrieve data columns.

    Returns:
    - A list of data columns used for the city.
    """
    return __data_columns.get(city, [])

# If this script is run directly (not imported as a module)
if __name__ == '__main__':
    # Load the saved models and data columns
    load_saved_artifacts()
    
    # Printing the location names for 'bangalore' as a test
    print(get_location_names('bangalore'))
    
