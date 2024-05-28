import streamlit as st

st.set_page_config(
    page_icon="📊"
    
)
st.title("Statistics Page")
st.sidebar.success("Select a page above")
df = st.session_state.get('uploaded_data')

# Set the background image
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://img.freepik.com/premium-photo/illustration-sunset-hanging-hundreds-chinese-lanterns-chinese-new-year-celebrations_923894-10141.jpg?w=826");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
}
</style>
"""
st.markdown(background_image, unsafe_allow_html=True)

if df is not None:
    st.success("File successfully transfered!")
    try:
        st.write("Vorschau der hochgeladenen Daten:")
        st.dataframe(df.head())
    except Exception as e:
        st.error(f"Es gab ein Problem beim Lesen der Datei: {e}")