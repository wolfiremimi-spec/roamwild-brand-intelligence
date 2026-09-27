import plotly.graph_objects as go
import streamlit as st
from engine import data, ui

comp = data.competitors(); opp = data.opportunities(); S = data.strategy()
ATTR = {"transformation": "Transformation (functional → transformational)", "personalization": "Personalization (mass → personalized)",
        "adventure": "Adventure intensity", "curation": "Curation", "community": "Community", "sustainability": "Sustainability",
        "digital": "Digital experience", "price_position": "Price position"}
TARGET_PT = {"transformation": 8, "personalization": 8, "adventure": 7}   # Restorative Adventure point tested in the case study
OWNS = {"Traditional tour operators": "Reassurance", "Adventure travel specialists": "Expertise", "Premium travel planners": "Luxury & exclusivity",
        "Wellness travel companies": "Rest", "Travel marketplaces": "Price & choice", "Independent planning": "Freedom", "ROAMWILD today": "Not yet defined"}

ui.header("05", "Competitive whitespace", "Each category has earned a clear territory. No one yet combines challenge and recovery.",
          "Category archetypes scored 1-10 on eight attributes. Change the axes to explore the landscape.")
st.markdown(ui.tag("INTERPRETATION") + " Scores are analyst judgments about category archetypes, not ratings of individual companies.", unsafe_allow_html=True)

a, b = st.columns(2)
xk = a.selectbox("Horizontal axis", list(ATTR), index=0, format_func=lambda k: ATTR[k])
yk = b.selectbox("Vertical axis", list(ATTR), index=1, format_func=lambda k: ATTR[k])

fig = go.Figure()
has_target = xk in TARGET_PT and yk in TARGET_PT and xk != yk
if has_target:
    fig.add_shape(type="rect", x0=6.6, x1=10.4, y0=6.6, y1=10.4, fillcolor=ui.SKY, opacity=.45, line_width=0, layer="below")
    fig.add_annotation(x=10.3, y=10.3, text="<b>RESTORATIVE ADVENTURE</b><br>whitespace", showarrow=False, xanchor="right", yanchor="top", font=dict(color=ui.NAVY, size=11), align="right")
others = comp[comp["competitor"] != "ROAMWILD today"]
fig.add_scatter(x=others[xk], y=others[yk], mode="markers+text", text=others["competitor"], textposition="bottom center", name="Competitor categories",
                marker=dict(size=16, color=ui.GRAY, line=dict(width=2, color="#fff")), textfont=dict(size=11, color=ui.MUTE),
                customdata=others[["value_proposition", "emotional_territory"]].values,
                hovertemplate="<b>%{text}</b><br>%{customdata[0]}<br>Emotional territory: %{customdata[1]}<extra></extra>")
rt = comp[comp["competitor"] == "ROAMWILD today"].iloc[0]
fig.add_scatter(x=[rt[xk]], y=[rt[yk]], mode="markers+text", text=["ROAMWILD today"], textposition="bottom center", name="ROAMWILD today",
                marker=dict(size=18, color=ui.BLUE, line=dict(width=2, color="#fff")), textfont=dict(color=ui.BLUE, size=12))
if has_target:
    tx, ty = TARGET_PT[xk], TARGET_PT[yk]
    fig.add_annotation(x=tx, y=ty, ax=rt[xk], ay=rt[yk], xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=3, arrowwidth=2, arrowcolor=ui.NAVY, opacity=.8)
    fig.add_scatter(x=[tx], y=[ty], mode="markers+text", text=["ROAMWILD target"], textposition="top left", name="ROAMWILD target",
                    marker=dict(size=22, color=ui.NAVY, line=dict(width=2, color="#fff")), textfont=dict(color=ui.NAVY, size=12))
fig.update_layout(height=560, xaxis=dict(title=ATTR[xk], range=[0, 10.5], dtick=2), yaxis=dict(title=ATTR[yk], range=[0, 10.5], dtick=2),
                  legend=dict(orientation="h", y=-0.13), margin=dict(t=20, b=40))
st.plotly_chart(fig, use_container_width=True)
if not has_target:
    st.caption("The proposed position is defined on transformation, personalization and adventure; choose two of those axes to see it.")

c1, c2 = st.columns([1, 1.1])
with c1:
    st.markdown("#### What each category is known for")
    st.markdown('<table class="rw-table"><tr><th>Category</th><th>Value proposition</th><th>Known for</th></tr>' + "".join(
        f'<tr class="{"hl" if r.competitor == "ROAMWILD today" else ""}"><td><b>{ui.e(r.competitor)}</b></td><td>{ui.e(r.value_proposition)}</td><td>{OWNS[r.competitor]}</td></tr>'
        for r in comp.itertuples()) + "</table>", unsafe_allow_html=True)
with c2:
    o = opp.sort_values("weighted_score")
    fig = go.Figure(go.Bar(x=o["weighted_score"], y=o["territory"], orientation="h", text=[f"{v:.2f}" for v in o["weighted_score"]], textposition="outside",
                           marker_color=[ui.NAVY if t == "Restorative Adventure" else ui.GRAY for t in o["territory"]],
                           customdata=o[["description"]].values, hovertemplate="<b>%{y}</b><br>%{customdata[0]}<br>Score %{x:.2f}<extra></extra>"))
    fig.update_layout(title="Opportunity territories, weighted score (0-10)", height=320, xaxis_range=[0, 10])
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Scored on desirability, differentiation, feasibility, credibility, revenue potential and defensibility (weights 20/20/15/15/20/10).")

st.markdown("#### The territory")
t = st.columns([1, 1, 1, 1.3])
for col, (lab, txt) in zip(t, [("Real challenge", "Physically meaningful days, not a soft retreat"), ("Real recovery", "Rest designed into every day, never an add-on"),
                               ("Personal fit", "Matched to the traveler's fitness and pace")]):
    with col: ui.card(lab, txt)
with t[3]: ui.card("= Restorative Adventure", "Not expedition-grade adventure. Not a rest-only retreat. Not bespoke luxury.", dark=True)

w3 = S["whitespace_3d"]
ui.why(f"Distance to the nearest competitor on transformation, personalization and adventure: Restorative Adventure {w3['Restorative Adventure point (8,8,7)']:.2f} vs ROAMWILD today {w3['ROAMWILD today (5,4,6)']:.2f}. The territory scores {opp['weighted_score'].max():.2f} of 10, well ahead of the next ({opp['weighted_score'].nlargest(2).iloc[-1]:.2f}).",
       "Specialists are known for challenge and wellness companies for rest. The combination, personalized, is open.",
       "Competing on another category's home ground favors the incumbents; the open space favors a focused brand.",
       "Move ROAMWILD from a broad position to Restorative Adventure.")
ui.footer("Competitive scores describe category archetypes, not companies.")
