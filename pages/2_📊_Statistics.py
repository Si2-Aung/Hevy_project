import streamlit as st

st.set_page_config(
    page_icon="📊"
    
)
st.title("Statistics Page")
st.sidebar.success("Select a page above")
df = st.session_state.get('uploaded_data')

if df is not None:
    st.success("File successfully transfered!")
    try:
        st.write("Vorschau der hochgeladenen Daten:")
        st.dataframe(df.head())
    except Exception as e:
        st.error(f"Es gab ein Problem beim Lesen der Datei: {e}")