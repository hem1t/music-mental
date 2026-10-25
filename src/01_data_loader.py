#!/usr/bin/env python3

import kagglehub

kagglehub.dataset_download(
    "catherinerasgaitis/mxmh-survey-results",
    path="mxmh_survey_results.csv",
    output_dir="./data",
    force_download=True,
)

