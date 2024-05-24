import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data
file_path = 'dein_dateipfad.csv'  # Update this to your actual file path
workout_data = pd.read_csv(file_path)

# Define the mapping of exercises to categories based on your specifications
category_mapping = {
    'Core': [
        'Ab Scissors', 'Ab Wheel', 'Bicycle Crunch', 'Bicycle Crunch Raised Legs',
        'Cable Core Palloff Press', 'Cable Crunch', 'Cable Twist (Down to up)', 
        'Cable Twist (Up to down)', 'Crunch', 'Crunch (Machine)', 'Crunch (Weighted)',
        'Dead Bug', 'Decline Crunch', 'Decline Crunch (Weighted)', 'Dragon Flag',
        'Dragonfly', 'Elbow to Knee', 'Front Lever Hold', 'Front Lever Raise',
        'Hanging Knee Raise', 'Hanging Leg Raise', 'Heel Taps', 'Hollow Rock',
        'Jack Knife (Suspension)', 'Jackknife Sit Up', 'Knee Raise Parallel Bars',
        'L-Sit Hold', 'Landmine 180', 'Leg Raise Parallel Bars', 'Oblique Crunch',
        'Plank', 'Reverse Crunch', 'Reverse Plank', 'Russian Twist (Bodyweight)',
        'Russian Twist (Weighted)', 'Side Bend', 'Side Bend (Dumbbell)', 'Side Plank',
        'Spiderman', 'Toe Touch', 'Toes to Bar', 'Torso Rotation', 'V Up'
    ],
    'Beine': [
        'Assisted Pistol Squats', 'Box Jump', 'Box Squat (Barbell)', 'Bulgarian Split Squat',
        'Calf Extension (Machine)', 'Calf Press (Machine)', 'Curtsy Lunge (Dumbbell)',
        'Deadlift (Band)', 'Deadlift (Barbell)', 'Deadlift (Dumbbell)', 'Deadlift (Smith Machine)',
        'Deadlift (Trap bar)', 'Front Squat', 'Full Squat', 'Glute', 'Glute Bridge',
        'Glute Ham Raise', 'Glute Kickback (Machine)', 'Glute Kickback on Floor', 'Goblet Squat',
        'Good Morning (Barbell)', 'Hack Squat', 'Hack Squat (Machine)', 'Hip Abduction (Machine)',
        'Hip Adduction (Machine)', 'Hip Thrust', 'Hip Thrust (Barbell)', 'Hip Thrust (Machine)',
        'Leg Curl', 'Leg Extension (Machine)', 'Leg Press (Machine)', 'Leg Press Horizontal (Machine)',
        'Lunge', 'Lunge (Barbell)', 'Lunge (Dumbbell)', 'Overhead Dumbbell Lunge', 'Pendulum Squat (Machine)',
        'Pistol Squat', 'Seated Leg Curl (Machine)', 'Single Leg Extensions', 'Single Leg Glute Bridge',
        'Single Leg Hip Thrust', 'Single Leg Hip Thrust (Dumbbell)', 'Single Leg Press (Machine)',
        'Single Leg Romanian Deadlift (Barbell)', 'Single Leg Romanian Deadlift (Dumbbell)',
        'Single Leg Standing Calf Raise', 'Single Leg Standing Calf Raise (Barbell)',
        'Single Leg Standing Calf Raise (Dumbbell)', 'Single Leg Standing Calf Raise (Machine)',
        'Sissy Squat (Weighted)', 'Squat (Band)', 'Squat (Barbell)', 'Squat (Bodyweight)',
        'Squat (Dumbbell)', 'Squat (Machine)', 'Squat (Smith Machine)', 'Squat (Suspension)',
        'Standing Leg Curls', 'Sumo Deadlift', 'Sumo Squat', 'Sumo Squat (Barbell)',
        'Sumo Squat (Dumbbell)', 'Sumo Squat (Kettlebell)', 'Walking Lunge', 'Walking Lunge (Dumbbell)'
    ],
    'Arme': [
        '21s Bicep Curl', 'Bench Dip', 'Bench Press - Close Grip (Barbell)', 'Behind the Back Bicep Wrist Curl (Barbell)',
        'Bicep Curl (Barbell)', 'Bicep Curl (Cable)', 'Bicep Curl (Dumbbell)', 'Bicep Curl (Machine)',
        'Bicep Curl (Suspension)', 'Concentration Curl', 'Cross Body Hammer Curl', 'Diamond Push Up',
        'Drag Curl', 'EZ Bar Biceps Curl', 'Floor Triceps Dip', 'Hammer Curl (Band)', 'Hammer Curl (Cable)',
        'Hammer Curl (Dumbbell)', 'Overhead Curl (Cable)', 'Plate Curl', 'Preacher Curl (Barbell)',
        'Preacher Curl (Dumbbell)', 'Preacher Curl (Machine)', 'Reverse Curl (Barbell)', 'Reverse Curl (Cable)',
        'Reverse Curl (Dumbbell)', 'Reverse Grip Concentration Curl', 'Rope Cable Curl', 'Seated Incline Curl (Dumbbell)',
        'Seated Palms Up Wrist Curl', 'Seated Wrist Extension (Barbell)', 'Single Arm Curl (Cable)', 'Skullcrusher (Barbell)',
        'Skullcrusher (Dumbbell)', 'Spider Curl (Barbell)', 'Spider Curl (Dumbbell)', 'Triceps Dip',
        'Triceps Dip (Assisted)', 'Triceps Dip (Weighted)', 'Triceps Extension (Barbell)', 'Triceps Extension (Cable)',
        'Triceps Extension (Dumbbell)', 'Triceps Extension (Machine)', 'Triceps Extension (Suspension)',
        'Triceps Kickback (Cable)', 'Triceps Kickback (Dumbbell)', 'Triceps Pressdown', 'Triceps Pushdown',
        'Triceps Rope Pushdown', 'Wrist Roller'
    ],
    'Rücken': [
        'Back Extension (Hyperextension)', 'Back Extension (Machine)', 'Back Extension (Weighted Hyperextension)',
        'Bent Over Row (Band)', 'Bent Over Row (Barbell)', 'Bent Over Row (Dumbbell)', 'Chin Up',
        'Chin Up (Assisted)', 'Chin Up (Weighted)', 'Dead Hang', 'Dumbbell Row', 'Gorilla Row (Kettlebell)',
        'Iso-Lateral High Row (Machine)', 'Iso-Lateral Low Row', 'Iso-Lateral Row (Machine)', 'Kneeling Pulldown (band)',
        'Landmine Row', 'Lat Pulldown (Band)', 'Lat Pulldown (Cable)', 'Lat Pulldown (Machine)', 'Lat Pulldown - Close Grip (Cable)',
        'Meadows Rows (Barbell)', 'Negative Pull Up', 'Pendlay Row (Barbell)', 'Pull Up', 'Pull Up (Assisted)',
        'Pull Up (Band)', 'Pull Up (Weighted)', 'Rack Pull', 'Rear Delt Reverse Fly (Cable)', 'Rear Delt Reverse Fly (Dumbbell)',
        'Rear Delt Reverse Fly (Machine)', 'Renegade Row (Dumbbell)', 'Reverse Grip Lat Pulldown (Cable)', 'Rope Straight Arm Pulldown',
        'Seated Cable Row - Bar Grip', 'Seated Cable Row - Bar Wide Grip', 'Seated Cable Row - V Grip (Cable)',
        'Seated Row (Machine)', 'Single Arm Cable Row', 'Single Arm Lat Pulldown', 'Sternum Pull up (Gironda)',
        'Straight Arm Lat Pulldown (Cable)', 'T Bar Row', 'Wide Pull Up'
    ],
    'Cardio': [
        'Aerobics', 'Air Bike', 'Battle Ropes', 'Boxing', 'Climbing', 'Cycling', 'Elliptical Trainer', 'HIIT', 'Hiking',
        'Jump Rope', 'Rowing Machine', 'Running', 'Skiing', 'Snowboarding', 'Spinning', 'Sprints', 'Stair Machine',
        'Treadmill', 'Walking'
    ],
    'Brust': [
        'Around The World', 'Bench Press (Barbell)', 'Bench Press (Cable)', 'Bench Press (Dumbbell)',
        'Bench Press (Smith Machine)', 'Bench Press - Wide Grip (Barbell)', 'Butterfly (Pec Deck)', 'Cable Fly Crossovers',
        'Chest Dip', 'Chest Dip (Assisted)', 'Chest Dip (Weighted)', 'Chest Fly (Band)', 'Chest Fly (Dumbbell)',
        'Chest Fly (Machine)', 'Chest Fly (Suspension)', 'Chest Press (Band)', 'Chest Press (Machine)',
        'Clap Push Ups', 'Decline Bench Press (Barbell)', 'Decline Bench Press (Dumbbell)', 'Decline Bench Press (Machine)',
        'Decline Bench Press (Smith Machine)', 'Decline Chest Fly (Dumbbell)', 'Decline Push Up', 'Dumbbell Squeeze Press',
        'Floor Press (Barbell)', 'Floor Press (Dumbbell)', 'Hex Press (Dumbbell)', 'Incline Bench Press (Barbell)',
        'Incline Bench Press (Dumbbell)', 'Incline Bench Press (Smith Machine)', 'Incline Chest Fly (Dumbbell)',
        'Incline Chest Press (Machine)', 'Incline Push Ups', 'Iso-Lateral Chest Press (Machine)', 'Kneeling Push Up',
        'Low Cable Fly Crossovers', 'Plank Pushup', 'Plate Press', 'Plate Squeeze (Svend Press)', 'Pullover (Dumbbell)',
        'Pullover (Machine)', 'Push Up', 'Push Up (Weighted)', 'Push Up - Close Grip',
    ],
    'shoulder_exercises' : [
        'Arnold Press (Dumbbell)', 'Band Pullaparts', 'Chest Supported Y Raise (Dumbbell)', 'Face Pull', 
        'Front Raise (Band)', 'Front Raise (Barbell)', 'Front Raise (Cable)', 'Front Raise (Dumbbell)', 
        'Front Raise (Suspension)', 'Handstand Push Up', 'Lateral Raise (Band)', 'Lateral Raise (Cable)', 
        'Lateral Raise (Dumbbell)', 'Lateral Raise (Machine)', 'Overhead Press (Barbell)', 'Overhead Press (Dumbbell)', 
        'Overhead Press (Smith Machine)', 'Plate Front Raise', 'Push Press', 'Seated Overhead Press (Barbell)', 
        'Seated Overhead Press (Dumbbell)', 'Seated Shoulder Press (Machine)', 'Shoulder Press (Dumbbell)', 
        'Shoulder Press (Machine Plates)', 'Shoulder Taps', 'Single Arm Landmine Press (Barbell)', 'Single Arm Lateral Raise (Cable)', 
        'Upright Row (Cable)', 'Upright Row (Dumbbell)', 'Upright Row (Barbell)'
    ]
}

# Reverse the mapping for easier lookup
exercise_to_category = {exercise: category for category, exercises in category_mapping.items() for exercise in exercises}
workout_data['category'] = workout_data['exercise_title'].apply(lambda x: [category for exercise, category in exercise_to_category.items() if exercise in x])

# Flatten the categories since some exercises may belong to multiple categories
workout_data = workout_data.explode('category')

# Aggregate the repetitions for simplicity
category_summary = workout_data.groupby('category')['reps'].sum().reindex(category_mapping.keys(), fill_value=0)

# Prepare data for the radar chart
labels = category_summary.index
stats = category_summary.values
stats = np.concatenate((stats,[stats[0]]))  # Close the circle for the radar chart
angles=np.linspace(0, 2*np.pi, len(labels),