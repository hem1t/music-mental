import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Saving cleaned data
# from cleaner import *
from helpers import get_data_dir


@st.cache_data
def load_data():
    # Assuming data is cleaned for now
    # TODO: run cleaning methods here.
    # For using cleaned data from cleaner.
    return pd.read_csv(f"{get_data_dir()}/mxmh_survey_results_cleaner.csv")

df = load_data()
# st.write(df)

st.set_page_config(
    layout="wide"
)

st.selectbox("Questions", [
    "What is the effect distribution among listeners?",
    "Does stays consistent across different mental health conditions?",

])