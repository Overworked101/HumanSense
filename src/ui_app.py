import sys 
sys.path.insert(0, ".")  

import os  
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import pandas as pd

from fusion_engine import FusionEngine

# ---------------------------------
# Page config
# ---------------------------------
st.set_page_config(
    page_title="HumanSense Movie Recommender",
    layout="centered"
)

# ---------------------------------
# Background styling
# ---------------------------------
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
    }
    .card {
        background-color: rgba(255, 255, 255, 0.08);
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------
# Title
# ---------------------------------
st.title("🎬 HumanSense")
st.subheader("A Human-Centric Movie Recommendation System")

st.markdown(
    """
    **HumanSense** recommends movies based on *why* you want to watch,
    *who* you think you are, and *how much* emotional or cognitive load
    you can handle.
    """
)

# ---------------------------------
# Load data (cached)
# ---------------------------------
@st.cache_data
def load_data():
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_path, "..", "data", "movies_cleaned.csv")
    return pd.read_csv(data_path)

movies_df = load_data()

# ---------------------------------
# Cache engine
# ---------------------------------
@st.cache_resource
def load_engine():
    return FusionEngine()

engine = load_engine()

# ---------------------------------
# Slider label mapping
# ---------------------------------
LABEL_MAP = {
    0.0: "VERY LOW",
    0.25: "LOW",
    0.5: "MEDIUM",
    0.75: "HIGH",
    1.0: "VERY HIGH"
}

# ---------------------------------
# Sidebar inputs
# ---------------------------------
st.sidebar.header("🧠 Your Context")

purpose = st.sidebar.selectbox(
    "Why are you watching a movie?",
    ["RELAX", "UPLIFT", "DISTRACT", "EXPLORE"]
)

purpose_description = st.sidebar.text_area(
    "Describe what you feel like watching",
    "Something light, comforting, and enjoyable"
)

identity = st.sidebar.selectbox(
    "How do you see yourself?",
    ["casual", "artistic"]
)

cognitive_tolerance = st.sidebar.slider(
    "Cognitive / Emotional Tolerance",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.25,
    format=""
)
st.sidebar.caption(f"Selected: **{LABEL_MAP[cognitive_tolerance]}**")

novelty_preference = st.sidebar.slider(
    "Novelty Preference",
    min_value=0.0,
    max_value=1.0,
    value=0.5,
    step=0.25,
    format=""
)
st.sidebar.caption(f"Selected: **{LABEL_MAP[novelty_preference]}**")

top_k = st.sidebar.slider(
    "Number of recommendations",
    min_value=5,
    max_value=15,
    value=10
)

# ---------------------------------
# Recommendation logic
# ---------------------------------
if st.button("🎯 Recommend Movies"):
    with st.spinner("Thinking like a human..."):

        user_profile = {
            "purpose": purpose,
            "purpose_description": purpose_description,
            "identity": identity,
            "cognitive_tolerance": cognitive_tolerance,
            "novelty_preference": novelty_preference
        }

        recommendations = engine.recommend(
            movies_df,
            user_profile,
            top_k=top_k
        )

    st.success("Here are your recommendations 👇")

    for _, row in recommendations.iterrows():
        st.markdown(
            f"""
            <div class="card">
                <h4>🎬 {row['title']}</h4>
                <p><b>Genres:</b> {row['genres']}</p>
                <p><b>HumanSense Score:</b> {row['humanSense_score']:.2f}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        **Interpretation:**  
        These recommendations adapt to your *purpose*, *identity*, and
        *tolerance level*, reflecting a human-aligned decision process.
        """
    )
