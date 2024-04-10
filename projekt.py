import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image
import seaborn as sns
import matplotlib.pyplot as plt



# Setzt die Seitenkonfiguration
st.set_page_config(page_title="Hevy Dashboard")

# Erstellt Überschriften
st.header("Hevy Daten")
st.subheader("Wie oft trainierst du?")

# Ermöglicht dem Benutzer das Hochladen einer CSV-Datei
csv_file = st.file_uploader("Upload csv", type=["csv"])

# Überprüft, ob eine Datei hochgeladen wurde
if csv_file is not None:
    # Zeigt eine Erfolgsmeldung an
    st.success("Datei erfolgreich hochgeladen!")
    
    # Versucht, die CSV-Datei zu lesen
    try:
        # Verwendet Pandas, um die CSV-Datei zu lesen
        df = pd.read_csv(csv_file)
        
        # Zeigt eine Vorschau der Daten an
        st.write("Vorschau der hochgeladenen Daten:")
        st.dataframe(df.head())  # Zeigt die ersten Zeilen der DataFrame an
    except Exception as e:
        # Zeigt eine Fehlermeldung an, falls die Datei nicht gelesen werden kann
        st.error(f"Es gab ein Problem beim Lesen der Datei: {e}")
else:
    # Anweisung, wenn keine Datei hochgeladen wurde
    st.info("Bitte lade eine CSV-Datei hoch, um fortzufahren.")