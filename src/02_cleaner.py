"""# Loading and Renaming columns"""

import pandas as pd

df = pd.read_csv("./data/mxmh_survey_results.csv")
df.head(3)

df1 = df.drop(columns=["Timestamp", "Foreign languages", "Permissions", "Exploratory"])
df1.columns

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

df1.head(5)

"""# Setting number series if blank to mean
This includes `age`, `hours_daily`, `bpm`, `*_scr`.
"""

df1.age = df1["age"].fillna(df1["age"].mean())
df1.hours_daily = df1["hours_daily"].fillna(df1["hours_daily"].mean())
df1.bpm = df1["bpm"].fillna(df1["bpm"].mean())
df1.anxiety_scr = df1["anxiety_scr"].fillna(df1["anxiety_scr"].mean())
df1.depression_scr = df1["depression_scr"].fillna(df1["depression_scr"].mean())
df1.insomnia_scr = df1["insomnia_scr"].fillna(df1["insomnia_scr"].mean())
df1.ocd_scr = df1["ocd_scr"].fillna(df1["ocd_scr"].mean())

# Test before proceding
assert df1.age.isna().sum() == 0
assert df1.hours_daily.isna().sum() == 0
assert df1.bpm.isna().sum() == 0
assert df1.anxiety_scr.isna().sum() == 0
assert df1.depression_scr.isna().sum() == 0
assert df1.insomnia_scr.isna().sum() == 0
assert df1.ocd_scr.isna().sum() == 0

"""# Filling NAs of Yes and Nos if any Na
This includes `listen_on_work`, `is_instrumentalist`, `is_composer`.
"""

df1.listen_on_work = df1["listen_on_work"].fillna("No")
df1.is_instrumentalist = df1["is_instrumentalist"].fillna("No")
df1.is_composer = df1["is_composer"].fillna("No")

# Test
assert df1.listen_on_work.isna().sum() == 0
assert df1.is_instrumentalist.isna().sum() == 0
assert df1.is_composer.isna().sum() == 0

"""# Primary Streaming service fix

"""

df1.streaming_service.unique()

df1.streaming_service = df1.streaming_service.replace(
    {"I do not use a streaming service.": "Other", "Other streaming service": "Other"}
)

df1.streaming_service = df1.streaming_service.fillna("Other")

# is subset
assert {"Spotify", "Pandora", "YouTube Music", "Other", "Apple Music"} <= set(
    df1.streaming_service.unique()
)

"""# Favorite Genre"""

df1.fav_genre.unique()

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

"""# Music Effect"""

df1.effect.unique()

df1.effect = df1.effect.fillna("No effect")

# is subset
assert {"No effect", "Improve", "Worsen"} <= set(df1.effect.unique())

"""# Setting frequencies
If na set to Never
"""

df1.fr_classical = df1.fr_classical.fillna("Never")
df1.fr_country = df1.fr_country.fillna("Never")
df1.fr_edm = df1.fr_edm.fillna("Never")
df1.fr_folk = df1.fr_folk.fillna("Never")
df1.fr_gospel = df1.fr_gospel.fillna("Never")
df1.fr_hiphop = df1.fr_hiphop.fillna("Never")
df1.fr_jazz = df1.fr_jazz.fillna("Never")
df1.fr_kpop = df1.fr_kpop.fillna("Never")
df1.fr_latin = df1.fr_latin.fillna("Never")
df1.fr_lofi = df1.fr_lofi.fillna("Never")
df1.fr_metal = df1.fr_metal.fillna("Never")
df1.fr_pop = df1.fr_pop.fillna("Never")
df1.fr_rnb = df1.fr_rnb.fillna("Never")
df1.fr_rap = df1.fr_rap.fillna("Never")
df1.fr_rock = df1.fr_rock.fillna("Never")
df1.fr_videogame = df1.fr_videogame.fillna("Never")
# test
assert df1.fr_classical.isna().sum() == 0
assert df1.fr_country.isna().sum() == 0
assert df1.fr_edm.isna().sum() == 0
assert df1.fr_folk.isna().sum() == 0
assert df1.fr_gospel.isna().sum() == 0
assert df1.fr_hiphop.isna().sum() == 0
assert df1.fr_jazz.isna().sum() == 0
assert df1.fr_kpop.isna().sum() == 0
assert df1.fr_latin.isna().sum() == 0
assert df1.fr_lofi.isna().sum() == 0
assert df1.fr_metal.isna().sum() == 0
assert df1.fr_pop.isna().sum() == 0
assert df1.fr_rnb.isna().sum() == 0
assert df1.fr_rap.isna().sum() == 0
assert df1.fr_rock.isna().sum() == 0
assert df1.fr_videogame.isna().sum() == 0


"""# Loading clean data"""

df1.to_csv("./data/mxmh_survey_results_clean.csv", index=False)
