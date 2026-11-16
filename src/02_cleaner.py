"""# Loading and Renaming columns"""

import logging
import pandas as pd
import os

# Making sure the data directory is under project root
data_dir = "./.data"
if os.getcwd().endswith("/src"):
    data_dir = "../.data"

# Logging to file and console
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s [%(lineno)d] - %(message)s",
    handlers=[logging.FileHandler(f"{data_dir}/data_cleaning.log"), logging.StreamHandler()])


logging.info(f"Data directory set to: {data_dir}")

###################################
# Loding and cleaning starts here #
###################################

df = pd.read_csv(f"{data_dir}/mxmh_survey_results.csv")

logging.info(f"Initial columns of the dataframe: {df.columns.tolist()}")

## Dropping columns
df.drop(columns=["Timestamp", "Foreign languages", "Permissions", "Exploratory"], inplace=True)
# Changing column names
df.columns = [
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

## Stats before cleaning
from collections import OrderedDict

def data_stats(df):
    """
    Routine to generate complete stats on datatable.
        input: Dataframe
        output: (d1, d2)
            d1: Numerical columns stats dataframe
            d2: Categorical columns stats dataframe
    """
    numerical_columns = df.select_dtypes(include=['number']).columns.tolist()
    d1 = []
    for col in numerical_columns:
        d1.append(
            OrderedDict({
                'min': df[col].min(),
                'max': df[col].max(),
                'mean': df[col].mean(),
                'std': df[col].std(),
                '50%': df[col].quantile(0.5),
                '25%': df[col].quantile(0.25),
                '75%': df[col].quantile(0.75),
                'IQR': df[col].quantile(0.75) - df[col].quantile(0.25),
                'skew': df[col].skew(),
                'kurtosis': df[col].kurtosis(),
                'missing_values': df[col].isnull().sum()/df.shape[0] * 100,
            })
        )
    d1 = pd.DataFrame(d1, index=numerical_columns)

    categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
    d2 = []
    for col in categorical_columns:
        d2.append(
            OrderedDict({
                'unique_values': df[col].nunique(),
                'top_value': df[col].mode()[0],
                'top_value_percentage': df[col].value_counts(normalize=True).iloc[0] * 100,
                'missing_values_percentage': df[col].isnull().sum()/df.shape[0] * 100,
                'unique_values_list': df[col].unique()
            })
        )
    d2 = pd.DataFrame(d2, index=categorical_columns)

    return d1, d2


# Checking stats before cleaning
num_stats, cat_stats = data_stats(df)

## Report ie log anomalies
num_cols_with_high_missing_values = []
cat_cols_with_high_missing_values = []
# Present null values
for row in num_stats.index:
    if num_stats.loc[row, 'missing_values'] > 10:
        logging.warning(f"Column '{row}' has missing values: {num_stats.loc[row, 'missing_values']}")
        num_cols_with_high_missing_values.append(row)

for row in cat_stats.index:
    if cat_stats.loc[row, 'missing_values_percentage'] > 10:
        logging.warning(f"Column '{row}' has missing values: {cat_stats.loc[row, 'missing_values_percentage']:.2f}%")
        cat_cols_with_high_missing_values.append(row)

cols_with_high_kurt_skew = []
# imporper skewness and kurtosis
for row in num_stats.index:
    if abs(num_stats.loc[row, 'skew']) > 2:
        logging.warning(f"Column '{row}' has high skewness: {num_stats.loc[row, 'skew']}")
        cols_with_high_kurt_skew.append(row)
    if abs(num_stats.loc[row, 'kurtosis']) > 5:
        logging.warning(f"Column '{row}' has high kurtosis: {num_stats.loc[row, 'kurtosis']}")
        cols_with_high_kurt_skew.append(row)



# """
# # Setting number series if blank to median
# This includes `age`, `hours_daily`, `bpm`, `*_scr`.
# """
# numerical_columns = [
#     "age",
#     "hours_daily",
#     "bpm",
#     "anxiety_scr",
#     "depression_scr",
#     "insomnia_scr",
#     "ocd_scr",
# ]

# logging.info(f"Numerical columns to fill NAs with median: {numerical_columns}")
# logging.info(f"Missing values before filling: {df1[numerical_columns].isna().sum()}")

# for col in numerical_columns:
#     df1[col] = df1[col].fillna(df1[col].median())

# logging.info(f"Missing values after filling: {df1[numerical_columns].isna().sum()}")



# """# Filling NAs of Yes and Nos if any Na
# This includes `listen_on_work`, `is_instrumentalist`, `is_composer`.
# """
# yn_columns = ["listen_on_work", "is_instrumentalist", "is_composer"]

# logging.info(f"YN columns to fill NAs with 'No': {yn_columns}")
# logging.info(f"Missing values before filling: {df1[yn_columns].isna().sum()}")

# for col in yn_columns:
#     df1[col] = df1[col].fillna("No")

# logging.info(f"Missing values after filling: {df1[yn_columns].isna().sum()}")


# """
# # Setting frequencies
# If na set to Never
# """
# frequency_columns = df1.columns[df1.columns.str.startswith("fr_")]

# for col in frequency_columns:
#     df1[col] = df1[col].fillna("Never")

# logging.info(f"Missing values in frequency columns after filling: {df1[frequency_columns].isna().sum()}")



# """
# # Primary Streaming service value replacement and filling NAs with Other
# """
# logging.info(f"Values in 'streaming_service' column before cleaning: {df1.streaming_service.unique()}")
# df1.streaming_service = df1.streaming_service.replace(
#     {"I do not use a streaming service.": "Other", "Other streaming service": "Other"}
# )
# df1.streaming_service = df1.streaming_service.fillna("Other")

# # is subset
# assert {"Spotify", "Pandora", "YouTube Music", "Other", "Apple Music"} <= set(
#     df1.streaming_service.unique()
# )
# logging.info(f"Values in 'streaming_service' column after cleaning: {df1.streaming_service.unique()}")



# """
# # Favorite Genre
# """

# logging.info(f"Values in 'fav_genre' column before cleaning: {df1.fav_genre.unique()}")

# df1.fav_genre = df1.fav_genre.replace(
#     {"Video game music": "VideoGame", "Hip hop": "HipHop", "K pop": "KPop"}
# )

# df1.fav_genre = df1.fav_genre.fillna("Other")

# # is subset
# assert {
#     "Latin",
#     "Rock",
#     "VideoGame",
#     "Jazz",
#     "R&B",
#     "KPop",
#     "Country",
#     "EDM",
#     "HipHop",
#     "Pop",
#     "Rap",
#     "Classical",
#     "Metal",
#     "Folk",
#     "Lofi",
#     "Gospel",
# } <= set(df1.fav_genre.unique())

# logging.info(f"Values in 'fav_genre' column after cleaning: {df1.fav_genre.unique()}")


# """
# # Music Effect
# """
# logging.info(f"Values in 'effect' column before cleaning: {df1.effect.unique()}")

# if df1.effect.isna().sum() > 0:
#     logging.info(f"Missing values in 'effect' column: {df1.effect.isna().sum()}") 
#     df1.effect = df1.effect.fillna("No effect")
#     logging.info(f"Missing values in 'effect' column after filling: {df1.effect.isna().sum()}")

# # is subset
# assert {"No effect", "Improve", "Worsen"} <= set(df1.effect.unique())
# logging.info(f"Values in 'effect' column after cleaning: {df1.effect.unique()}")


# # Calculating the number of missing values in each column
# missing_count = {}
# for col in df1.columns:
#     missing_count[col] = (df1[col].isna().sum(), df1[col].isna().sum() / len(df1) * 100)
#     logging.info(f"Missing values after cleaning in column '{col}': {missing_count[col][0]} ({missing_count[col][1]:.2f}%)")

# for col, (count, percent) in missing_count.items():
#     if count > 0:
#         logging.warning(f"Column '{col}' has {count} missing values ({percent:.2f}%).")


# """
# # Saving cleaned data
# """
# logging.info(f"Final columns of the dataframe: {df1.columns.tolist()}")

# df1.to_csv(f"{data_dir}/mxmh_survey_results_clean.csv", index=False)
