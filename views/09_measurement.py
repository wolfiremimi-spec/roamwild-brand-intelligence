import streamlit as st
from engine import data, finance as F, ui

cust = data.customers(); mi = data.model_inputs(); S = data.strategy()
base = F.run(cust, F.preset(mi, "Baseline")); strat = F.run(cust, F.preset(mi, "Strategy case"))

# Source: case study pages 18-19 / 24 (measurement system). Commercial targets come from the model; brand,
# experience and satisfaction baselines are assumptions until the first brand-tracker wave.
FRAME = {
    "Brand": ("Does the market see us differently?", "ASSUMPTION", [("Aided awareness (target segment)", "11%", "15%"), ("Consideration", "18%", "24%"),
              ("Association with “challenged + restored”", "—", "35%"), ("Share of voice", "4%", "8%"), ("AI answer visibility (25 prompts)", "0%", "20%")]),
    "Customer": ("Do customers behave differently?", "ASSUMPTION", [("Fit Profile completion", "—", "55%"), ("NPS, all customers", f"{S['overall']['nps']:+.0f}", "+20"),
                 ("Referral share of new customers", "14.9%", "20%"), ("Post-trip satisfaction", "4.3", "4.5")]),
    "Growth": ("Is the right growth happening?", "MODEL", [("Target share of new customers", ui.pct(base["target_share_of_new"]), ui.pct(strat["target_share_of_new"])),
               ("Repeat rate, new cohort", ui.pct(base["repeat_rate_new"], 1), ui.pct(strat["repeat_rate_new"], 1)),
               ("Conversion", ui.pct(base["conversion"], 2), ui.pct(strat["conversion"], 2)), ("Revenue", ui.m(base["revenue"]), ui.m(strat["revenue"]))]),
    "Economics": ("Does it pay?", "MODEL", [("Acquisition cost per customer", ui.usd(base["acquisition_cac"]), ui.usd(strat["acquisition_cac"])),
                  ("CLV, new customer", ui.usd(base["clv_new_customer"]), ui.usd(strat["clv_new_customer"])),
                  ("CLV : CAC", f"{base['clv_to_cac']:.2f}x", f"{strat['clv_to_cac']:.2f}x"), ("Gross margin", ui.pct(base["gross_margin"], 1), ui.pct(strat["gross_margin"], 1))]),
    "Experience": ("Is the promise kept?", "ASSUMPTION", [("Pacing complaints (target segment)", "10%", "< 5%"), ("Guide quality rating", "4.5", "4.7"),
                   ("Recovery satisfaction", "—", "4.5"), ("Group satisfaction", "—", "4.5")]),
}

ui.header("09", "Measurement framework", "Measure whether the position changes behavior, not just whether people saw the campaign",
          "Five layers, each answering one management question. Baseline → year-1 target.")
cat = st.radio("Layer", list(FRAME), horizontal=True, label_visibility="collapsed")
q, src, rows = FRAME[cat]
st.markdown(f'<div style="font-size:1.25rem;font-weight:700;color:{ui.NAVY};margin:.4rem 0">{cat}: {q}</div>'
            + (ui.tag("MODELED SCENARIO") + " from the decision model" if src == "MODEL" else ui.tag("HYPOTHESIS") + " baselines and targets to validate with the first tracker wave"),
            unsafe_allow_html=True)
cols = st.columns(len(rows))
for col, (lab, b_, t_) in zip(cols, rows):
    col.metric(lab, t_, f"from {b_}", delta_color="off")

st.markdown("#### How the layers connect")
st.markdown('<div style="display:grid;grid-template-columns:1fr auto 1fr auto 1fr auto 1fr;gap:8px;align-items:center">' + "".join(
    f'<div style="background:{ui.NAVY if i == 3 else ui.ICE};color:{"#fff" if i == 3 else ui.NAVY};padding:12px;border-radius:5px;font-weight:600;font-size:.92rem">{t}</div>'
    + ("" if i == 3 else f'<div style="color:{ui.BLUE};font-weight:700;font-size:1.2rem">→</div>')
    for i, t in enumerate(["Brand perception<br><small>awareness, association</small>", "Customer behavior<br><small>Fit Profile, NPS, referral</small>",
                           "Experience<br><small>pacing, recovery, groups</small>", "Commercial outcomes<br><small>CAC, CLV, margin, revenue</small>"])) + "</div>",
    unsafe_allow_html=True)

st.markdown("#### The evidence gate: scale in Q3 only if")
g = st.columns(4)
for col, (lab, v, sub) in zip(g, [("Target share", "≥ 20%", "of new customers"), ("Signature adoption", "≥ 50%", "of target bookings"),
                                  ("Pacing complaints", "< 5%", "target segment"), ("Acquisition CAC", f"≤ {ui.usd(base['acquisition_cac'])}", "today's level or better")]):
    with col: ui.card(lab, f'<span class="rw-big" style="color:#fff">{v}</span><br>{sub}', dark=True)
p1, p2 = st.columns(2)
with p1: ui.card("Pass → Scale", "Alumni community, referral program, creator scale-up, geo holdout test.")
with p2: ui.card("Fail → Learn + refine", "Find the broken link in the chain before more money follows.")
st.markdown(f'<p style="font-size:1.15rem;font-weight:600;color:{ui.NAVY};border-left:4px solid {ui.BLUE};padding-left:14px;margin-top:1.2rem">'
            "The model does not promise a result. It tells management what has to be true, and how early we can find out.</p>", unsafe_allow_html=True)

ui.why("Stress tests in the case study: each single downside still pays back in 6-8 months, but all four together turn year-1 ROI negative.",
       "The strategy is attractive but depends on a few testable links: target share, Signature adoption and experience quality.",
       "Measuring only reach would miss whether the positioning changes behavior and economics.",
       "Track brand, customer, growth, economics and experience together, and release scale-up funding only through the evidence gate.")
ui.footer()
