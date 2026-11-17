import streamlit as st
import pandas as pd
import os
import kagglehub


@st.cache_data
def load_data():
    data_dir = "./.data"
    if os.getcwd().endswith("/src"):
        data_dir = "../.data"

    kagglehub.dataset_download(
        "catherinerasgaitis/mxmh-survey-results",
        path="mxmh_survey_results.csv",
        output_dir=data_dir,
        force_download=True,
    )

    return pd.read_csv(f"{data_dir}/mxmh_survey_results.csv")


df = load_data()
df
