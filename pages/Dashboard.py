import streamlit as st

def mostrar():
    st.session_state.page = "dashboard"
    st.title("Dashboard")
    st.write("Aquí puedes ver el dashboard de tus gastos.")