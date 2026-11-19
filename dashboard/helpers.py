#!/usr/bin/env python3

import kagglehub
import os
import pandas as pd


# TODO: Use Env file
def get_data_dir():
    data_dir = "./.data"
    if os.getcwd().endswith("/src"):
        data_dir = "../.data"

    return data_dir


def download_data(force=False):
    if force:
        log_info("Enabled force download from kaggle.")

    data_dir = get_data_dir()
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    try:
        log_info("Downloading data from kaggle.")
        kagglehub.dataset_download(
            "catherinerasgaitis/mxmh-survey-results",
            path="mxmh_survey_results.csv",
            output_dir=get_data_dir(),
            force_download=force,
        )
    except Exception as e:
        log_error("Error downloading data from kaggle.")
        log_error(e)


# TODO: Use env file
DATA_NAME = "mxmh_survey_results"
DATA_PATH = f"{get_data_dir()}/{DATA_NAME}.csv"
CLEAN_DATA_PATH = f"{get_data_dir()}/{DATA_NAME}_clean.csv"


def get_uncleaned_data():
    global DATA_PATH
    try:
        log_info("Loading Uncleaned data to memory.")
        return pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        raise FileNotFoundError(f"Uncleaned data not found. at {DATA_PATH}")


def get_cleaned_data():
    global CLEAN_DATA_PATH
    try:
        log_info("Loading Cleaned data to memory.")
        return pd.read_csv(CLEAN_DATA_PATH)
    except FileNotFoundError:
        raise FileNotFoundError(f"Cleaned data not found. at {CLEAN_DATA_PATH}")

import logging

LOGGING = False


def enable_logging():
    global LOGGING
    LOGGING = True

    data_dir = get_data_dir()
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s [%(lineno)d] - %(message)s",
        handlers=[
            logging.FileHandler(f"{get_data_dir()}/data_cleaning.log"),
            logging.StreamHandler(),
        ],
    )


def log_info(msg):
    if LOGGING:
        logging.info(msg)


def log_warning(msg):
    if LOGGING:
        logging.warning(msg)


def log_error(msg):
    if LOGGING:
        logging.error(msg)


def clear_logs():
    log_path = f"{get_data_dir()}/data_cleaning.log"
    try:
        with open(log_path, "w", encoding="utf-8"):
            pass
    except FileNotFoundError:
        pass
