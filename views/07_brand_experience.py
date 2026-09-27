import streamlit as st
from engine import ui

# Source: ROAMWILD case study, page 17 (brand experience blueprint).
STAGES = [
    ("Discover", "See trips for someone like me", "Challenge and recovery, matched to you", "Stories from real travelers showing both halves of the day", "Target reach; click-through rate", "Marketing"),
    ("Explore", "Compare trips at my level", "Fit first", "Honest effort and recovery ratings on every trip", "Trip page → Fit Profile start", "Product"),
    ("Fit", "Know it fits me", "Fit first", "12-question Fit Profile and pace-group match", "Completion 55%", "Product · Data"),
    ("Book", "Confidence, fair terms", "Recovery included, never upsold", "Transparent Signature pricing showing what recovery includes", "Conversion 0.76%", "Pricing"),
    ("Prepare", "Be ready", "Effort earns rest", "Four-week prep plan by pace group; guide intro call", "Prep plan opened 70%", "CRM · Guides"),
    ("Experience", "Challenge plus recovery, with my people", "Challenged and restored", "Guide pacing standard; daily check-ins; groups of ten or fewer", "Pacing complaints < 5%", "Operations · Guides"),
    ("Reflect", "Make sense of it", "Come back stronger", "Recovery recap and progress summary", "NPS +50 or higher (target segment)", "CRM"),
    ("Return", "Next challenge", "Fit first", "Next trip based on Fit Profile progress", "Cohort repeat 29%", "CRM · Product"),
    ("Advocate", "Share it", "Small by design", "Alumni community; referral credit for pace-matched friends", "Referral share 20%", "Community"),
]
PRIORITY = {"Fit", "Experience"}

ui.header("07", "Brand experience", "The position only works if the experience makes it true",
          "Nine stages from discovery to advocacy. Most of the interventions are operational, not advertising.")
st.markdown(ui.tag("RECOMMENDATION") + " KPI targets are assumptions to be validated.", unsafe_allow_html=True)

names = [s[0] for s in STAGES]
pick = st.select_slider("Journey stage", options=names, value="Experience")
st.markdown('<div style="display:flex;gap:4px;margin:.3rem 0 1rem">' + "".join(
    f'<div style="flex:1;text-align:center;padding:8px 2px;border-radius:4px;font-size:.78rem;font-weight:600;'
    f'background:{ui.NAVY if n == pick else (ui.SKY if n in PRIORITY else ui.ICE)};color:{"#fff" if n == pick else ui.NAVY}">{n}</div>' for n in names) + "</div>",
    unsafe_allow_html=True)
st_, need, promise, action, kpi, owner = STAGES[names.index(pick)]
c = st.columns(4)
with c[0]: ui.card("Customer need", need)
with c[1]: ui.card("Brand promise", promise)
with c[2]: ui.card("Intervention", action, dark=True)
with c[3]: ui.card("KPI · owner", f"{kpi}<br><span style='color:{ui.MUTE};font-size:.85rem'>{owner}</span>")

st.markdown("#### The full blueprint")
st.markdown('<table class="rw-table"><tr><th>Stage</th><th>Customer need</th><th>Brand promise</th><th>Intervention</th><th>KPI</th><th>Owner</th></tr>' + "".join(
    f'<tr class="{"hl" if s[0] in PRIORITY else ""}"><td><b>{s[0]}</b></td><td>{s[1]}</td><td>{s[2]}</td><td>{s[3]}</td><td>{s[4]}</td><td>{s[5]}</td></tr>' for s in STAGES)
    + "</table>", unsafe_allow_html=True)
owners = sorted({o.strip() for s in STAGES for o in s[5].split("·")})
st.caption(f"Owners are the strategist's proposed assignment. Teams involved: {', '.join(owners)}. Only one of nine stages is owned by marketing alone.")

st.markdown("#### Three priority changes: the operating proof of the positioning")
p = st.columns(3)
for col, (a, b) in zip(p, [("01 · Fit Profile", "Matches every traveler to a trip and a level before they book. Proves “fit first.”"),
                           ("02 · Pace-matched groups", "Ten or fewer, grouped by pace. Proves “small by design” and removes the #1 pain."),
                           ("03 · Guide pacing + recovery standard", "Certification and a set ratio of effort to recovery days. Proves “challenged and restored.”")]):
    with col: ui.card(a, b, dark=True)

ui.why("The top customer pains are mismatched pace, vague difficulty ratings and trips that are either too hard or too soft.",
       "The promise lives or dies in operations: fit, pacing and recovery, not advertising.",
       "Brand strategy must change the product, guide standards and CRM, not just the campaign.",
       "Build the Fit Profile, pace-matched groups and the guide recovery standard before scaling spend.")
ui.footer()
