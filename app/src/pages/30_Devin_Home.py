import streamlit as st
from modules.nav import SideBarLinks
SideBarLinks(show_home=True)


st.title("Welcome, Devin!")
st.write("### Role: Data Analyst")
st.write("Navigate through your features:")

if st.button("View Metrics"):
    st.write("Redirecting to View Metrics page...")
    st.experimental_rerun()  # Placeholder; replace with redirection logic

if st.button("Create KPI Views"):
    st.write("Redirecting to Create KPI Views page...")
    st.experimental_rerun()

if st.button("Access Dashboard"):
    st.write("Redirecting to Access Dashboard page...")
    st.experimental_rerun()

if st.button("Back to Home"):
    st.session_state['authenticated'] = False
    st.switch_page('ProjectHome.py') 
