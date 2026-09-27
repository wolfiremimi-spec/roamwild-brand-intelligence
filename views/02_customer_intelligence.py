import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from engine import data, ui

seg = data.segments().reindex(ui.SEG_ORDER); S = data.strategy(); cust = data.customers()
ra = seg.loc[ui.TARGET]; O = S["overall"]

ui.header("02", "Customer intelligence", "Customer value is concentrated, and paid media is not the most efficient source of it",
          "What 1,500 synthetic customers reveal about who creates value, who stays and who brings others.")

k = st.columns(5)
k[0].metric("Customers analyzed", f"{len(cust):,}")
k[1].metric("Average CLV (5-yr GP)", ui.usd(O["avg_clv"]))
k[2].metric("NPS, all customers", f"{O['nps']:+.1f}")
k[3].metric("Repeat rate", ui.pct(O["repeat_rate"], 1))
k[4].metric("Top 20% hold", f"{ui.pct(S['top20_clv_share'])} of CLV")
st.markdown(ui.tag("SOURCE DATA") + ui.tag("CALCULATED") + " Synthetic customer records; metrics calculated in the case study.", unsafe_allow_html=True)

c1, c2 = st.columns([1.15, 1])
with c1:
    fig = go.Figure()
    fig.add_bar(name="Share of customers", x=seg.index, y=seg["share"], marker_color=ui.SKY, hovertemplate="%{x}<br>Customers: %{y:.0%}<extra></extra>")
    fig.add_bar(name="Share of lifetime gross profit", x=seg.index, y=seg["gross_profit_share"],
                marker_color=[ui.SEG_COLOR[s] if s in (ui.TARGET, ui.SECOND) else ui.GRAY for s in seg.index],
                hovertemplate="%{x}<br>Lifetime gross profit: %{y:.0%}<extra></extra>", text=[ui.pct(v) for v in seg["gross_profit_share"]], textposition="outside")
    fig.update_layout(title="Who creates value: customers vs lifetime gross profit", barmode="group", bargap=.25, height=380, yaxis_tickformat=".0%",
                      xaxis=dict(tickangle=0, tickfont=dict(size=11)))
    st.plotly_chart(fig, use_container_width=True)
with c2:
    ch = pd.DataFrame(S["channel"]).T.sort_values("clv_to_cac")
    paid = {"Paid social", "Paid search", "Marketplace/OTA"}
    fig = go.Figure(go.Bar(x=ch["clv_to_cac"], y=ch.index, orientation="h",
                           marker_color=[ui.GRAY if c in paid else (ui.NAVY if c in ("Referral", "Email/CRM") else ui.BLUE) for c in ch.index],
                           text=[f"{v:.1f}x" for v in ch["clv_to_cac"]], textposition="outside",
                           customdata=ch[["customers", "avg_cac"]].values, hovertemplate="%{y}<br>CLV:CAC %{x:.1f}x<br>Customers %{customdata[0]}<br>Avg CAC $%{customdata[1]:.0f}<extra></extra>"))
    fig.update_layout(title="Lifetime gross profit per $1 of acquisition cost", height=380, xaxis_title="CLV : CAC")
    st.plotly_chart(fig, use_container_width=True)
    st.caption(f"Gray = paid channels ({ui.pct(S['paid_share'])} of customers). Navy = referral and CRM.")

c3, c4 = st.columns(2)
nb = pd.DataFrame(S["nps_by_band"]).T
with c3:
    fig = go.Figure(go.Bar(x=nb.index, y=nb["repeat"], marker_color=[ui.GRAY, ui.SKY, ui.NAVY], text=[ui.pct(v) for v in nb["repeat"]], textposition="outside",
                           hovertemplate="%{x}<br>Repeat booking: %{y:.0%}<extra></extra>"))
    fig.update_layout(title="Promoters rebook far more often", height=320, yaxis_tickformat=".0%")
    st.plotly_chart(fig, use_container_width=True)
with c4:
    fig = go.Figure()
    for s in ui.SEG_ORDER[::-1]:
        d = cust[cust["segment"] == s]
        fig.add_scatter(x=d["wtp_premium_pct"], y=d["estimated_clv"], mode="markers", name=s, marker=dict(color=ui.SEG_COLOR[s], size=6, opacity=.75, line=dict(width=.5, color="#fff")),
                        hovertemplate=f"{s}<br>Stated premium %{{x:.0f}}%<br>CLV $%{{y:,.0f}}<extra></extra>")
    fig.update_layout(title="Each customer: willingness to pay vs lifetime value", height=320, xaxis_title="Stated premium for the right trip (%)",
                      yaxis_title="CLV ($, 5-yr gross profit)", legend=dict(font=dict(size=10), y=-0.3))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("#### Segment economics " + ui.tag("SOURCE DATA") + ui.tag("CALCULATED"), unsafe_allow_html=True)
tbl = pd.DataFrame({"Customers": seg["share"].map(ui.pct), "Lifetime gross profit": seg["gross_profit_share"].map(ui.pct), "NPS": seg["nps"].map(lambda v: f"{v:+.0f}"),
                    "Avg CLV": seg["avg_clv"].map(ui.usd), "Avg CAC": seg["avg_cac"].map(ui.usd), "CLV : CAC": seg["clv_to_cac"].map(lambda v: f"{v:.1f}x"),
                    "Avg booking": seg["avg_booking_value"].map(ui.usd), "Repeat": seg["repeat_rate"].map(ui.pct), "Stated premium": seg["wtp_premium_pct"].map(lambda v: f"+{v:.0f}%")})
st.dataframe(tbl, use_container_width=True)

ui.why(f"Top 20% of customers hold {ui.pct(S['top20_clv_share'])} of lifetime value. Promoters rebook at {ui.pct(nb.loc['Promoter 9-10', 'repeat'])} vs {ui.pct(nb.loc['Detractor 0-6', 'repeat'], 1)} for detractors. Referral returns {S['channel']['Referral']['clv_to_cac']:.0f}x its acquisition cost; paid channels about 3x.",
       "Growth is bought, not earned. The customers who become advocates are the cheapest to acquire and the most valuable to keep.",
       "The goal is not simply more customers; it is more of the customers who become valuable advocates.",
       "Segment the base by value and advocacy, not demographics, and let the most valuable segment set the brand's priorities.")
ui.footer("Correlation, not proof of causation.")
