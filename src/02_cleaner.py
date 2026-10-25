"""# Loading and Renaming columns"""

import logging
import pandas as pd
import os

# Making sure the data directory is under project root
data_dir = "./data"
if os.getcwd().endswith("/src"):
    data_dir = "../data"

# Logging to file and console
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s [%(lineno)d] - %(message)s",
    handlers=[logging.FileHandler(f"{data_dir}/data_cleaning.log"), logging.StreamHandler()])



###################################
# Loding and cleaning starts here #
###################################

df = pd.read_csv(f"{data_dir}/mxmh_survey_results.csv")

logging.info(f"Initial columns of the dataframe: {df.columns.tolist()}")

df1 = df.drop(columns=["Timestamp", "Foreign languages", "Permissions", "Exploratory"])

# Changing column names
df1.columns = [
    "age",
    "streaming_service",
    "hours_daily",
    "listen_on_work",
    "is_instrumentalist",
    "is_composer",
    "fav_genre",
    "bpm",
    "fr_classical",
    "fr_country",
    "fr_edm",
    "fr_folk",
    "fr_gospel",
    "fr_hiphop",
    "fr_jazz",
    "fr_kpop",
    "fr_latin",
    "fr_lofi",
    "fr_metal",
    "fr_pop",
    "fr_rnb",
    "fr_rap",
    "fr_rock",
    "fr_videogame",
    "anxiety_scr",
    "depression_scr",
    "insomnia_scr",
    "ocd_scr",
    "effect",
]

# Calculating the number of missing values in each column
missing_count = {}
for col in df1.columns:
    missing_count[col] = (df1[col].isna().sum(), df1[col].isna().sum() / len(df1) * 100)
    logging.info(f"Missing values in column '{col}': {missing_count[col][0]} ({missing_count[col][1]:.2f}%)")

for col, (count, percent) in missing_count.items():
    if count > 10:
        logging.warning(f"Column '{col}' has {count} missing values ({percent:.2f}%).")

"""
# Setting number series if blank to median
This includes `age`, `hours_daily`, `bpm`, `*_scr`.
"""
numerical_columns = [
    "age",
    "hours_daily",
    "bpm",
    "anxiety_scr",
    "depression_scr",
    "insomnia_scr",
    "ocd_scr",
]

logging.info(f"Numerical columns to fill NAs with median: {numerical_columns}")
logging.info(f"Missing values before filling: {df1[numerical_columns].isna().sum()}")

for col in numerical_columns:
    df1[col] = df1[col].fillna(df1[col].median())

logging.info(f"Missing values after filling: {df1[numerical_columns].isna().sum()}")



"""# Filling NAs of Yes and Nos if any Na
This includes `listen_on_work`, `is_instrumentalist`, `is_composer`.
"""
yn_columns = ["listen_on_work", "is_instrumentalist", "is_composer"]

logging.info(f"YN columns to fill NAs with 'No': {yn_columns}")
logging.info(f"Missing values before filling: {df1[yn_columns].isna().sum()}")

for col in yn_columns:
    df1[col] = df1[col].fillna("No")

logging.info(f"Missing values after filling: {df1[yn_columns].isna().sum()}")


"""
# Setting frequencies
If na set to Never
"""
frequency_columns = df1.columns[df1.columns.str.startswith("fr_")]

for col in frequency_columns:
    df1[col] = df1[col].fillna("Never")

logging.info(f"Missing values in frequency columns after filling: {df1[frequency_columns].isna().sum()}")



"""
# Primary Streaming service value replacement and filling NAs with Other
"""
logging.info(f"Values in 'streaming_service' column before cleaning: {df1.streaming_service.unique()}")
df1.streaming_service = df1.streaming_service.replace(
    {"I do not use a streaming service.": "Other", "Other streaming service": "Other"}
)
df1.streaming_service = df1.streaming_service.fillna("Other")

# is subset
assert {"Spotify", "Pandora", "YouTube Music", "Other", "Apple Music"} <= set(
    df1.streaming_service.unique()
)
logging.info(f"Values in 'streaming_service' column after cleaning: {df1.streaming_service.unique()}")



"""
# Favorite Genre
"""

logging.info(f"Values in 'fav_genre' column before cleaning: {df1.fav_genre.unique()}")

df1.fav_genre = df1.fav_genre.replace(
    {"Video game music": "VideoGame", "Hip hop": "HipHop", "K pop": "KPop"}
)

df1.fav_genre = df1.fav_genre.fillna("Other")

# is subset
assert {
    "Latin",
    "Rock",
    "VideoGame",
    "Jazz",
    "R&B",
    "KPop",
    "Country",
    "EDM",
    "HipHop",
    "Pop",
    "Rap",
    "Classical",
    "Metal",
    "Folk",
    "Lofi",
    "Gospel",
} <= set(df1.fav_genre.unique())

logging.info(f"Values in 'fav_genre' column after cleaning: {df1.fav_genre.unique()}")


"""
# Music Effect
"""
logging.info(f"Values in 'effect' column before cleaning: {df1.effect.unique()}")

if df1.effect.isna().sum() > 0:
    logging.info(f"Missing values in 'effect' column: {df1.effect.isna().sum()}") 
    df1.effect = df1.effect.fillna("No effect")
    logging.info(f"Missing values in 'effect' column after filling: {df1.effect.isna().sum()}")

# is subset
assert {"No effect", "Improve", "Worsen"} <= set(df1.effect.unique())
logging.info(f"Values in 'effect' column after cleaning: {df1.effect.unique()}")


# Calculating the number of missing values in each column
missing_count = {}
for col in df1.columns:
    missing_count[col] = (df1[col].isna().sum(), df1[col].isna().sum() / len(df1) * 100)
    logging.info(f"Missing values after cleaning in column '{col}': {missing_count[col][0]} ({missing_count[col][1]:.2f}%)")

for col, (count, percent) in missing_count.items():
    if count > 0:
        logging.warning(f"Column '{col}' has {count} missing values ({percent:.2f}%).")


"""
# Saving cleaned data
"""
logging.info(f"Final columns of the dataframe: {df1.columns.tolist()}")

df1.to_csv(f"{data_dir}/mxmh_survey_results_clean.csv", index=False)
