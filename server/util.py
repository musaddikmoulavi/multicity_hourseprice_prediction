import pickle
import json
import numpy as np
import os

__models = {}
__data_columns = {}
__locations = {}

def get_estimated_price(city, location, area_sqft, bedrooms, bathrooms):
    try:
        loc_index = __data_columns[city].index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns[city]))
    x[0] = area_sqft
    x[1] = bathrooms
    x[2] = bedrooms
    if loc_index >= 0:
        x[loc_index] = 1
 

    return round(__models[city].predict([x])[0], 2)

def load_saved_artifacts():
    print("Loading saved artifacts...start")
    global __models
    global __data_columns
    global __locations

    artifacts_path = "./artifacts"
    for city in os.listdir(artifacts_path):
        city_path = os.path.join(artifacts_path, city)
        if os.path.isdir(city_path):
            with open(os.path.join(city_path, "columns.json"), "r") as f:
                __data_columns[city] = json.load(f)['data_columns']
                __locations[city] = __data_columns[city][3:]  # first 3 columns are area_sqft, bathroomsrooms, bedrooms
            with open(os.path.join(city_path, "model.pickle"), 'rb') as f:
                __models[city] = pickle.load(f)            
    print("Loading saved artifacts...done")

def get_location_names(city):
    return __locations.get(city, [])

def get_data_columns(city):
    return __data_columns.get(city, [])

if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names('bangalore'))
    # print('Hii', get_data_columns('bangalore'))
    # print(get_estimated_price('bangalore', '1st Phase JP Nagar', 1000, 3, 3))
    # print(get_estimated_price('bangalore', '1st Phase JP Nagar', 1000, 2, 2))
    # print(get_estimated_price('bangalore', 'Kalhalli', 1000, 2, 2)) # other location
    # print(get_estimated_price('bangalore', 'Ejipura', 1000, 2, 2))  # other location
