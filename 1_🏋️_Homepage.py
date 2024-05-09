import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt



# Set the page configuration
st.set_page_config(
    page_title="Hevy Dashboard",
    page_icon="🏋️"
)

# Set the background image
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://wallpapercave.com/wp/wp12424948.jpg");
    background-position: center;  
    background-repeat: no-repeat;
}
</style>
"""
st.markdown(background_image, unsafe_allow_html=True)


st.sidebar.success("Select a page above")
# Create headers
st.title("Main Page")

df = None
# Allow the user to upload a CSV file
if st.session_state.get('uploaded_data') is None:
    csv_file = st.file_uploader("Upload csv", type="csv")
    st.write("No file uploaded yet.")

    if csv_file is not None:
        st.success("Datei erfolgreich hochgeladen!")
        df = pd.read_csv(csv_file)
        st.session_state['uploaded_data'] = df
        st.write("File uploaded and saved in session state successfully!")

else:
    df = st.session_state.get('uploaded_data')

if df is not None:
    try:
        st.session_state['uploaded_data'] = df
        st.write("File uploaded and saved in session state successfully!")

        # Processing datetime data
        df['start_time'] = pd.to_datetime(df['start_time'])
        df['end_time'] = pd.to_datetime(df['end_time'])
        
        # Calculate duration in minutes for each workout
        df['duration_minutes'] = (df['end_time'] - df['start_time']).dt.total_seconds() / 60
        
        # Display total workouts and average duration
        total_workouts = df['title'].nunique()
        average_duration = df['duration_minutes'].mean()
        st.metric(label="Total Workouts", value=total_workouts)
        st.metric(label="Average Workout Duration (minutes)", value=f"{average_duration:.2f}")
        
        # Display the most common exercises
        common_exercises = df['exercise_title'].value_counts().nlargest(5)
        st.subheader("Most Common Exercises")
        fig, ax = plt.subplots()
        sns.barplot(x=common_exercises.values, y=common_exercises.index, ax=ax)
        plt.xlabel("Frequency")
        plt.ylabel("Exercise")
        st.pyplot(fig)
        
        # Calendar view of workouts
        workout_dates = df['start_time'].dt.date.value_counts()
        workout_dates = workout_dates.reset_index()
        workout_dates.columns = ['date', 'count']
        st.subheader("Workout Calendar")
        fig = px.scatter(workout_dates, x='date', y='count', size='count', title="Workouts by Date")
        st.plotly_chart(fig)
        
    except Exception as e:
        st.error(f"Es gab ein Problem beim Lesen der Datei: {e}")
