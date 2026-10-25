#!/usr/bin/env python3

import kagglehub
import os

data_dir = "./data"
if os.getcwd().endswith("/src"):
    data_dir = "../data"


kagglehub.dataset_download(
    "catherinerasgaitis/mxmh-survey-results",
    path="mxmh_survey_results.csv",
    output_dir=data_dir,
    force_download=True,
)

