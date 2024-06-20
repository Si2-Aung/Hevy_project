import streamlit as st
import pandas as pd

def get_workout_data():
    workout_data = st.session_state.get('uploaded_data')
    if workout_data is None:
        st.error("Please upload a file to get started")
        return None
    return workout_data

def filter_data_by_months(workout_data, months):
    if months == 0:
        return workout_data
    else:
        workout_data = workout_data.copy()
        workout_data['start_time'] = pd.to_datetime(workout_data['start_time'], format="%d %b %Y, %H:%M", dayfirst=True)
        latest_date = workout_data['start_time'].max()
        start_date = latest_date - pd.DateOffset(months=months)
        return workout_data[workout_data['start_time'] >= start_date]

def choose_exercise(workout_data, months):
    # Sort exercises by frequency
    exercise_counts = workout_data['exercise_title'].value_counts()
    sorted_exercises = exercise_counts.index.tolist()

    if 'selected_exercise' not in st.session_state or st.session_state.selected_exercise not in sorted_exercises:
        if 'selected_exercise' in st.session_state:
            st.warning(f"Du hast in den letzten {months} Monat kein '{st.session_state.selected_exercise}' trainiert. Wähle ne andere Übung.")
        st.session_state.selected_exercise = sorted_exercises[0]
    
    selected_exercise = st.selectbox('Select an exercise: (sortiert nach häufigkeit )', sorted_exercises, index=sorted_exercises.index(st.session_state.selected_exercise))
    st.session_state.selected_exercise = selected_exercise

    return workout_data[workout_data['exercise_title'] == selected_exercise]

def main():
    st.set_page_config(
        page_title="More Statistics",
        page_icon="📊"
    )
    st.title("Exercise Statistics")
    st.sidebar.success("Select a page above")
    workout_data = get_workout_data()
    if workout_data is not None:
        slider_value = st.slider(
            label="Anzahl der Monate die Berücksichtigt werden sollen: 0 = Alle Monate",
            min_value=0,
            max_value=12,
            value=0,  # Standardwert
            step=1,  # Schrittweite
        )
        workout_data = filter_data_by_months(workout_data, slider_value)
        exercise_data = choose_exercise(workout_data,slider_value) #Funtion before filter_data_by_months
main()
