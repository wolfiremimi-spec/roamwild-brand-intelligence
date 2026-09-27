"""Presentation helpers: Coastal Strategy palette, CSS, evidence labels and the 'Why this decision?' block."""
import html
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

NAVY, BLUE, SKY, ICE, WHITE, CHAR = "#16324F", "#477FA8", "#BFD9E8", "#F2F7FA", "#FFFFFF", "#29343D"
GRAY, LINE, MUTE = "#C9D5DF", "#DDE5EC", "#5B6873"
TARGET, SECOND = "Restorative Adventurers", "Purposeful Explorers"
SEG_ORDER = ["Restorative Adventurers", "Purposeful Explorers", "Experience Collectors", "Budget Social Travelers", "Adventure Purists"]
# Emphasis encoding, not a rainbow: primary target navy, secondary coastal blue, others recede.
SEG_COLOR = {"Restorative Adventurers": NAVY, "Purposeful Explorers": BLUE, "Experience Collectors": "#9DB9CF",
             "Budget Social Travelers": GRAY, "Adventure Purists": "#DCE5EC"}
FONT = "Inter, 'Helvetica Neue', Arial, sans-serif"

pio.templates["roamwild"] = go.layout.Template(data=dict(bar=[go.Bar(cliponaxis=False)]), layout=go.Layout(
    font=dict(family=FONT, color=CHAR, size=13), paper_bgcolor=WHITE, plot_bgcolor=WHITE,
    colorway=[NAVY, BLUE, "#9DB9CF", GRAY], margin=dict(l=10, r=30, t=56, b=10),
    xaxis=dict(gridcolor=LINE, zeroline=False, linecolor=LINE, tickfont=dict(color=MUTE), automargin=True),
    yaxis=dict(gridcolor=LINE, zeroline=False, linecolor=LINE, tickfont=dict(color=MUTE), automargin=True),
    hoverlabel=dict(bgcolor=WHITE, bordercolor=LINE, font=dict(color=CHAR, family=FONT)),
    legend=dict(orientation="h", yanchor="top", y=-0.2, x=0, font=dict(color=MUTE)),
    title=dict(font=dict(size=14, color=NAVY), x=0, xanchor="left")))
pio.templates.default = "roamwild"

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"], .stMarkdown, .stText {{ font-family: {FONT}; color: {CHAR}; }}
.block-container {{ padding-top: 2.2rem; max-width: 1180px; }}
h1, h2, h3 {{ color: {NAVY} !important; letter-spacing: -0.01em; }}
[data-testid="stSidebar"] {{ background: {ICE}; border-right: 1px solid {LINE}; }}
[data-testid="stMetric"] {{ background: {WHITE}; border-top: 3px solid {NAVY}; padding: 10px 14px 12px; }}
[data-testid="stMetricLabel"] p {{ font-size: 0.72rem !important; letter-spacing: .12em; text-transform: uppercase; color: {MUTE} !important; font-weight: 600; }}
[data-testid="stMetricValue"] {{ color: {NAVY}; font-weight: 700; }}
.rw-kicker {{ font-size: .72rem; font-weight: 700; letter-spacing: .18em; text-transform: uppercase; color: {BLUE}; margin-bottom: .2rem; }}
.rw-title {{ font-size: 2.05rem; line-height: 1.15; font-weight: 700; color: {NAVY}; margin: 0 0 .35rem; max-width: 30ch; }}
.rw-sub {{ font-size: 1.02rem; color: {MUTE}; margin-bottom: 1.1rem; max-width: 70ch; }}
.rw-tag {{ display: inline-block; font-size: .64rem; font-weight: 700; letter-spacing: .08em; padding: 2px 7px; border-radius: 3px; margin: 0 4px 4px 0; vertical-align: middle; white-space: nowrap; }}
.t-src {{ border: 1px solid {BLUE}; color: {BLUE}; }}
.t-calc {{ background: {SKY}; color: {NAVY}; }}
.t-int {{ border: 1px solid {GRAY}; color: {MUTE}; }}
.t-hyp {{ border: 1px dotted {MUTE}; color: {MUTE}; }}
.t-rec {{ background: {NAVY}; color: {WHITE}; }}
.t-scn {{ border: 1px dashed {BLUE}; color: {BLUE}; }}
.rw-why {{ border: 1px solid {LINE}; border-radius: 6px; overflow: hidden; margin: 1rem 0 1.4rem; }}
.rw-why-h {{ background: {NAVY}; color: {WHITE}; font-size: .72rem; font-weight: 700; letter-spacing: .18em; padding: 8px 14px; }}
.rw-why-g {{ display: grid; grid-template-columns: repeat(4, 1fr); }}
.rw-why-g > div {{ padding: 12px 14px; border-right: 1px solid {LINE}; background: {ICE}; }}
.rw-why-g > div:last-child {{ border-right: 0; background: {WHITE}; border-left: 3px solid {NAVY}; }}
.rw-why-g b {{ display: block; font-size: .66rem; letter-spacing: .14em; text-transform: uppercase; color: {BLUE}; margin-bottom: 4px; }}
.rw-why-g > div:last-child b {{ color: {NAVY}; }}
.rw-why-g p {{ font-size: .9rem; line-height: 1.45; margin: 0; color: {CHAR}; }}
.rw-card {{ background: {ICE}; border-radius: 6px; padding: 14px 16px; height: 100%; }}
.rw-card b.l {{ display: block; font-size: .66rem; letter-spacing: .14em; text-transform: uppercase; color: {BLUE}; margin-bottom: 4px; }}
.rw-card p {{ margin: 0; font-size: .95rem; line-height: 1.45; }}
.rw-dark {{ background: {NAVY}; color: {WHITE}; border-radius: 6px; padding: 18px 20px; }}
.rw-dark b.l {{ display: block; font-size: .66rem; letter-spacing: .16em; text-transform: uppercase; color: {SKY}; margin-bottom: 6px; }}
.rw-dark p {{ margin: 0; font-size: 1.05rem; line-height: 1.45; color: {WHITE}; }}
.rw-big {{ font-size: 2.2rem; font-weight: 700; line-height: 1.05; color: {NAVY}; }}
.rw-foot {{ margin-top: 2.2rem; padding-top: .7rem; border-top: 1px solid {LINE}; font-size: .78rem; color: {MUTE}; }}
.rw-banner {{ background: {ICE}; border-left: 3px solid {BLUE}; padding: 8px 12px; font-size: .82rem; color: {MUTE}; margin-bottom: 1rem; }}
.rw-table {{ width: 100%; border-collapse: collapse; font-size: .9rem; }}
.rw-table th {{ text-align: left; font-size: .68rem; letter-spacing: .1em; text-transform: uppercase; color: {MUTE}; border-bottom: 2px solid {NAVY}; padding: 6px 8px; }}
.rw-table td {{ padding: 7px 8px; border-bottom: 1px solid {LINE}; vertical-align: top; }}
.rw-table tr.hl td {{ background: {ICE}; }}
@media (max-width: 800px) {{ .rw-why-g {{ grid-template-columns: 1fr; }} .rw-why-g > div {{ border-right: 0; border-bottom: 1px solid {LINE}; }} .rw-title {{ font-size: 1.6rem; }} }}
</style>
"""

TAGS = {"SOURCE DATA": "t-src", "CALCULATED": "t-calc", "INTERPRETATION": "t-int", "HYPOTHESIS": "t-hyp",
        "RECOMMENDATION": "t-rec", "MODELED SCENARIO": "t-scn"}
e = lambda x: html.escape(str(x))


def tag(label: str) -> str:
    return f'<span class="rw-tag {TAGS[label]}">{label}</span>'


def setup():
    st.markdown(CSS, unsafe_allow_html=True)


def header(num: str, kicker: str, title: str, sub: str = ""):
    st.markdown(f'<div class="rw-kicker">{e(num)} · {e(kicker)}</div><div class="rw-title">{e(title)}</div>'
                + (f'<div class="rw-sub">{sub}</div>' if sub else ""), unsafe_allow_html=True)


def why(evidence: str, insight: str, implication: str, decision: str):
    cells = [("Evidence", evidence), ("Insight", insight), ("Strategic implication", implication), ("Decision", decision)]
    st.markdown('<div class="rw-why"><div class="rw-why-h">WHY THIS DECISION?</div><div class="rw-why-g">'
                + "".join(f"<div><b>{a}</b><p>{b}</p></div>" for a, b in cells) + "</div></div>", unsafe_allow_html=True)


def card(label: str, text: str, dark: bool = False):
    cls = "rw-dark" if dark else "rw-card"
    st.markdown(f'<div class="{cls}"><b class="l">{label}</b><p>{text}</p></div>', unsafe_allow_html=True)


def footer(extra: str = ""):
    st.markdown(f'<div class="rw-foot">ROAMWILD is a fictional company. Customer data are synthetic (1,500 generated customers). '
                f'Financial outputs are modeled scenarios, not forecasts. {extra} · Brand strategy case study by Amelia Wolfire.</div>',
                unsafe_allow_html=True)


def usd(v, d=0): return f"${v:,.{d}f}"
def m(v, d=1): return f"${v/1e6:,.{d}f}M"
def pct(v, d=0): return f"{v*100:.{d}f}%"
