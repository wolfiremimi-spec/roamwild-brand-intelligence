import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from engine import data, ui

seg = data.segments().reindex(ui.SEG_ORDER); S = data.strategy(); cust = data.customers()
Z = pd.DataFrame(S["segmentation"]["centroids_z"]).T

ROLE = {"Restorative Adventurers": ("PRIMARY TARGET · INVEST", "Want real challenge and real recovery in the same trip, matched to their fitness. Time-pressed, high income, least price sensitive."),
        "Purposeful Explorers": ("SECONDARY TARGET · ADJACENCY", "Driven by community and sustainability. Served through impact departures and organic, community and PR channels."),
        "Experience Collectors": ("MAINTAIN · DON'T CHASE", "Frequent, high-spending travelers who want rare, polished experiences. Valuable, but premium planners compete hard for them."),
        "Budget Social Travelers": ("MAINTAIN · DON'T CHASE", "The largest segment, most price sensitive and least valuable. Core trips stay available; no discounting to win them."),
        "Adventure Purists": ("MAINTAIN · DON'T CHASE", "Want maximum intensity and self-organize. Adventure specialists and DIY planning serve them well.")}
LABELS = {"travel_frequency": "Travel frequency", "log_annual_spend": "Annual travel spend", "adventure_intensity": "Adventure intensity",
          "wellness_interest": "Wellness interest", "sustainability_importance": "Sustainability", "community_interest": "Community",
          "price_sensitivity": "Price sensitivity", "luxury_preference": "Luxury preference", "personalization_interest": "Personalization",
          "cultural_interest": "Cultural interest"}

ui.header("03", "Segment explorer", "Five segments, with very different needs and economics",
          "Pick a segment to see what it wants, what it is worth, and the role it plays in the strategy.")
choice = st.radio("Segment", ui.SEG_ORDER, horizontal=True, label_visibility="collapsed")
s = seg.loc[choice]; avg = {"nps": S["overall"]["nps"], "avg_clv": S["overall"]["avg_clv"], "repeat_rate": S["overall"]["repeat_rate"],
                            "avg_booking_value": S["overall"]["avg_booking_value"], "clv_to_cac": S["overall"]["clv_to_cac"]}
role, desc = ROLE[choice]
st.markdown(f'<div class="rw-kicker" style="margin-top:.6rem">{role}</div><div style="font-size:1.6rem;font-weight:700;color:{ui.NAVY}">{choice}</div>'
            f'<p style="max-width:70ch;color:{ui.CHAR}">{desc} {ui.tag("INTERPRETATION")}</p>', unsafe_allow_html=True)

c = st.columns(6)
c[0].metric("Share of customers", ui.pct(s["share"]))
c[1].metric("Lifetime gross profit", ui.pct(s["gross_profit_share"]), f"{(s['gross_profit_share'] - s['share'])*100:+.0f} pts vs its size")
c[2].metric("NPS", f"{s['nps']:+.0f}", f"{s['nps'] - avg['nps']:+.0f} vs all")
c[3].metric("Average CLV", ui.usd(s["avg_clv"]), f"{(s['avg_clv']/avg['avg_clv']-1)*100:+.0f}% vs all")
c[4].metric("CLV : CAC", f"{s['clv_to_cac']:.1f}x", f"{s['clv_to_cac'] - avg['clv_to_cac']:+.1f}x vs all")
c[5].metric("Repeat", ui.pct(s["repeat_rate"]), f"{(s['repeat_rate'] - avg['repeat_rate'])*100:+.0f} pts vs all")
st.caption("Deltas compare with all 1,500 customers. " + "Source: synthetic customer data, segment averages.")

c1, c2 = st.columns([1.1, 1])
with c1:
    z = Z.loc[choice].rename(index=LABELS).sort_values()
    fig = go.Figure(go.Bar(x=z.values, y=z.index, orientation="h", marker_color=[ui.NAVY if v > 0 else ui.GRAY for v in z.values],
                           hovertemplate="%{y}: %{x:+.2f} standard deviations vs average<extra></extra>"))
    fig.add_vline(x=0, line_color=ui.MUTE, line_width=1)
    fig.update_layout(title="What makes this segment different (vs the average customer)", height=400, xaxis_title="Standard deviations from average")
    st.plotly_chart(fig, use_container_width=True)
with c2:
    fig = go.Figure(go.Bar(x=seg.index, y=seg["avg_clv"], marker_color=[ui.NAVY if x == choice else ui.GRAY for x in seg.index],
                           text=[ui.usd(v) for v in seg["avg_clv"]], textposition="outside", hovertemplate="%{x}<br>Average CLV $%{y:,.0f}<extra></extra>"))
    fig.update_layout(title="Average CLV, all segments", height=400, xaxis=dict(tickfont=dict(size=10)))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("#### Profile")
p = st.columns(4)
p[0].metric("Median income", ui.usd(s["median_income"]))
p[1].metric("Average age", f"{s['avg_age']:.0f}")
p[2].metric("Avg booking value", ui.usd(s["avg_booking_value"]))
p[3].metric("Stated premium", f"+{s['wtp_premium_pct']:.0f}%")
d = cust[cust["segment"] == choice]
tt = d["preferred_trip_type"].value_counts(normalize=True).head(5)
ch = d["acquisition_channel"].value_counts(normalize=True).head(5)
q1, q2 = st.columns(2)
with q1:
    fig = go.Figure(go.Bar(x=tt.values, y=tt.index, orientation="h", marker_color=ui.BLUE, text=[ui.pct(v) for v in tt.values], textposition="outside"))
    fig.update_layout(title="Preferred trip types", height=260, xaxis_tickformat=".0%", yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)
with q2:
    fig = go.Figure(go.Bar(x=ch.values, y=ch.index, orientation="h", marker_color=ui.BLUE, text=[ui.pct(v) for v in ch.values], textposition="outside"))
    fig.update_layout(title="How they arrived (acquisition channel)", height=260, xaxis_tickformat=".0%", yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

if choice == ui.TARGET:
    ui.why(f"{ui.pct(s['share'])} of customers, {ui.pct(s['gross_profit_share'])} of lifetime gross profit; wellness and personalization interest are the highest of any segment.",
           "They want challenge and recovery together, and they will pay for a trip that fits them.", "A brand built around this need can charge a premium and grow through advocacy.",
           "Primary target: weight acquisition, product and CRM toward them.")
else:
    ui.why(f"{ui.pct(s['share'])} of customers, {ui.pct(s['gross_profit_share'])} of lifetime gross profit, NPS {s['nps']:+.0f}.",
           desc, "Dedicated investment here would dilute focus on the segment the brand can serve better than anyone.",
           role.title().replace(" · ", ": "))
ui.footer()
