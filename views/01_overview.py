import streamlit as st
from engine import data, finance as F, ui

seg = data.segments(); mi = data.model_inputs(); cust = data.customers(); S = data.strategy()
ra = seg.loc[ui.TARGET]
base = F.run(cust, F.preset(mi, "Baseline")); strat = F.run(cust, F.preset(mi, "Strategy case")); cmp = F.compare(base, strat)

ui.header("01", "Executive overview", "Turning customer, competitive and financial intelligence into brand decisions",
          "ROAMWILD is an emerging adventure-travel brand with strong trips and no distinctive reason to be chosen. "
          "This engine shows how the evidence leads to one strategic choice, and what that choice is worth.")
st.markdown('<div class="rw-banner">ROAMWILD is fictional. Customer data are synthetic; financial outputs are modeled scenarios. '
            'Every number here comes from the published case study and its Excel decision model.</div>', unsafe_allow_html=True)

st.markdown("#### The strategic question")
st.markdown(f'<p style="font-size:1.25rem;color:{ui.NAVY};font-weight:600;max-width:60ch;border-left:4px solid {ui.BLUE};padding-left:14px">'
            "Where should ROAMWILD compete, who should it prioritize, what should it stand for, and how could that choice create measurable growth?</p>",
            unsafe_allow_html=True)

st.markdown("#### The key discovery " + ui.tag("SOURCE DATA") + ui.tag("CALCULATED"), unsafe_allow_html=True)
c = st.columns(5)
c[0].metric("Share of customers", ui.pct(ra["share"]))
c[1].metric("Share of lifetime gross profit", ui.pct(ra["gross_profit_share"]))
c[2].metric("NPS", f"{ra['nps']:+.0f}")
c[3].metric("CLV : CAC", f"{ra['clv_to_cac']:.1f}x")
c[4].metric("Stated premium", f"+{ra['wtp_premium_pct']:.0f}%")
st.caption(f"Restorative Adventurers, one of five segments found by k-means clustering in the 1,500-customer synthetic dataset. Repeat rate {ui.pct(ra['repeat_rate'])}.")

st.markdown("#### The recommendation " + ui.tag("RECOMMENDATION"), unsafe_allow_html=True)
cols = st.columns(4)
for col, (lab, txt) in zip(cols, [("Target", "Restorative Adventurers first; Purposeful Explorers second"),
                                   ("Territory", "Restorative Adventure: real challenge + real recovery + personal fit"),
                                   ("Positioning", "Come back challenged and restored."),
                                   ("Experience", "Fit Profile · pace-matched groups of ten or fewer · recovery built into every day")]):
    with col: ui.card(lab, txt, dark=(lab == "Positioning"))

st.markdown("#### What the strategy is worth, year 1 " + ui.tag("MODELED SCENARIO"), unsafe_allow_html=True)
k = st.columns(4)
k[0].metric("Revenue", ui.m(strat["revenue"]), f"{cmp['revenue_growth']*100:+.1f}% vs {ui.m(base['revenue'])}")
k[1].metric("Gross profit", ui.m(strat["gross_profit"], 2), f"+{ui.m(cmp['incremental_gross_profit'], 2)}")
k[2].metric("CLV : CAC", f"{strat['clv_to_cac']:.2f}x", f"from {base['clv_to_cac']:.2f}x")
k[3].metric("Payback", f"{cmp['payback_months']:.1f} months", f"on {ui.m(cmp['incremental_investment'], 2)} incremental", delta_color="off")
st.caption("Scenario estimates from the case study's decision model, not forecasts. Explore the assumptions in the Growth Simulator.")

st.markdown("#### How the decision was made")
steps = ["Customer data", "Segment intelligence", "Customer economics", "Target prioritization", "Competitive whitespace",
         "Positioning", "Brand experience", "Growth scenarios", "Strategic decision"]
st.markdown('<div style="display:flex;flex-wrap:wrap;gap:6px;align-items:center">' + "".join(
    f'<span style="background:{ui.NAVY if i == len(steps)-1 else ui.ICE};color:{"#fff" if i == len(steps)-1 else ui.NAVY};'
    f'padding:7px 11px;border-radius:4px;font-size:.85rem;font-weight:600">{s}</span>' + ("" if i == len(steps)-1 else f'<span style="color:{ui.BLUE};font-weight:700">→</span>')
    for i, s in enumerate(steps)) + "</div>", unsafe_allow_html=True)

ui.why(f"{ui.pct(ra['share'])} of customers create {ui.pct(ra['gross_profit_share'])} of lifetime gross profit, with NPS {ra['nps']:+.0f} and {ui.pct(ra['repeat_rate'])} repeat.",
       "Value is concentrated in travelers who want real challenge and real recovery in the same trip. No competitor category serves that combination.",
       "Competing as a better generic adventure brand spreads investment thin. Focusing on the most valuable need creates a position ROAMWILD can own.",
       "Prioritize Restorative Adventurers and own Restorative Adventure: come back challenged and restored.")
ui.footer()
