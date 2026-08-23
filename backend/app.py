# Import necessary libraries
import numpy as np
import joblib  # For loading the serialized model
import pandas as pd  # For data manipulation
from flask import Flask, request, jsonify  # For creating the Flask API

# Initialize the Flask application
customer_predictor_api = Flask("ExtraaLearn Customer Predictor")

# Load the trained machine learning model
model = saved_model

# Define a route for the home page (GET request)
@customer_predictor_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the ExtraaLearn Customer Prediction API!"

# Define an endpoint for single customer prediction (POST request)
@customer_predictor_api.post('/v1/customer')
def predict_customer_conversion():
    """
    This function handles POST requests to the '/v1/customer' endpoint.
    It expects a JSON payload containing extraalearn customer details and returns
    the predicted rental price as a JSON response.
    """
    # Get the JSON data from the request body
    extraalearn_data = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
        'age': extraalearn_data['age'],
        'current_occupation': extraalearn_data['current_occupation'],
        'first_interaction': extraalearn_data['first_interaction'],
        'profile_completed': extraalearn_data['profile_completed'],
        'website_visits': extraalearn_data['website_visits'],
        'time_spent_on_website': extraalearn_data['time_spent_on_website'],
        'page_views_per_visit': extraalearn_data['page_views_per_visit'],
        'last_activity': extraalearn_data['last_activity'],
        'print_media_type1': extraalearn_data['print_media_type1'],
        'print_media_type2': extraalearn_data['print_media_type2'],
        'digital_media': extraalearn_data['digital_media'],
        'educational_channels': extraalearn_data['educational_channels'],
        'referral' : extraalearn_data['referral']

    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction 
    predicted_customer_val = model.predict(input_data)[0]

   
    # Return the actual price
    return jsonify({'Predicted Customer conversion value': predicted_customer_val})


# Define an endpoint for batch prediction (POST request)
@customer_predictor_api.post('/v1/customerbatch')
def predict_customer_convesion_batch():
    """
    This function handles POST requests to the '/v1/customerbatch' endpoint.
    It expects a CSV file containing extraalearn potential customer details 
    and returns the predicted customer conversion chances as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all potential leads in the DataFrame 
    predicted_customer_val = model.predict(input_data).tolist()

    # Create a dictionary of predictions with property IDs as keys
    customer_ids = input_data['id'].tolist()  # Assuming 'id' is the customer ID column
    output_dict = dict(zip(customer_ids, predicted_customer_val))  

    # Return the predictions dictionary as a JSON response
    return output_dict

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    customer_predictor_api.run(debug=True)
