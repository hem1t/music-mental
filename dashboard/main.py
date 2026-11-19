from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

from cleaners import all_cleaning, save_cleaned_data
from helpers import *

enable_logging()
sns.set_theme(style="whitegrid")

st.set_page_config(
    page_title="Music and Mental Health",
    page_icon=":musical_note:",
    layout="wide",
)


def clean_and_save_data(force_download=False):
    download_data(force=force_download)
    df = get_uncleaned_data()
    cleaned_df = all_cleaning(df)
    save_cleaned_data(cleaned_df)


@st.cache_data(show_spinner=False)
def load_cleaned_data():
    try:
        return get_cleaned_data()
    except FileNotFoundError:
        log_info("Cleaned data not found. Cleaning and saving data.")
        clean_and_save_data()
        return get_cleaned_data()


def set_loaded_time():
    if "loaded_at" not in st.session_state:
        st.session_state.loaded_at = datetime.now()


def get_effect_palette():
    return {
        "Improve": "#2A9D8F",
        "No effect": "#E9C46A",
        "Worsen": "#E76F51",
    }


@st.cache_resource(show_spinner=True)
def build_effect_distribution(df, normalized):
    counts = df["effect"].value_counts(dropna=False)
    values = counts / counts.sum() if normalized else counts
    fig, ax = plt.subplots(figsize=(7, 4))
    palette = get_effect_palette()
    sns.barplot(
        x=values.index.astype(str),
        y=values.values,
        hue=values.index.astype(str),
        palette=palette,
        legend=False,
        ax=ax,
    )
    ax.set_xlabel("Reported effect")
    ax.set_ylabel("Percentage" if normalized else "Respondents")
    ax.set_title("Distribution of reported music effects")
    if normalized:
        ax.yaxis.set_major_formatter(lambda value, _: f"{value:.0%}")
        for bar, value in zip(ax.patches, values):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                f"{value:.1%}",
                ha="center",
                va="bottom",
            )
    else:
        ax.bar_label(ax.containers[0], fmt="%.0f", padding=3)
    fig.tight_layout()
    return fig


@st.cache_resource(show_spinner=True)
def build_disorder_effect(df, disorders, normalized):
    disorder_columns = {
        "Anxiety": "anxiety_scr",
        "Depression": "depression_scr",
        "Insomnia": "insomnia_scr",
        "OCD": "ocd_scr",
    }
    selected = [name for name in disorders if name in disorder_columns]
    if not selected:
        return None

    averages = pd.DataFrame(
        {
            disorder: df[df["effect"].notna()].groupby("effect")[column].mean()
            for disorder, column in disorder_columns.items()
            if disorder in selected
        }
    )
    if normalized:
        averages = averages / 10
    fig, ax = plt.subplots(figsize=(8, 4))
    averages.plot(kind="bar", ax=ax)
    ax.set_xlabel("Reported effect")
    ax.set_ylabel("Average severity (% of 10-point scale)" if normalized else "Average severity score")
    ax.set_title("Mental-health scores across reported effects")
    if normalized:
        ax.yaxis.set_major_formatter(lambda value, _: f"{value:.0%}")
    for container in ax.containers:
        labels = [
            f"{value:.0%}" if normalized else f"{value:.1f}"
            for value in container.datavalues
        ]
        ax.bar_label(container, labels=labels, padding=2)
    ax.tick_params(axis="x", rotation=0)
    fig.tight_layout()
    return fig


@st.cache_resource(show_spinner=True)
def build_genre_effect(df, top_n):
    genre_columns = [column for column in df.columns if column.startswith("fr_")]
    genre_counts = {}
    for column in genre_columns:
        genre_counts[column] = (
            df[df[column].eq("Very frequently")]["effect"].value_counts()
        )
    genre_effect = pd.DataFrame(genre_counts).fillna(0).T
    genre_effect["total"] = genre_effect.sum(axis=1)
    genre_effect = genre_effect.sort_values("total", ascending=False).head(top_n)
    genre_effect = genre_effect.drop(columns="total")
    genre_effect.index = genre_effect.index.str.removeprefix("fr_").str.replace(
        "_", " ", regex=False
    ).str.title()

    fig, ax = plt.subplots(figsize=(8, 5))
    genre_effect.plot(kind="bar", stacked=True, ax=ax, color=get_effect_palette())
    ax.set_xlabel("Genre")
    ax.set_ylabel("Very-frequent listeners")
    ax.set_title("Reported effects among frequent genre listeners")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    return fig


@st.cache_resource(show_spinner=True)
def build_age_effect(df, bin_count, normalized):
    valid = df.dropna(subset=["age", "effect"]).copy()
    age_edges = pd.cut(valid["age"], bins=bin_count, retbins=True, include_lowest=True)[1]
    age_labels = [
        f"{int(round(age_edges[index]))}-{int(round(age_edges[index + 1]))}"
        for index in range(len(age_edges) - 1)
    ]
    valid["age_group"] = pd.cut(
        valid["age"],
        bins=bin_count,
        labels=age_labels,
        include_lowest=True,
    )
    table = pd.crosstab(valid["age_group"], valid["effect"], normalize="index" if normalized else False)
    table.index = table.index.astype(str)

    fig, ax = plt.subplots(figsize=(8, 5))
    table.plot(kind="bar", stacked=True, ax=ax, color=get_effect_palette())
    ax.set_xlabel("Age group")
    ax.set_ylabel("Share of respondents" if normalized else "Respondents")
    ax.set_title("Reported effects by age group")
    ax.tick_params(axis="x", rotation=45)
    if normalized:
        ax.yaxis.set_major_formatter(lambda value, _: f"{value:.0%}")
    fig.tight_layout()
    return fig


@st.cache_resource(show_spinner=True)
def build_bpm_effect(df, bin_count, normalized):
    valid = df.dropna(subset=["bpm", "effect"]).copy()
    bpm_edges = pd.cut(valid["bpm"], bins=bin_count, retbins=True, include_lowest=True)[1]
    bpm_labels = [
        f"{int(round(bpm_edges[index]))}-{int(round(bpm_edges[index + 1]))}"
        for index in range(len(bpm_edges) - 1)
    ]
    valid["bpm_group"] = pd.cut(
        valid["bpm"],
        bins=bin_count,
        labels=bpm_labels,
        include_lowest=True,
    )
    table = pd.crosstab(valid["bpm_group"], valid["effect"], normalize="index" if normalized else False)
    table.index = table.index.astype(str)

    fig, ax = plt.subplots(figsize=(8, 5))
    table.plot(kind="bar", stacked=True, ax=ax, color=get_effect_palette())
    ax.set_xlabel("BPM group")
    ax.set_ylabel("Share of respondents" if normalized else "Respondents")
    ax.set_title("Reported effects by BPM group")
    ax.tick_params(axis="x", rotation=45)
    if normalized:
        ax.yaxis.set_major_formatter(lambda value, _: f"{value:.0%}")
    fig.tight_layout()
    return fig


df = load_cleaned_data()
set_loaded_time()
build_effect_distribution(df, True)

st.title("Music and Mental Health Survey")

with st.sidebar:
    st.header("Options")
    if st.button("Reload and reclean data", width="stretch"):
        clear_logs()
        try:
            load_cleaned_data.clear()
            st.cache_resource.clear()
            clean_and_save_data(force_download=True)
            df = load_cleaned_data()
            build_effect_distribution(df, True)
            st.session_state.loaded_at = datetime.now()
            st.success("Data reloaded and recleaned.")
        except Exception as exc:
            st.error(f"Reload failed: {exc}")

    if st.button("Reset cache", width="stretch"):
        clear_logs()
        load_cleaned_data.clear()
        st.cache_data.clear()
        st.cache_resource.clear()
        st.session_state.loaded_at = datetime.now()
        st.success("Cache cleared. Data cache will reload.")
        st.rerun()

    if st.button("Clear generated logs", width="stretch"):
        clear_logs()
        st.success("Generated logs cleared.")

    st.divider()
    st.header("Details")
    st.caption("Data loaded")
    st.write(st.session_state.loaded_at.strftime("%Y-%m-%d %H:%M:%S"))
    st.caption("Dataset")
    st.write(f"{df.shape[0]:,} rows x {df.shape[1]:,} columns")
    st.caption("Paths")
    st.code(DATA_PATH)
    st.code(CLEAN_DATA_PATH)

tab_data, tab_visuals, tab_logs = st.tabs(
    ["Cleaned Data", "Visualisations", "Logs"]
)

with tab_data:
    st.subheader("Cleaned dataframe")
    st.caption(f"{df.shape[0]:,} rows and {df.shape[1]:,} columns")
    st.dataframe(df, width="stretch", hide_index=True)

with tab_visuals:
    questions = [
        "What is the effect distribution among listeners?",
        "Does effect vary across mental-health conditions?",
        "How does effect vary by frequently listened genre?",
        "How does effect vary across age groups?",
        "How does effect correlate with BPM?",
    ]

    default_visual_settings = {
        questions[0]: {"normalized": True},
        questions[1]: {
            "disorders": ["Anxiety", "Depression", "Insomnia", "OCD"],
            "normalized": True,
        },
        questions[2]: {"top_n": 8},
        questions[3]: {"bin_count": 5, "normalized": True},
        questions[4]: {"bin_count": 6, "normalized": True},
    }

    if "visual_settings" not in st.session_state:
        st.session_state.visual_settings = default_visual_settings

    question = st.selectbox(
        "Select a question",
        questions,
        key="selected_visual_question",
        accept_new_options=False,
    )

    control_col, visual_col = st.columns([1, 3], gap="large")
    settings = st.session_state.visual_settings.get(
        question,
        default_visual_settings[question],
    )

    with control_col:
        st.subheader("Controls")
        if question.startswith("What is"):
            normalized = st.checkbox(
                "Show percentages",
                value=settings.get("normalized", True),
            )
        elif question.startswith("Does effect"):
            disorders = st.multiselect(
                "Mental-health conditions",
                ["Anxiety", "Depression", "Insomnia", "OCD"],
                default=settings.get(
                    "disorders",
                    ["Anxiety", "Depression", "Insomnia", "OCD"],
                ),
            )
            normalized = st.checkbox(
                "Normalize scores",
                value=settings.get("normalized", True),
            )
        elif question.startswith("How does effect vary by"):
            top_n = st.slider(
                "Number of genres",
                3,
                15,
                settings.get("top_n", 8),
            )
        elif question.startswith("How does effect vary across age"):
            bin_count = st.slider(
                "Age bins",
                2,
                12,
                settings.get("bin_count", 5),
            )
            normalized = st.checkbox(
                "Show percentages",
                value=settings.get("normalized", True),
            )
        else:
            bin_count = st.slider(
                "BPM bins",
                2,
                12,
                settings.get("bin_count", 6),
            )
            normalized = st.checkbox(
                "Show percentages",
                value=settings.get("normalized", True),
            )

        apply_visual = st.button("Apply", type="primary", width="stretch")

    if apply_visual:
        if question.startswith("What is"):
            st.session_state.visual_settings[question] = {
                "normalized": normalized,
            }
        elif question.startswith("Does effect"):
            st.session_state.visual_settings[question] = {
                "disorders": disorders,
                "normalized": normalized,
            }
        elif question.startswith("How does effect vary by"):
            st.session_state.visual_settings[question] = {
                "top_n": top_n,
            }
        elif question.startswith("How does effect vary across age"):
            st.session_state.visual_settings[question] = {
                "bin_count": bin_count,
                "normalized": normalized,
            }
        else:
            st.session_state.visual_settings[question] = {
                "bin_count": bin_count,
                "normalized": normalized,
            }
        st.toast("Visualisation controls applied.")
        settings = st.session_state.visual_settings[question]

    with visual_col:
        if question.startswith("What is"):
            fig = build_effect_distribution(
                df,
                settings.get("normalized", True),
            )
        elif question.startswith("Does effect"):
            fig = build_disorder_effect(
                df,
                settings.get("disorders", []),
                settings.get("normalized", True),
            )
        elif question.startswith("How does effect vary by"):
            fig = build_genre_effect(
                df,
                settings.get("top_n", 8),
            )
        elif question.startswith("How does effect vary across age"):
            fig = build_age_effect(
                df,
                settings.get("bin_count", 5),
                settings.get("normalized", True),
            )
        else:
            fig = build_bpm_effect(
                df,
                settings.get("bin_count", 6),
                settings.get("normalized", True),
            )

        if fig is None:
            st.info("Select at least one mental-health condition.")
        else:
            st.pyplot(fig, width="stretch")

with tab_logs:
    st.subheader("Generated logs")
    log_path = f"{get_data_dir()}/data_cleaning.log"
    try:
        with open(log_path, "r", encoding="utf-8") as log_file:
            log_text = log_file.read()
    except FileNotFoundError:
        log_text = ""

    if log_text:
        st.text_area("data_cleaning.log", log_text, height=500)
        st.download_button(
            "Download log",
            data=log_text,
            file_name="data_cleaning.log",
            mime="text/plain",
        )
    else:
        st.info("No cleaning log entries are available.")