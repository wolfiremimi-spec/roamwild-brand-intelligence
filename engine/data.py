"""Loads the case-study outputs in data/. All values originate in the ROAMWILD case study models."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
import streamlit as st

DATA = Path(__file__).resolve().parents[1] / "data"


@st.cache_data
def customers() -> pd.DataFrame:
    return pd.read_csv(DATA / "customers.csv")


@st.cache_data
def segments() -> pd.DataFrame:
    return pd.read_csv(DATA / "segment_profiles.csv").set_index("segment")


@st.cache_data
def criteria_scores() -> pd.DataFrame:
    return pd.read_csv(DATA / "segment_criteria_scores.csv").set_index("segment")


@st.cache_data
def competitors() -> pd.DataFrame:
    return pd.read_csv(DATA / "competitors.csv")


@st.cache_data
def opportunities() -> pd.DataFrame:
    return pd.read_csv(DATA / "opportunities.csv")


@st.cache_data
def strategy() -> dict:
    return json.loads((DATA / "strategy.json").read_text())


@st.cache_data
def model_inputs() -> dict:
    return json.loads((DATA / "model_inputs.json").read_text())


@st.cache_data
def dictionary() -> pd.DataFrame:
    return pd.read_csv(DATA / "data_dictionary.csv")


def weighted_scores(scores: pd.DataFrame, weights: dict) -> pd.Series:
    w = pd.Series(weights, dtype=float)
    w = w / w.sum() if w.sum() > 0 else w
    return (scores[w.index] * w).sum(axis=1).sort_values(ascending=False)


@st.cache_data
def random_weight_robustness(scores: pd.DataFrame, n: int = 5000, seed: int = 7) -> pd.Series:
    """Share of random weight sets (Dirichlet, all criteria > 0) in which each segment ranks first."""
    rng = np.random.default_rng(seed)
    W = rng.dirichlet(np.ones(scores.shape[1]), n)
    winners = scores.index[np.argmax(scores.values @ W.T, axis=0)]
    return pd.Series(winners).value_counts(normalize=True).reindex(scores.index, fill_value=0)
