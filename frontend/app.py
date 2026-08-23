import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title("ExtraaLearn Customer Prediction")

# Section for online prediction
st.subheader("Online Prediction")

# Collect user input for the leads features
age= st.number_input("Age",min_value=0 , max_value = 100)
current_occupation = st.selectbox("current_occupation", ["Professional", "Unemployed", "Student"])
first_interaction = st.selectbox("first_interaction", ["Website", "Mobile App"])
profile_completed = st.selectbox("profile_completed", ["High", "Medium","Low"])
website_visits = st.number_input("Number of Website Visit",min_value=0 , max_value = 50)
time_spent_on_website = st.number_input("Time spent on a website",min_value = 0 , max_value = 2000 ) 
page_views_per_visit = st.number_input("Average pages visited per website",min_value = 0.000 , max_value = 5.000,format = "%.3f" ) 
last_activity = st.selectbox("Last Activity", ["Email Activity", "Phone Activity","Website Activity"])
print_media_type1 = st.selectbox("Print Media Type1", ["Yes", "No"])
print_media_type2 = st.selectbox("Print Media Type2", ["Yes", "No"])
digital_media = st.selectbox("Digital Media used for communication", ["Yes", "No"])
educational_channels = st.selectbox("Educational Channels", ["Yes", "No"])
referral = st.selectbox("Referral", ["Yes", "No"])

# Convert user input into a DataFrame
input_data = pd.DataFrame([{
'age' :age,
'current_occupation ' :current_occupation ,
'first_interaction ' :first_interaction ,
'profile_completed ' :profile_completed ,
'website_visits ' :website_visits ,
'time_spent_on_website ' :time_spent_on_website ,
'page_views_per_visit ' :page_views_per_visit ,
'last_activity ' :last_activity ,
'print_media_type1 ' :print_media_type1 ,
'print_media_type2 ' :print_media_type2 ,
'digital_media ' :digital_media ,
'educational_channels ' :educational_channels ,
'referral ' :referral 
}])

# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/customer", json=input_data.to_dict(orient='records')[0])  # Send data to Flask API
    if response.status_code == 200:
        prediction = response.json()['Predicted Customer conversion value']
        st.success(f"Predicted Customer conversion (1 = 'Successful Conversion' , 0 = 'Unsuccessful Conversion'): {prediction}")
    else:
        st.error("Unable to connect to the prediction API.")

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/customerbatch", files={"file": uploaded_file})  # Send file to Flask API
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)  # Display the predictions
        else:
            st.error("Unable to connect to the prediction API.")
