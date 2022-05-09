import streamlit as st
from discrete_slider import discrete_slider

cars = ["Porsche", "Mercedes", "BMV", "Audi", "VW"]
st.subheader("Develop Mode")
selected_idx = discrete_slider(cars)
st.markdown(f"You've selected: {cars[selected_idx]}")