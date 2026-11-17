"""# Loading and Renaming columns"""

import logging
import pandas as pd
import helpers

data_dir = helpers.get_data_dir()

###################################
# Loading and cleaning starts here #
###################################

helpers.enable_logging()

df = helpers.get_uncleaned_data()


def fix_columns(df):
    ## Dropping columns
    columns = ["Timestamp", "Foreign languages", "Permissions", "Exploratory"]

    df.drop(
        columns=columns,
        inplace=True,
    )

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

fix_columns(df)

## Stats before cleaning
from collections import OrderedDict


def numerical_col_stats(df):
    """
    Routine to generate complete stats on datatable.
        input: Dataframe
        output: Numerical columns stats dataframe
    """
    numerical_columns = df.select_dtypes(include=["number"]).columns.tolist()
    d1 = []
    for col in numerical_columns:
        d1.append(
            OrderedDict(
                {
                    "min": df[col].min(),
                    "max": df[col].max(),
                    "mean": df[col].mean(),
                    "std": df[col].std(),
                    "50%": df[col].quantile(0.5),
                    "25%": df[col].quantile(0.25),
                    "75%": df[col].quantile(0.75),
                    "IQR": df[col].quantile(0.75) - df[col].quantile(0.25),
                    "skew": df[col].skew(),
                    "kurtosis": df[col].kurtosis(),
                    "missing_values": df[col].isnull().sum() / df.shape[0] * 100,
                }
            )
        )
    d1 = pd.DataFrame(d1, index=numerical_columns)

def categorical_col_stats(df):
    categorical_columns = df.select_dtypes(include=["str"]).columns.tolist()
    d2 = []
    for col in categorical_columns:
        d2.append(
            OrderedDict(
                {
                    "unique_values": df[col].nunique(),
                    "top_value": df[col].mode()[0],
                    "top_value_percentage": df[col].value_counts(normalize=True).iloc[0]
                    * 100,
                    "missing_values_percentage": df[col].isnull().sum()
                    / df.shape[0]
                    * 100,
                    "unique_values_list": df[col].unique(),
                }
            )
        )
    d2 = pd.DataFrame(d2, index=categorical_columns)

    return d1, d2


def find_and_log_anamolies(df):
    # Checking stats before cleaning
    num_stats, cat_stats = data_stats(df)

    ## Report ie log anomalies
    num_cols_with_high_missing_values = []
    cat_cols_with_high_missing_values = []
    # Present null values
    for row in num_stats.index:
        if num_stats.loc[row, "missing_values"] > 0:
            logging.warning(
                f"Column '{row}' has missing values: {num_stats.loc[row, 'missing_values']}"
            )
            num_cols_with_high_missing_values.append(row)

    for row in cat_stats.index:
        if cat_stats.loc[row, "missing_values_percentage"] > 0:
            logging.warning(
                f"Column '{row}' has missing values: {cat_stats.loc[row, 'missing_values_percentage']:.2f}%"
            )
            cat_cols_with_high_missing_values.append(row)

    cols_with_high_kurt = []
    cols_with_high_skew = []

    # imporper skewness and kurtosis
    for row in num_stats.index:
        if abs(num_stats.loc[row, "skew"]) > 2:
            logging.warning(
                f"Column '{row}' has high skewness: {num_stats.loc[row, 'skew']}"
            )
            cols_with_high_skew.append(row)
        if abs(num_stats.loc[row, "kurtosis"]) > 2:
            logging.warning(
                f"Column '{row}' has high kurtosis: {num_stats.loc[row, 'kurtosis']}"
            )
            cols_with_high_kurt.append(row)

    return (
        num_cols_with_high_missing_values,
        cat_cols_with_high_missing_values,
        cols_with_high_kurt,
        cols_with_high_skew,
    )


(
    num_cols_with_high_missing_values,
    cat_cols_with_high_missing_values,
    cols_with_high_kurt,
    cols_with_high_skew,
) = find_and_log_anamolies(df)

## Fixing missings before (can't trim them directly)
for col in num_cols_with_high_missing_values:
    df[col] = df[col].fillna(df[col].median())

for col in cat_cols_with_high_missing_values:
    df[col] = df[col].fillna(df[col].mode()[0])


(
    num_cols_with_high_missing_values,
    cat_cols_with_high_missing_values,
    cols_with_high_kurt,
    cols_with_high_skew,
) = find_and_log_anamolies(df)

## Trying fix on high kurtosis by trimming heavy tail
## Keep trimming till 5 - 95 or till kurtosis value is in right range
for col in cols_with_high_kurt:
    # Future TODO: trim from side where there is better result.
    for percentile_diff in range(1, 5):
        logging.info(
            f"Trimming column '{col}' with percentile difference: {percentile_diff}"
        )
        df = df[(df[col] >= df[col].quantile(percentile_diff / 100))]
        if abs(df[col].kurtosis()) <= 2:
            break
        df = df[(df[col] <= df[col].quantile(1 - percentile_diff / 100))]
        if abs(df[col].kurtosis()) <= 2:
            break


(
    num_cols_with_high_missing_values,
    cat_cols_with_high_missing_values,
    cols_with_high_kurt,
    cols_with_high_skew,
) = find_and_log_anamolies(df)


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
logging.info(f"Final columns of the dataframe: {df.columns.tolist()}")

df.to_csv(f"{data_dir}/mxmh_survey_results_cleaner.csv", index=False)
