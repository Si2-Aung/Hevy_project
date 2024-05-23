import streamlit as st
import pandas as pd
import calendar

# Function to load and process the CSV file
def load_data(file):
    workout_data = pd.read_csv(file)
    workout_data['start_time'] = pd.to_datetime(workout_data['start_time'], format="%d %b %Y, %H:%M", dayfirst=True)
    return workout_data

# Function to calculate the month with the most workouts
def calculate_month_with_most_workouts(workout_data):
    workout_data['workout_month'] = workout_data['start_time'].dt.to_period('M')
    workouts_per_month = workout_data['workout_month'].value_counts().sort_index()
    most_workouts_month = workouts_per_month.idxmax()
    most_workouts_count = workouts_per_month.max()
    return most_workouts_month, most_workouts_count

# Function to get training days in the month with the most workouts
def get_training_days_in_month(workout_data, month):
    most_workouts_month_data = workout_data[workout_data['workout_month'] == month]
    training_days = most_workouts_month_data['start_time'].dt.day.unique().tolist()
    return training_days

# Function to create a calendar for a specific month and year
def create_calendar(year, month, highlight_days):
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]
    days = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']
    
        # Create table header
    header = f"""
    <table style='border-collapse: collapse; width: 50%; background-color: white; color: black;'>
        <tr>
            <th colspan='7' style='text-align: center; font-size: 24px; background-color: lightgray; border: 1px solid black;'>{month_name} {year}</th>
        </tr>
        <tr>
            {" ".join(f"<th style='border: 1px solid black; padding: 5px; background-color: white;'>{day}</th>" for day in days)}
        </tr>
    """
    # Create table rows
    rows = ""
    for week in cal:
        row = "<tr>"
        for day in week:
            if day == 0:
                row += "<td style='border: 1px solid black; padding: 10px; background-color: #white;'></td>"
            elif day in highlight_days:
                row += f"<td style='border: 1px solid black; padding: 10px; background-color: lightblue; color: black;'>{day}</td>"
            else:
                row += f"<td style='border: 1px solid black; padding: 10px; background-color: #white; color: black;'>{day}</td>"
        row += "</tr>"
        rows += row
    
    # Combine header and rows
    table = header + rows + "</table>"
    return table

def create_calander(workout_data):
    # Calculate the month with the most workouts and get the training days
    most_workouts_month, most_workouts_count = calculate_month_with_most_workouts(workout_data)
    training_days = get_training_days_in_month(workout_data, most_workouts_month)
    
    # Get the year and month from the most workouts month
    year = most_workouts_month.year
    month = most_workouts_month.month

    calendar_html = create_calendar(year, month, training_days)
    
    # Display the calendar using Streamlit's HTML method
    st.markdown(calendar_html, unsafe_allow_html=True)
