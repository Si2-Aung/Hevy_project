import pandas as pd
import streamlit as st
import streamlit_shadcn_ui as ui
import Calender_Calculator
import Spidergram_creater

# Set the page configuration
def setPage():    
    st.set_page_config(
        page_title="Hevy Dashboard",
        page_icon="🏋️"
    )
    st.sidebar.success("Select a page above")
    st.header("Overview")
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
# Function to filter data by the number of months
def filter_data_by_months(workout_data, months):
    if months == 0:
        return workout_data
    else:
        workout_data['start_time'] = pd.to_datetime(workout_data['start_time'], format="%d %b %Y, %H:%M", dayfirst=True)
        latest_date = workout_data['start_time'].max()
        start_date = latest_date - pd.DateOffset(months=months)
        return workout_data[workout_data['start_time'] >= start_date]
    
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
    result = str(round(workout_data['duration_minutes'].mean()))+ " min"
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

def get_csv_file():
    # Allow the user to upload a CSV file
    csv_file = st.file_uploader("",type="csv")
    if csv_file is not None:
        st.success("Datei erfolgreich hochgeladen!")
        workout_data = pd.read_csv(csv_file)
        st.session_state['uploaded_data'] = workout_data
    else:
        if 'uploaded_data' in st.session_state:
            workout_data = st.session_state['uploaded_data']
        else:
            workout_data = None
    return workout_data  

def main():
    setPage()
    workout_data = get_csv_file()

    if workout_data is not None:
        # Slider hinzufügen
        slider_value = st.slider(
            label="Wähle die Anzahl der Monate",
            min_value=0,
            max_value=12,
            value=0,  # Standardwert
            step=1  # Schrittweite
        )
        
        # Filter workout data based on slider value
        workout_data = filter_data_by_months(workout_data, slider_value)

        total_workouts = calculate_total_workouts(workout_data)
        average_duration = calculate_average_duration(workout_data)
        longest_streak = calculate_longest_streak(workout_data)

        cols = st.columns(3)
        with cols[0]:
            ui.metric_card(title="Total Workouts", content=total_workouts, key="card1")
        with cols[1]:
            ui.metric_card(title="Average Workout Time", content=average_duration, key="card2")
        with cols[2]:
            ui.metric_card(title="Longest Streak in weeks", content=longest_streak, key="card3")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Most tryhard month")
            Calender_Calculator.create_calander(workout_data)

        with col2:
            st.subheader('Focued muscle groups')
            Spidergram_creater.main(workout_data)

    else:
        st.error("Please upload a file to get started")

    
main()