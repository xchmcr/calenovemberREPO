from pymongo import MongoClient
import streamlit as st

# Define the function to connect to MongoDB
def connect_to_mongo():
    # MongoDB connection URI
    uri = "mongodb+srv://xchmcr:Waffletea27@clustertest01.dc3gd.mongodb.net/"

    try:
        # Connect to MongoDB
        client = MongoClient(uri)
        db = client["fridaydatabase"]  # Replace with your database name
        return db
    except Exception as e:
        st.error(f"Error connecting to MongoDB: {e}")
        return None
