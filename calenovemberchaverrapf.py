import streamlit as st
from connections import connect_to_mongo
import calendar
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

def main():
    st.title("Soccer Player Data Management System")

    # Session state to store form data and admin status
    if "parent_name" not in st.session_state:
        st.session_state.parent_name = None
    if "player_name" not in st.session_state:
        st.session_state.player_name = None
    if "is_admin" not in st.session_state:
        st.session_state.is_admin = False  # Admin status to view submissions

    # Menu options for the parent data collection
    menu = ["Parent Info & Calendar", "Admin Login"]

    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Parent Info & Calendar":
        parent_info_and_calendar()

    elif choice == "Admin Login":
        admin_login()

    # If the user is logged in as admin, allow them to view submissions
    if st.session_state.is_admin:
        st.sidebar.subheader("Admin Options")
        if st.sidebar.button("View Submissions"):
            view_submissions()


def parent_info_and_calendar():
    st.subheader("Select Training Dates for November")

    # Define the microcycles with checkboxes
    st.markdown("### Microciclo #1 (Light Blue)")
    microcycle_1 = {
        "29 de octubre (martes)": st.checkbox("29 de octubre (martes)"),
        "30 de octubre (miércoles)": st.checkbox("30 de octubre (miércoles)")
    }

    st.markdown("### Microciclo #2 (Red)")
    microcycle_2 = {
        "4 de noviembre (lunes)": st.checkbox("4 de noviembre (lunes)"),
        "5 de noviembre (martes)": st.checkbox("5 de noviembre (martes)"),
        "7 de noviembre (jueves)": st.checkbox("7 de noviembre (jueves)"),
        "8 de noviembre (viernes)": st.checkbox("8 de noviembre (viernes)"),
        "9 de noviembre (sábado)": st.checkbox("9 de noviembre (sábado)")
    }

    st.markdown("### Microciclo #3 (Orange)")
    microcycle_3 = {
        "11 de noviembre (lunes)": st.checkbox("11 de noviembre (lunes)"),
        "12 de noviembre (martes)": st.checkbox("12 de noviembre (martes)"),
        "14 de noviembre (jueves)": st.checkbox("14 de noviembre (jueves)"),
        "15 de noviembre (viernes)": st.checkbox("15 de noviembre (viernes)"),
        "16 de noviembre (sábado)": st.checkbox("16 de noviembre (sábado)")
    }

    st.markdown("### Microciclo #4 (Purple)")
    microcycle_4 = {
        "18 de noviembre (lunes)": st.checkbox("18 de noviembre (lunes)"),
        "19 de noviembre (martes)": st.checkbox("19 de noviembre (martes)"),
        "21 de noviembre (jueves)": st.checkbox("21 de noviembre (jueves)"),
        "22 de noviembre (viernes)": st.checkbox("22 de noviembre (viernes)"),
        "23 de noviembre (sábado)": st.checkbox("23 de noviembre (sábado)")
    }

    st.markdown("### Microciclo #5 (Green)")
    microcycle_5 = {
        "25 de noviembre (lunes)": st.checkbox("25 de noviembre (lunes)"),
        "26 de noviembre (martes)": st.checkbox("26 de noviembre (martes)"),
        "28 de noviembre (jueves)": st.checkbox("28 de noviembre (jueves)"),
        "29 de noviembre (viernes)": st.checkbox("29 de noviembre (viernes)"),
        "30 de noviembre (sábado)": st.checkbox("30 de noviembre (sábado)")
    }

    # Display the custom calendar image
    st.image("https://raw.githubusercontent.com/xchmcr/calenovemberREPO/main/calendar.png", caption="November 2024 Training Calendar", use_column_width=True)

    # Collect parent and player data
    st.subheader("Enter Parent and Player Information")
    parent_name = st.text_input("Parent Name")
    player_name = st.text_input("Player Name")

    # Collect selected dates
    selected_dates = []
    for microcycle in [microcycle_1, microcycle_2, microcycle_3, microcycle_4, microcycle_5]:
        for date, selected in microcycle.items():
            if selected:
                selected_dates.append(date)

    if st.button("Submit"):
        if parent_name and player_name and selected_dates:
            db = connect_to_mongo()
            parents_collection = db["parents"]  # Collection to store parent/player data

            # Insert data into MongoDB
            new_entry = {
                "parent_name": parent_name,
                "player_name": player_name,
                "selected_dates": selected_dates
            }
            parents_collection.insert_one(new_entry)
            
            st.success(f"Data for {parent_name} and {player_name} with selected dates saved successfully!")
        else:
            st.error("Please fill in all fields and select at least one date.")


def view_submissions():
    st.subheader("Submitted Data")

    db = connect_to_mongo()
    parents_collection = db["parents"]

    # Fetch and display data from MongoDB
    submissions = parents_collection.find()

    if parents_collection.count_documents({}) > 0:
        for submission in submissions:
            st.write(f"**Parent:** {submission['parent_name']}, **Player:** {submission['player_name']}, **Selected Dates:** {', '.join(submission['selected_dates'])}")
    else:
        st.write("No data submitted yet.")


def admin_login():
    st.subheader("Admin Login")
    
    admin_password = st.text_input("Enter Admin Password", type="password")
    
    if st.button("Login"):
        # Simple password check
        if admin_password == "admin123":  # Change this to a secure password
            st.session_state.is_admin = True
            st.success("Admin access granted.")
        else:
            st.error("Incorrect password!")


if __name__ == "__main__":
    main()
