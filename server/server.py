# Import necessary libraries and modules
from flask import Flask, request, jsonify, send_from_directory
import util  # A custom module that we assume contains utility functions for the app
import os
from flask_cors import CORS  # This helps to handle Cross-Origin Resource Sharing (CORS)

# Create a new Flask web application
app = Flask(__name__, static_folder='../client', static_url_path='', template_folder='../client')

# Allow CORS so that the frontend can communicate with this server from different origins
CORS(app)

# Define a route for the root URL ('/')
@app.route('/')
def home():
    # When someone accesses the root URL, serve the 'index.html' file from the client directory
    return send_from_directory(app.static_folder, 'index.html')

# Define a route to get location names based on a city
@app.route('/get_location_names/<city>', methods=['GET'])
def get_location_names(city):
    # Call a function from the 'util' module to get location names for the given city
    locations = util.get_location_names(city)
    
    # Create a JSON response containing the locations
    response = jsonify({
        'locations': locations
    })
    
    # Add a header to allow cross-origin requests (CORS)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Define a route to predict home prices based on various parameters
@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    # Get the data sent in the POST request as JSON
    data = request.get_json()
    
    # Extract the data from the JSON request
    city = data['city']
    area_sqft = float(data['area_sqft'])
    location = data['location']
    bedrooms = int(data['bedrooms'])
    bathrooms = int(data['bathrooms'])
    
    # Call a function from the 'util' module to get the estimated price based on the input data
    estimated_price = util.get_estimated_price(city, location, area_sqft, bedrooms, bathrooms)
    
    # Create a JSON response with the estimated price
    response = jsonify({
        'estimated_price': estimated_price
    })
    
    # Add a header to allow cross-origin requests (CORS)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Start the Flask web server when this script is executed directly
if __name__ == '__main__':
    print("Starting Python Flask Server For Home Price Prediction...")
    
    # Load any necessary saved artifacts or models (e.g., machine learning models)
    util.load_saved_artifacts()
    
    # Run the Flask app on all available IP addresses (0.0.0.0) and port 8000 in debug mode
    app.run(host='0.0.0.0', port=8000, debug=True)
