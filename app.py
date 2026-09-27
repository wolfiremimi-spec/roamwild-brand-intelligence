"""ROAMWILD Brand Intelligence Engine: turning customer, competitive and financial intelligence into brand decisions."""
import streamlit as st

st.set_page_config(page_title="ROAMWILD · Brand Intelligence Engine", page_icon="🧭", layout="wide", initial_sidebar_state="expanded")

from engine import ui  # noqa: E402  (after page config)
ui.setup()

pages = {
    "Strategy": [
        st.Page("views/01_overview.py", title="Executive Overview", default=True),
    ],
    "Evidence": [
        st.Page("views/02_customer_intelligence.py", title="Customer Intelligence"),
        st.Page("views/03_segment_explorer.py", title="Segment Explorer"),
        st.Page("views/04_target_prioritization.py", title="Target Prioritization"),
        st.Page("views/05_competitive_whitespace.py", title="Competitive Whitespace"),
    ],
    "Strategy in action": [
        st.Page("views/06_positioning.py", title="Positioning Strategy"),
        st.Page("views/07_brand_experience.py", title="Brand Experience"),
        st.Page("views/08_growth_simulator.py", title="Growth Simulator"),
        st.Page("views/09_measurement.py", title="Measurement Framework"),
    ],
    "About": [
        st.Page("views/10_methodology.py", title="Methodology & Limitations"),
    ],
}
nav = st.navigation(pages)
with st.sidebar:
    st.markdown("**ROAMWILD**  \nBrand Intelligence Engine")
    st.caption("Fictional company · synthetic customer data · modeled scenarios")
    st.caption("Built by Amelia Wolfire, brand strategist")
nav.run()
