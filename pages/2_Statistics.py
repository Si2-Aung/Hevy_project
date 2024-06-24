import streamlit as st
import pandas as pd
import streamlit_shadcn_ui as ui

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
            st.warning(f"Du hast in den letzten {months} Monaten kein '{st.session_state.selected_exercise}' trainiert. Wähle eine andere Übung.")
        st.session_state.selected_exercise = sorted_exercises[0]
    
    selected_exercise = st.selectbox('Select an exercise: (sortiert nach häufigkeit )', sorted_exercises, index=sorted_exercises.index(st.session_state.selected_exercise))
    st.session_state.selected_exercise = selected_exercise

    return workout_data[workout_data['exercise_title'] == selected_exercise]

def get_personal_best(exercise_data):
    if exercise_data.empty:
        st.warning("No data available for the selected exercise.")
        return None
    
    # Filter out rows with NaN values in the 'weight_kg' column
    valid_data = exercise_data.dropna(subset=['weight_kg'])
    
    if valid_data.empty:
        return None
    
    # Find the row with the highest weight lifted
    max_weight_row = valid_data.loc[valid_data['weight_kg'].idxmax()]
    highest_weight = int(max_weight_row['weight_kg'])
    reps_with_highest_weight = int(max_weight_row['reps'])
    personal_best = f"{highest_weight}kg x {reps_with_highest_weight} 🦾"
    
    return personal_best

def get_total_volume_lifted(exercise_data):
    if exercise_data.empty:
        return None
    
    # Filter out rows with NaN values in the 'weight_kg' and 'reps' columns
    valid_data = exercise_data.dropna(subset=['weight_kg', 'reps'])
    
    if valid_data.empty:
        return None
    
    total_volume = (valid_data['weight_kg'] * valid_data['reps']).sum()
    return f"{total_volume} kg 🤯"

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
        exercise_data = choose_exercise(workout_data, slider_value)
        if not exercise_data.empty:
            #Display Data
            personal_best = get_personal_best(exercise_data)
            total_volume_lifted = get_total_volume_lifted(exercise_data)
            if personal_best or total_volume_lifted is not None:
                cols = st.columns(2)
                with cols[0]:
                    ui.metric_card(title="Personal best", content= personal_best, key="card1")
                with cols[1]:
                    ui.metric_card(title="Total volume lifted", content=total_volume_lifted, key="card2")
            else:
                st.warning("Sry, Exercises without weights are not included...yet")
    st.warning("Ich wollte noch mehr machen aber bin zu faul")


            
main()
