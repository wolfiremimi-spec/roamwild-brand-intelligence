import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from engine import data, ui

S = data.strategy(); sc = data.criteria_scores().reindex(ui.SEG_ORDER)
CRIT = S["criteria"]; PRESETS = S["weight_scenarios"]
JUDG = {"Growth potential", "Competitive whitespace"}

ui.header("04", "Target prioritization", "Which segment deserves the investment? Change the weights and see.",
          "Eight criteria, scored 1-10. Six are calculated from the customer data; two are analyst judgments with a cited rationale. "
          "The weights are yours to change; the method does not force a winner.")

for c in CRIT:
    st.session_state.setdefault(f"w_{c}", int(round(PRESETS["Base (brief)"][CRIT.index(c)] * 100)))

def load(name):
    for i, c in enumerate(CRIT): st.session_state[f"w_{c}"] = int(round(PRESETS[name][i] * 100))

st.markdown("**Start from a weighting**")
b = st.columns(len(PRESETS))
for col, name in zip(b, PRESETS):
    col.button(name, on_click=load, args=(name,), use_container_width=True)

left, right = st.columns([1, 1.35])
with left:
    st.markdown("**Criterion weights** (relative; normalized to 100%)")
    w = {}
    for c in CRIT:
        w[c] = st.slider(c + (" · judgment" if c in JUDG else ""), 0, 40, key=f"w_{c}")
    tot = sum(w.values())
with right:
    if tot == 0:
        st.warning("Give at least one criterion some weight.")
        st.stop()
    score = data.weighted_scores(sc[CRIT], w)
    fig = go.Figure(go.Bar(x=score.values, y=score.index, orientation="h", text=[f"{v:.2f}" for v in score.values], textposition="outside",
                           marker_color=[ui.SEG_COLOR[s] if s in (ui.TARGET, ui.SECOND) else ui.GRAY for s in score.index],
                           hovertemplate="%{y}<br>Weighted score %{x:.2f} of 10<extra></extra>"))
    fig.update_layout(title="Weighted attractiveness score (0-10)", height=330, xaxis_range=[0, 10.5], yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)
    winner = score.index[0]
    if winner == ui.TARGET:
        st.markdown(f'<div class="rw-card"><b class="l">Result with your weights</b><p><b>{winner}</b> rank first, {score.iloc[0] - score.iloc[1]:.2f} points ahead of {score.index[1]}.</p></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="rw-dark"><b class="l">Result with your weights</b><p><b>{winner}</b> rank first. With these priorities the case for Restorative Adventurers weakens; '
                    f'this is what a sensitivity test is for.</p></div>', unsafe_allow_html=True)
    rob = S["sensitivity"]
    st.markdown(f"<p style='margin-top:.8rem'>Robustness in the case study: across 5,000 random weight sets, Restorative Adventurers ranked first in "
                f"<b>{ui.pct(rob[ui.TARGET]['Rank #1 in random weightings'], 1)}</b>, and first under all five preset weightings. {ui.tag('CALCULATED')}</p>", unsafe_allow_html=True)

st.markdown("#### Scores behind the ranking " + ui.tag("CALCULATED") + ui.tag("INTERPRETATION"), unsafe_allow_html=True)
show = sc[CRIT].copy(); show.columns = [c + (" (J)" if c in JUDG else "") for c in CRIT]
st.dataframe(show.style.format("{:.1f}"), use_container_width=True)
st.caption("Calculated criteria are min-max scaled from segment averages. (J) = analyst judgment with cited rationale; see below.")
with st.expander("Why the judgment scores are what they are"):
    for crit, rat in S["judgment_rationale"].items():
        st.markdown(f"**{crit}**")
        for sgm, txt in rat.items(): st.markdown(f"- *{sgm}*: {txt}")

ui.why(f"Restorative Adventurers score highest on willingness to pay, lifetime value, brand fit and retention, and rank first under every preset weighting and in {ui.pct(S['sensitivity'][ui.TARGET]['Rank #1 in random weightings'])} of random ones.",
       "The choice does not depend on one convenient set of weights. Holding the other weights in proportion, it flips only when market size carries about 45% or more of the weight, or accessibility about 55% or more.",
       "Resources can shift toward one segment with confidence, while Purposeful Explorers are a credible secondary target.",
       "Concentrate growth around Restorative Adventurers; move them from 16% to 24% of new customers.")
ui.footer()
