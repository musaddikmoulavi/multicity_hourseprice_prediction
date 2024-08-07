# import pickle
# import json
# import numpy as np
# import os
# # from sklearn.exceptions import InconsistentVersionWarning
# import warnings

# __models = {}
# __data_columns = {}
# __locations = {}

# def get_estimated_price(city, location, area_sqft, bedrooms, bathrooms):
#     try:
#         loc_index = __data_columns[city].index(location.lower())
#     except ValueError:
#         loc_index = -1

#     x = np.zeros(len(__data_columns[city]))
#     x[0] = area_sqft
#     x[1] = bathrooms
#     x[2] = bedrooms
#     if loc_index >= 0:
#         x[loc_index] = 1

#     return round(__models[city].predict([x])[0], 2)

# def load_saved_artifacts():
#     print("Loading saved artifacts...start")
#     global __models
#     global __data_columns
#     global __locations

#     artifacts_path = "./artifacts"
#     for city in os.listdir(artifacts_path):
#         city_path = os.path.join(artifacts_path, city)
#         if os.path.isdir(city_path):
#             with open(os.path.join(city_path, "columns.json"), "r") as f:
#                 __data_columns[city] = json.load(f)['data_columns']
#                 __locations[city] = __data_columns[city][3:]  # first 3 columns are area_sqft, bathroomsrooms, bedrooms

#             with warnings.catch_warnings():
#                 warnings.simplefilter("ignore", category=InconsistentVersionWarning)
#                 with open(os.path.join(city_path, "model.pickle"), 'rb') as f:
#                     __models[city] = pickle.load(f)
#     print("Loading saved artifacts...done")

# def get_location_names(city):
#     return __locations.get(city, [])

# def get_data_columns(city):
#     return __data_columns.get(city, [])

# if __name__ == '__main__':
#     load_saved_artifacts()



# server.py

from flask import Flask, request, jsonify, send_from_directory
import util
import os
from flask_cors import CORS

app = Flask(__name__, static_folder='/client', static_url_path='', template_folder='/client')
CORS(app)

@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/get_location_names/<city>', methods=['GET'])
def get_location_names(city):
    response = jsonify({
        'locations': util.get_location_names(city)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    data = request.get_json()
    city = data['city']
    area_sqft = float(data['area_sqft'])
    location = data['location']
    bedrooms = int(data['bedrooms'])
    bathrooms = int(data['bathrooms'])

    response = jsonify({
        'estimated_price': util.get_estimated_price(city, location, area_sqft, bedrooms, bathrooms)
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    app.run(host='0.0.0.0', port=8000, debug=True)







# from flask import Flask, request, jsonify, send_from_directory
# import util
# from flask_cors import CORS

# app = Flask(__name__, static_folder='../client', static_url_path='', template_folder='../client')

# # app = Flask(__name__)
# CORS(app)

# @app.route('/')
# def home():
#     return send_from_directory(app.static_folder, 'index.html')


# @app.route('/get_location_names/<city>', methods=['GET'])
# def get_location_names(city):
#     response = jsonify({
#         'locations': util.get_location_names(city)
#     })
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     return response

# @app.route('/predict_home_price', methods=['POST'])
# def predict_home_price():
#     data = request.get_json()
#     city = data['city']
#     area_sqft = float(data['area_sqft'])
#     location = data['location']
#     bedrooms = int(data['bedrooms'])
#     bathrooms = int(data['bathrooms'])

#     response = jsonify({
#         'estimated_price': util.get_estimated_price(city, location, area_sqft, bedrooms, bathrooms)
#     })
#     print(data)
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     return response


# if __name__ == '__main__':
#     print("Starting Python Flask Server For Home Price Prediction...")
#     util.load_saved_artifacts()
#     # app.run(host='0.0.0.0')
#     app.run()    

# if __name__ == '__main__':
#     print("Starting Python Flask Server For Home Price Prediction...")
#     util.load_saved_artifacts()
#     app.run(debug=True)



# # trial
# from flask import Flask, request, jsonify
# import util

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return "Welcome to the Home Price Prediction API"

# @app.route('/get_location_names/<city>', methods=['GET'])
# def get_location_names(city):
#     response = jsonify({
#         'locations': util.get_location_names(city)
#     })
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     return response

# @app.route('/predict_home_price/<city>', methods=['POST'])
# def predict_home_price(city):
#     total_sqft = float(request.form['total_sqft'])
#     location = request.form['location']
#     bhk = int(request.form['bhk'])
#     bath = int(request.form['bath'])

#     response = jsonify({
#         'estimated_price': util.get_estimated_price(city, location, total_sqft, bhk, bath)
#     })
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     return response


