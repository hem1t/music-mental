"""# Loading and Renaming columns"""

import logging
import pandas as pd
import helpers

###################################
# Loading and cleaning starts here #
###################################

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

    return df

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

    return d1

def categorical_col_stats(df):
    categorical_columns = df.select_dtypes(include=["str"]).columns.tolist()
    d2 = []
    for col in categorical_columns:
        d2.append(
            OrderedDict(
                {
                    "unique_values": df[col].nunique(),
                    "top_value": df[col].mode()[0],
                    "top_value_percentage": df[col].value_counts(normalize=True).iloc[0] * 100,
                    "missing_values_percentage": df[col].isnull().sum() / df.shape[0]* 100,
                    "unique_values_list": df[col].unique(),
                }
            )
        )
    d2 = pd.DataFrame(d2, index=categorical_columns)

    return d2


def fill_missing_values(df, num_stats, cat_stats):
    ## Report ie log anomalies
    num_cols_with_high_missing_values = []
    cat_cols_with_high_missing_values = []
    # Present null values
    for row in num_stats.index:
        if num_stats.loc[row, "missing_values"] > 0:
            helpers.log_warning(
                f"Column '{row}' has missing values: {num_stats.loc[row, 'missing_values']:.2f}%"
            )
            num_cols_with_high_missing_values.append(row)

    for row in cat_stats.index:
        if cat_stats.loc[row, "missing_values_percentage"] > 0:
            helpers.log_warning(
                f"Column '{row}' has missing values: {cat_stats.loc[row, 'missing_values_percentage']:.2f}%"
            )
            cat_cols_with_high_missing_values.append(row)

    ## Fixing missings before (can't trim them directly)
    for col in num_cols_with_high_missing_values:
        df[col] = df[col].fillna(df[col].median())

    for col in cat_cols_with_high_missing_values:
        df[col] = df[col].fillna(df[col].mode()[0])

    return df

def trim_high_skewness(df, num_stats):
    """
    Remove 1 from each end of the distribution for columns with high skewness (> 1 or < -1)
    """

    high_skewness_cols = num_stats[
        (num_stats["skew"] > 1) | (num_stats["skew"] < -1)
    ].index.tolist()

    for col in high_skewness_cols:
        lower_bound = df[col].quantile(0.01)
        upper_bound = df[col].quantile(0.99)

        # Log the number of rows to be removed
        num_rows_before = df.shape[0]
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
        num_rows_after = df.shape[0]
        helpers.log_info(
            f"Trimmed {num_rows_before - num_rows_after} rows from column '{col}' due to high skewness."
        )

    return df

def trim_high_kurtosis(df, num_stats):
    """
    Remove 1 from each end of the distribution for columns with high kurtosis (> 3)
    """

    high_kurtosis_cols = num_stats[num_stats["kurtosis"] > 3].index.tolist()

    for col in high_kurtosis_cols:
        lower_bound = df[col].quantile(0.01)
        upper_bound = df[col].quantile(0.99)

        # Log the number of rows to be removed
        num_rows_before = df.shape[0]
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
        num_rows_after = df.shape[0]
        helpers.log_info(
            f"Trimmed {num_rows_before - num_rows_after} rows from column '{col}' due to high kurtosis."
        )

    return df


def beauty_fix(df):
    df.streaming_service = df.streaming_service.replace(
        {"I do not use a streaming service.": "Other", "Other streaming service": "Other"}
    )
    helpers.log_info(f"Values in 'streaming_service' column before cleaning: {df.streaming_service.unique()}")


    df.fav_genre = df.fav_genre.replace(
        {"Video game music": "VideoGame", "Hip hop": "HipHop", "K pop": "KPop"}
    )
    helpers.log_info(f"Values in 'fav_genre' column before cleaning: {df.fav_genre.unique()}")

    return df


def all_cleaning(df):
    df = fix_columns(df)
    df = fill_missing_values(df, numerical_col_stats(df), categorical_col_stats(df))
    df = trim_high_skewness(df, numerical_col_stats(df))
    df = trim_high_kurtosis(df, numerical_col_stats(df))
    df = beauty_fix(df)

    return df

# """
# # Saving cleaned data
# """

def save_cleaned_data(df):
    df.to_csv(helpers.CLEAN_DATA_PATH, index=False)
    helpers.log_info(f"Cleaned data saved to {helpers.CLEAN_DATA_PATH}")
