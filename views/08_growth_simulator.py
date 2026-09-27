import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from engine import data, finance as F, ui

cust = data.customers(); mi = data.model_inputs()
BASE_MIX = (cust["segment"].value_counts(normalize=True)).to_dict()
base_in = F.preset(mi, "Baseline"); strat_in = F.preset(mi, "Strategy case")
base = F.run(cust, base_in); strat = F.run(cust, strat_in)

ui.header("08", "Growth simulator", "What is the strategy worth, and what has to be true?",
          "The case study's decision model, live. Start from a scenario, change the assumptions, and compare your scenario with the "
          "baseline and the recommended strategy.")
st.markdown('<div class="rw-banner"><b>Modeled scenarios, not forecasts.</b> Segment economics come from the synthetic customer data; every slider is an assumption. '
            'With default settings the model reproduces the case study and Excel model exactly.</div>', unsafe_allow_html=True)

KEYS = ["target_share", "conversion", "sessions", "cac_eff", "repeat_up", "premium", "gm", "brand", "strategic"]
def load(name):
    x = F.preset(mi, name); mix = x.mix or BASE_MIX
    st.session_state.update({"target_share": round(mix[F.TARGET] * 100, 1), "conversion": round(x.conversion * 100, 2), "sessions": x.sessions / 1e6,
                             "cac_eff": round(x.cac_efficiency * 100), "repeat_up": round(x.repeat_uplift * 100, 1), "premium": round(x.signature_premium * 100),
                             "gm": round(x.gross_margin_base * 100), "brand": x.brand_investment / 1e3, "strategic": x.strategic_investment / 1e3,
                             "mix_src": name})
if "target_share" not in st.session_state: load("Strategy case")

b = st.columns([1, 1, 1, 3])
b[0].button("Load baseline", on_click=load, args=("Baseline",), use_container_width=True)
b[1].button("Load strategy case", on_click=load, args=("Strategy case",), use_container_width=True)
b[2].button("Load upside case", on_click=load, args=("Upside case",), use_container_width=True)

l, r = st.columns([1, 1.6])
with l:
    st.markdown("**Customer mix and demand**")
    st.slider("Restorative Adventurers, share of new customers (%)", 5.0, 45.0, step=0.1, key="target_share", help="Other segments scale proportionally.")
    st.slider("Website conversion rate (%)", 0.50, 1.00, step=0.01, key="conversion")
    st.slider("Website sessions (millions)", 0.80, 1.30, step=0.01, key="sessions")
    st.markdown("**Pricing and margin**")
    st.slider("Signature tier price premium (%)", 0, 20, key="premium", help="0 = Signature tier not launched. Only customers whose stated premium is at least 1.5x this price count as adopters.")
    st.slider("Gross margin before the Signature tier (%)", 25, 37, key="gm")
    st.markdown("**Acquisition, retention and investment**")
    st.slider("Acquisition efficiency (% lower cost per customer)", 0, 20, key="cac_eff")
    st.slider("Repeat-rate uplift (points)", 0.0, 6.0, step=0.5, key="repeat_up")
    st.slider("Brand investment ($K)", 0.0, 1500.0, step=25.0, key="brand")
    st.slider("One-off strategic investment ($K)", 0.0, 800.0, step=25.0, key="strategic", help="Fit Profile, guide certification, brand tracker.")

ss = st.session_state
src_mix = F.preset(mi, ss.get("mix_src", "Strategy case")).mix or BASE_MIX
user_in = F.Inputs(sessions=ss.sessions * 1e6, conversion=ss.conversion / 100, cac_efficiency=ss.cac_eff / 100, repeat_uplift=ss.repeat_up / 100,
                   brand_investment=ss.brand * 1e3, strategic_investment=ss.strategic * 1e3, mix=F.mix_with_target(src_mix, ss.target_share / 100),
                   signature_premium=ss.premium / 100, gross_margin_base=ss.gm / 100)
user = F.run(cust, user_in)
cs, cu = F.compare(base, strat), F.compare(base, user)

with r:
    k = st.columns(3)
    k[0].metric("Revenue", ui.m(user["revenue"], 2), f"{cu['revenue_growth']*100:+.1f}% vs baseline")
    k[1].metric("Gross profit", ui.m(user["gross_profit"], 2), f"{ui.m(cu['incremental_gross_profit'], 2)} vs baseline")
    k[2].metric("CLV : CAC", f"{user['clv_to_cac']:.2f}x", f"{user['clv_to_cac'] - base['clv_to_cac']:+.2f}x")
    k = st.columns(3)
    k[0].metric("Acquisition cost / customer", ui.usd(user["acquisition_cac"]), f"{user['acquisition_cac'] - base['acquisition_cac']:+.0f}", delta_color="inverse")
    k[1].metric("Payback", "n/a" if np.isnan(cu["payback_months"]) else f"{cu['payback_months']:.1f} months",
                help="Incremental investment ÷ monthly incremental gross profit, vs baseline.")
    k[2].metric("Marketing ROI, year 1", "n/a" if np.isnan(cu["marketing_roi"]) else ui.pct(cu["marketing_roi"]))

    names = ["Baseline", "Strategy case", "Your scenario"]; runs = [base, strat, user]
    fig = go.Figure()
    fig.add_bar(name="Revenue", x=names, y=[x["revenue"] for x in runs], marker_color=ui.SKY, text=[ui.m(x["revenue"]) for x in runs], textposition="outside")
    fig.add_bar(name="Gross profit", x=names, y=[x["gross_profit"] for x in runs], marker_color=[ui.GRAY, ui.NAVY, ui.BLUE],
                text=[ui.m(x["gross_profit"], 2) for x in runs], textposition="outside")
    fig.update_layout(title="Year-1 revenue and gross profit", barmode="group", height=330, yaxis_tickprefix="$", yaxis_tickformat=".2s")
    st.plotly_chart(fig, use_container_width=True)

rows = [("Share of new customers: Restorative Adventurers", "target_share_of_new", ui.pct), ("New customers", "new_customers", lambda v: f"{v:,.0f}"),
        ("Average booking value", "avg_booking_value", ui.usd), ("Gross margin", "gross_margin", lambda v: ui.pct(v, 1)),
        ("Repeat rate, new cohort", "repeat_rate_new", lambda v: ui.pct(v, 1)), ("CLV, new customer (5-yr GP)", "clv_new_customer", ui.usd),
        ("Acquisition cost per customer", "acquisition_cac", ui.usd), ("Fully loaded CAC", "cac_fully_loaded", ui.usd),
        ("CLV : fully loaded CAC", "clv_to_cac", lambda v: f"{v:.2f}x"), ("Marketing investment", "marketing_investment", lambda v: ui.m(v, 2)),
        ("Revenue", "revenue", lambda v: ui.m(v, 2)), ("Gross profit", "gross_profit", lambda v: ui.m(v, 2))]
tbl = pd.DataFrame({"Baseline": [f(base[k_]) for _, k_, f in rows], "Strategy case": [f(strat[k_]) for _, k_, f in rows],
                    "Your scenario": [f(user[k_]) for _, k_, f in rows]}, index=[a for a, _, _ in rows])
st.markdown("#### Scenario comparison " + ui.tag("MODELED SCENARIO"), unsafe_allow_html=True)
st.dataframe(tbl, use_container_width=True)
st.caption(f"Strategy case: ROI {ui.pct(cs['marketing_roi'])}, payback {cs['payback_months']:.1f} months on {ui.m(cs['incremental_investment'], 2)} incremental investment (case study).")

with st.expander("How the model works"):
    st.markdown("""
- **New customers** = website sessions × conversion rate. Their segment mix follows the slider; other segments scale proportionally.
- **Booking value and margin** rise only for *likely* Signature adopters: customers whose stated premium is at least 1.5× the price premium. 35% of the premium pays for delivering it (extra guide time, recovery partners, fit-matching).
- **Returning customers** come from a 10,000-customer prior-year base at the blended repeat rate.
- **Acquisition cost** is each segment's synthetic average CAC, weighted by mix, reduced by the efficiency slider. **Fully loaded CAC** adds brand investment.
- **CLV** = booking value × gross margin × booking frequency × Σ repeat-rate^year over 5 years (undiscounted).
- **Payback** = incremental investment ÷ (incremental gross profit ÷ 12), vs baseline.
- Code: `engine/finance.py`; a test (`tests/test_finance.py`) confirms it reproduces the case study's scenarios exactly.
""")

ui.why(f"The strategy case lifts gross profit by {ui.m(cs['incremental_gross_profit'], 2)} and CLV:CAC from {base['clv_to_cac']:.2f}x to {strat['clv_to_cac']:.2f}x, mostly by changing who ROAMWILD attracts, not by buying more volume.",
       "Mix and price do most of the work; volume matters less than the kind of customer.",
       "The strategy only pays if the target share, Signature adoption and experience quality actually move. Those are testable before scaling.",
       "Fund the strategy in stages, and scale only when the evidence gate is met (see Measurement).")
ui.footer("All outputs are modeled scenarios.")
