import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit_shadcn_ui as ui

# Set the page configuration
st.set_page_config(
    page_title="Hevy Dashboard",
    page_icon="🏋️"
)

st.sidebar.success("Select a page above")
# Create headers

# CSS for background image
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("");
    background-position: center;  
    background-repeat: no-repeat;
}
</style>
"""
st.markdown(background_image, unsafe_allow_html=True)

# Function to calculate total workouts
def calculate_total_workouts(workout_data):
    return str(workout_data['start_time'].nunique())

# Function to calculate average workout duration
def calculate_average_duration(workout_data):
    # Processing datetime data
    workout_data['start_time'] = pd.to_datetime(workout_data['start_time'], format="%d %b %Y, %H:%M", dayfirst=True)
    workout_data['end_time'] = pd.to_datetime(workout_data['end_time'], format="%d %b %Y, %H:%M", dayfirst=True)
    # Calculate duration in minutes for each workout
    workout_data['duration_minutes'] = (workout_data['end_time'] - workout_data['start_time']).dt.total_seconds() / 60
    result = str(round(workout_data['duration_minutes'].mean()))+ " minutes"
    return result

# Function to calculate longest streak
def calculate_longest_streak(workout_data):
    workout_data['workout_week'] = workout_data['start_time'].dt.isocalendar().week
    workout_data['workout_year'] = workout_data['start_time'].dt.isocalendar().year
    workout_data['year_week'] = workout_data['workout_year'].astype(str) + "-" + workout_data['workout_week'].astype(str)
    
    streaks = workout_data['year_week'].value_counts().sort_index().index
    longest_streak = 1
    current_streak = 1
    
    for i in range(1, len(streaks)):
        if int(streaks[i].split("-")[1]) - int(streaks[i-1].split("-")[1]) == 1:
            current_streak += 1
        else:
            longest_streak = max(longest_streak, current_streak)
            current_streak = 1
    return str(max(longest_streak, current_streak))


# Allow the user to upload a CSV file
csv_file = st.file_uploader("Upload your Hevy-CSV file",type="csv")

if csv_file is not None:
    st.success("Datei erfolgreich hochgeladen!")
    workout_data = pd.read_csv(csv_file)
    st.session_state['uploaded_data'] = workout_data
else:
    if 'uploaded_data' in st.session_state:
        workout_data = st.session_state['uploaded_data']
    else:
        workout_data = None

if workout_data is not None:
    try:
        st.header("Overview")
    
        total_workouts = calculate_total_workouts(workout_data)
        average_duration = calculate_average_duration(workout_data)
        longest_streak = calculate_longest_streak(workout_data)
        
        cols = st.columns(3)
        with cols[0]:
            ui.metric_card(title="Total Workouts", content=total_workouts, key="card1")
        with cols[1]:
            ui.metric_card(title="Average Workout Time", content=average_duration, key="card2")
        with cols[2]:
            ui.metric_card(title="Longest Streak (weeks)", content=longest_streak, key="card3")
    
    except Exception as e:
        st.error(f"Es gab ein Problem beim Lesen der Datei: {e}")
