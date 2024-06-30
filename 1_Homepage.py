import pandas as pd
import streamlit as st
import streamlit_shadcn_ui as ui
import Calender_Calculator
import Spidergram_creater
import matplotlib.pyplot as plt

# Function to filter data by the number of months
def filter_data_by_months(workout_data, months):
    if months == 0:
        return workout_data
    else:
        workout_data = workout_data.copy()
        workout_data.loc[:, 'start_time'] = pd.to_datetime(workout_data['start_time'], format="%d %b %Y, %H:%M", dayfirst=True)
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
    # Processing datetime data
    workouts_df = workout_data.copy()
    workouts_df['start_time'] = pd.to_datetime(workouts_df['start_time'], format='%d %b %Y, %H:%M')
    workouts_df['year'] = workouts_df['start_time'].dt.isocalendar().year
    workouts_df['week'] = workouts_df['start_time'].dt.isocalendar().week
    weekly_workouts = workouts_df.groupby(['year', 'week']).size().reset_index(name='workout_count')

    weekly_workouts = weekly_workouts.sort_values(by=['year', 'week']).reset_index(drop=True)
    max_streak = 0
    current_streak = 0
    previous_week = None
    for _, row in weekly_workouts.iterrows():
        year, week = row['year'], row['week']
        if previous_week is None or (year == previous_week[0] and week == previous_week[1] + 1) or (year == previous_week[0] + 1 and week == 1 and previous_week[1] == 52):
            current_streak += 1
        else:
            current_streak = 1
        max_streak = max(max_streak, current_streak)
        previous_week = (year, week)
    
    return max_streak

def calculate_top_exercises(workout_data):
    exercise_counts = workout_data['exercise_title'].value_counts()
    top_exercises = exercise_counts.head(3)
    sorted_exercises = top_exercises.sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(['2nd Most Trained', 'Most Trained', '3rd Most Trained'], 
            [sorted_exercises.values[1], sorted_exercises.values[0], sorted_exercises.values[2]], 
            color=['silver', '#FFD700', 'brown'], width=1)
    plt.xticks([0, 1, 2], sorted_exercises.index, fontsize=8)
    # Add numbers on top of the bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{int(height)}', ha='center', va='bottom')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.yaxis.set_visible(False)

    plt.subplots_adjust(left=0.1, right=0.6, top=0.22, bottom=0.1)
    return fig

def get_csv_file():
    # Allow the user to upload a CSV file
    csv_file = st.file_uploader("hi",type="csv",label_visibility="collapsed")
    if csv_file is not None:
        st.success("Datei erfolgreich hochgeladen!")
        st.title("Overview")
        workout_data = pd.read_csv(csv_file)
        st.session_state['uploaded_data'] = workout_data
    else:
        if 'uploaded_data' in st.session_state:
            workout_data = st.session_state['uploaded_data']
        else:
            workout_data = None
    return workout_data  

def main():
    st.set_page_config(
    page_title="Hevy Dashboard",
    page_icon="🚀"
    )
    st.sidebar.success("Select a page above")
    workout_data = get_csv_file()

    if workout_data is not None:
        # Slider hinzufügen
        workout_data['start_time'] = pd.to_datetime(workout_data['start_time'], format="%d %b %Y, %H:%M", dayfirst=True)
        max_months_available = (workout_data['start_time'].max() - workout_data['start_time'].min()).days // 30
        slider_value = st.slider(
            label="Anzahl der Monate die Berücksichtigt werden sollen: 0 = Alle Monate",
            min_value=0,
            max_value=min(12, max_months_available),
            value=0,  # Standardwert
            step=1,  # Schrittweite
        )
        workout_data = filter_data_by_months(workout_data, slider_value)
        # Filter workout data based on slider value
        total_workouts = calculate_total_workouts(workout_data)
        average_duration = calculate_average_duration(workout_data)
        longest_streak = calculate_longest_streak(workout_data)

        st.markdown("<h3 style='text-align: center;'>Top 3 Excersises</h2>", unsafe_allow_html=True)
        fig = calculate_top_exercises(workout_data)
        st.pyplot(fig)   

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
            st.subheader('Focused muscle groups')
            Spidergram_creater.main(workout_data)
        

    else:
        st.error("Please upload a Workout Data to get started")
        st.markdown('     Log in at [Hevy](https://hevy.com), navigate to Settings, select "Export Data" to download your CSV file.')    

    
main()