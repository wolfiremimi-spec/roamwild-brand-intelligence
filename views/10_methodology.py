import pandas as pd
import streamlit as st
from engine import data, ui

S = data.strategy(); seg = S["segmentation"]; mi = data.model_inputs()["assumptions"]

ui.header("10", "Methodology & limitations", "How this was built, and what it can't tell you",
          "Enough detail for an analytical reviewer to reconstruct every number.")

st.markdown("#### Evidence labels used in the app")
st.markdown(" ".join(ui.tag(t) for t in ui.TAGS) , unsafe_allow_html=True)
st.markdown("""
- **Source data**: the synthetic customer dataset. **Calculated**: metrics computed from it. **Interpretation**: the strategist's judgment.
- **Hypothesis**: an assumption to validate. **Recommendation**: what to do. **Modeled scenario**: an output that depends on assumptions.
""")

t1, t2, t3, t4, t5 = st.tabs(["Data", "Segmentation", "Economics & scenarios", "Competitive & strategic method", "Limitations"])
with t1:
    st.markdown("""
**Synthetic data disclosure.** ROAMWILD is a fictional company. The 1,500 customer records were generated for this case study with
documented relationships (for example, higher income lowers price sensitivity; NPS drives repeat booking; referrals follow a Poisson process).
They illustrate method; they are not observations of real travelers.

**Market context** in the case study cites published sources (Adventure Travel Trade Association, Global Wellness Institute, Outdoor Industry
Association, Booking.com, MMGY). Those facts inform judgment scores; they are not mixed into the customer data.
""")
    st.markdown("**Data dictionary**")
    st.dataframe(data.dictionary(), use_container_width=True, hide_index=True)
with t2:
    sil = seg["silhouette_by_k"]
    st.markdown(f"""
- **Method:** k-means clustering on {len(seg['variables'])} standardized needs and behavior variables: {', '.join(v.replace('_', ' ') for v in seg['variables'])}.
- **Choosing k:** silhouette scores k=4: {sil['4']}, k=5: {sil['5']}, k=6: {sil['6']} → **k = {seg['chosen_k']}**.
- **Validation:** because the data is synthetic, clusters were checked against the generating profiles: adjusted Rand index **{seg['adjusted_rand_index_vs_latent']}**.
- **Caveat:** modest silhouettes are typical of attitudinal data; real survey data may be fuzzier.
""")
    st.dataframe(pd.DataFrame(seg["centroids_z"]).T.round(2), use_container_width=True)
    st.caption("Segment centroids in standard deviations from the average customer.")
with t3:
    st.markdown(f"""
- **CLV** = average booking value × gross margin × booking frequency × Σ repeat-rate^year over {mi['clv_years']} years, undiscounted.
- **CAC** is the synthetic acquisition cost by channel; **fully loaded CAC** adds brand investment.
- **Willingness to pay** is stated, so it is discounted: a customer counts as a likely Signature adopter only if their stated premium is at least
  **{mi['adoption_buffer']}×** the {mi['signature_premium']*100:.0f}% price premium. {mi['tier_cost_of_premium']*100:.0f}% of the premium pays for delivering it.
- **Scenarios** combine sessions, conversion, customer mix, acquisition efficiency, repeat uplift, brand and one-off investment. Gross margin today {mi['gross_margin_base']*100:.0f}%;
  prior-year base {mi['prior_year_customers']:,} customers.
- **Economic value to the customer (EVC)** for a 5-night trip: about {ui.usd(S['evc']['evc'])} vs a {ui.usd(S['evc']['signature_price'])} Signature price.
- The app's model is a line-for-line port of the case study model and reproduces its scenarios exactly (automated test in `tests/`).
""")
    fs = pd.DataFrame(S["fin_sensitivity"]).rename(columns={"case": "Stress test", "revenue_growth": "Revenue growth", "incremental_gross_profit": "Incremental GP",
                                                             "marketing_roi": "Marketing ROI", "payback_months": "Payback (months)"})
    st.dataframe(fs.style.format({"Revenue growth": "{:.1%}", "Incremental GP": "${:,.0f}", "Marketing ROI": "{:.0%}", "Payback (months)": "{:.1f}"}),
                 use_container_width=True, hide_index=True)
with t4:
    st.markdown("""
- **Frameworks applied:** 5C situation analysis; segmentation, targeting and positioning; customer lifetime value; economic value to the customer;
  jobs to be done; perceptual mapping; positioning statement and brand platform; experience blueprint; scenario modeling.
- **Target prioritization:** 8 criteria. Six are min-max scaled from segment data; *growth potential* and *competitive whitespace* are judgment
  scores with a cited rationale. Robustness tested with five preset weightings and 5,000 random weight sets.
- **Competitive analysis:** six category archetypes (not individual companies) scored 1-10 on eight attributes; whitespace measured as distance to
  the nearest competitor.
- **Opportunity territories:** five candidates scored on desirability, differentiation, feasibility, credibility, revenue potential and defensibility.
""")
with t5:
    for l in ["All customer data is synthetic; relationships were designed, not observed.",
              f"Segments are moderately separated (silhouette {seg['silhouette_by_k']['5']}).",
              "Growth-potential, whitespace and territory scores are judgments, tested with sensitivity analysis.",
              "Stated willingness to pay overstates behavior; the adoption buffer is a simple correction.",
              "Competitor scores describe category archetypes, not companies.",
              "The financial model covers one year and assumes causal links (for example, better fit → higher NPS → more repeat) that must be tested.",
              "Brand, experience and satisfaction baselines are assumptions until a brand tracker runs.",
              "Modeled scenarios are not forecasts. Real-world validation (interviews, a survey, concept and price tests) would come next."]:
        st.markdown(f"- {l}")

st.markdown("#### Source files")
st.markdown("Case study PDF and Excel decision model: see the README in the GitHub repository. App code: `engine/` (calculations), `views/` (pages), `data/` (case-study outputs).")
ui.footer()
