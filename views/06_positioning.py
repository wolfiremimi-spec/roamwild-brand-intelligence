import streamlit as st
from engine import data, ui

S = data.strategy(); P = S["positioning"]; PL = S["platform"]

ui.header("06", "Positioning strategy", "Own one idea no competitor can claim",
          "The positioning architecture: every layer traces back to the customer evidence and the whitespace.")
st.markdown(f'<div style="font-size:2.6rem;font-weight:700;line-height:1.05;color:{ui.NAVY};margin:.4rem 0 1rem">Come back <span style="color:{ui.BLUE}">challenged</span><br>and restored.</div>',
            unsafe_allow_html=True)

layers = [("Target", P["Target audience"]), ("Customer need", P["Customer need"]), ("Frame of reference", P["Frame of reference"]),
          ("Differentiation", P["Points of difference"]), ("Reasons to believe", P["Reasons to believe"]), ("Brand promise", P["Brand promise"])]
st.markdown("#### Positioning architecture " + ui.tag("RECOMMENDATION"), unsafe_allow_html=True)
for i, (lab, txt) in enumerate(layers):
    last = i == len(layers) - 1
    st.markdown(f'<div style="display:grid;grid-template-columns:190px 1fr;gap:16px;padding:12px 16px;margin-bottom:6px;border-radius:5px;'
                f'background:{ui.NAVY if last else ui.ICE};color:{"#fff" if last else ui.CHAR}">'
                f'<div style="font-size:.7rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:{ui.SKY if last else ui.BLUE}">{i+1:02d} · {lab}</div>'
                f'<div style="font-size:{"1.15rem;font-weight:700" if last else ".98rem"}">{ui.e(txt)}</div></div>', unsafe_allow_html=True)

st.markdown("#### Positioning statement")
stmt = ui.e(S["positioning_statement"])
for w in ["FOR ", "WHO ", "ROAMWILD IS ", "THAT ", "BECAUSE "]:
    stmt = stmt.replace(w, f'<b style="color:{ui.BLUE};font-size:.8rem;letter-spacing:.08em">{w}</b>')
st.markdown(f'<div style="border-left:4px solid {ui.NAVY};background:{ui.ICE};padding:14px 18px;font-size:1.02rem;line-height:1.6;color:{ui.NAVY}">{stmt}</div>', unsafe_allow_html=True)

st.markdown("#### Brand platform")
c = st.columns(3)
for col, (lab, k) in zip(c * 2, [("Purpose", "Brand purpose"), ("Vision", "Brand vision"), ("Mission", "Brand mission"), ("Personality", "Brand personality"),
                                   ("Value proposition", "Value proposition"), ("Points of parity", "Points of parity")]):
    with col:
        ui.card(lab, ui.e(PL.get(k, P.get(k, ""))))
        st.write("")

st.markdown("#### A position is only a strategy if it forces choices")
w1, w2 = st.columns(2)
with w1:
    ui.card("ROAMWILD will", "Serve Restorative Adventurers first · Match every traveler with a Fit Profile · Cap every group at ten · "
            "Include recovery in every itinerary · Charge a premium justified by value (+12% Signature tier)")
with w2:
    ui.card("ROAMWILD will not", "Compete on price for budget group travel · Run groups larger than ten · Sell expedition-grade technical trips · "
            "Sell recovery as an optional add-on · Let AI make safety, pricing or positioning decisions", dark=True)

ui.why("The most valuable segment wants challenge and recovery together; no competitor category offers the combination; ROAMWILD's operations can deliver it.",
       "Challenge alone belongs to adventure specialists and recovery alone to wellness companies. The combination, matched to the traveler, is ownable.",
       "The promise must be provable in the product, or it is a slogan.",
       "Position ROAMWILD as the small-group adventure company that matches every trip to your fitness and builds recovery into every day.")
ui.footer()
