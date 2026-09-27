# ROAMWILD Brand Intelligence Engine

**Turning customer, competitive and financial intelligence into brand decisions.**

An interactive brand-strategy application built by **Amelia Wolfire** to accompany the ROAMWILD brand strategy case study.
It shows how a strategist moves from evidence to a decision: who to serve, where to compete, what to stand for, and what that choice is worth.

> **Data disclosure.** ROAMWILD is a fictional adventure-travel company. The customer data are **synthetic** (1,500 generated customers).
> Financial outputs are **modeled scenarios**, not forecasts. Market context in the case study cites published sources.

**Live app:** _link added after deployment_ · **Case study:** [`case-study/ROAMWILD_Brand_Strategy_Case_Study.pdf`](case-study/ROAMWILD_Brand_Strategy_Case_Study.pdf) · **Decision model:** [`case-study/ROAMWILD_Decision_Model.xlsx`](case-study/ROAMWILD_Decision_Model.xlsx)

---

## Overview
ROAMWILD runs strong trips for everyone, so it has no distinctive reason to be chosen, and it buys most of its growth through paid media.
The analysis finds that one segment, **Restorative Adventurers**, is 16% of customers but 42% of lifetime gross profit
(NPS +56, 47% repeat, 15.2x CLV:CAC). The recommendation: own **Restorative Adventure** (real challenge, real recovery, personal fit)
with the promise **"Come back challenged and restored."**

## Business question
> Where should ROAMWILD compete, who should it prioritize, what should it stand for, and how could that choice create measurable growth?

## Strategic approach
```
Customer data → Segment intelligence → Customer economics → Target prioritization → Competitive whitespace
→ Positioning → Brand experience → Growth scenarios → Strategic decision
```
Every section ends with **Why this decision?**: Evidence → Insight → Strategic implication → Decision.

## Application features
| Section | What it does |
|---|---|
| 01 Executive Overview | The question, the key discovery, the recommendation and what it is worth, in about 60 seconds |
| 02 Customer Intelligence | Value concentration, CLV:CAC by channel, NPS → repeat, every customer's willingness to pay vs lifetime value |
| 03 Segment Explorer | Select any of the five segments; metrics, needs profile, trip types and channels update |
| 04 Target Prioritization | Eight transparent criteria with adjustable weights; the ranking is recalculated live and can change |
| 05 Competitive Whitespace | Interactive perceptual map with selectable axes; ROAMWILD today → target; territory scores |
| 06 Positioning Strategy | Positioning architecture, statement, brand platform and the trade-offs it forces |
| 07 Brand Experience | Nine-stage journey: need, promise, intervention, KPI and owner at each stage |
| 08 Growth Simulator | The case study's financial model, live: compare Baseline, Strategy case and your own scenario |
| 09 Measurement Framework | Brand, customer, growth, economics and experience metrics, plus the evidence gate for scaling |
| 10 Methodology & Limitations | Data, segmentation, economics, competitive method and limitations |

Evidence labels used throughout: **Source data · Calculated · Interpretation · Hypothesis · Recommendation · Modeled scenario**.

## Methodology
- **Segmentation:** k-means on 10 standardized needs and behavior variables; k = 5 chosen by silhouette (0.226); validated against the generating profiles (adjusted Rand index 0.746).
- **Customer economics:** CLV = booking value × gross margin × booking frequency × Σ repeat-rate^year over 5 years; CAC by acquisition channel.
- **Target prioritization:** 8 weighted criteria (6 calculated, 2 judgment scores with cited rationale); robustness tested with 5 preset weightings and 5,000 random weight sets.
- **Competitive analysis:** six category archetypes scored on eight attributes; whitespace measured as distance to the nearest competitor.
- **Scenario model:** mix-shift growth model with a Signature price tier; stated willingness to pay is discounted (adopters must state ≥1.5× the premium).
  The app's model is a line-for-line port of the case study model and **reproduces its published scenarios exactly** (`tests/test_finance.py`).

Frameworks applied: 5C analysis, segmentation-targeting-positioning, customer lifetime value, economic value to the customer, jobs to be done,
perceptual mapping, brand platform, experience blueprint and scenario modeling.

## Technical architecture
```
roamwild-brand-intelligence/
├── app.py                  # navigation and page setup
├── views/                  # one file per section (01-10)
├── engine/
│   ├── data.py             # loads case-study outputs; weighting and robustness helpers
│   ├── finance.py          # growth scenario model (ported from the case study)
│   └── ui.py               # Coastal Strategy design system, evidence labels, 'Why this decision?' blocks
├── data/                   # case-study outputs: synthetic customers, segment profiles, scores, model inputs
├── case-study/             # case study PDF and Excel decision model
├── methodology/            # methodology notes
├── tests/                  # model reproduces the case study
└── .streamlit/config.toml  # theme
```
Built with Python, Streamlit, pandas, NumPy and Plotly. No machine-learning libraries are needed at runtime; clustering was done in the case study.

## How to run
```bash
pip install -r requirements.txt
streamlit run app.py
python tests/test_finance.py   # optional: checks the model against the case study
```

## Limitations
Synthetic data with designed relationships; moderate segment separation; judgment-based scores (tested for sensitivity); stated willingness to pay;
category archetypes rather than companies; a one-year model with causal links that must be tested; brand and experience baselines are assumptions.
Real-world validation (interviews, a survey, concept and price tests) would come next.

## Portfolio case study
This application accompanies the ROAMWILD brand strategy case study (25 pages plus appendix) and its 23-sheet Excel decision model,
both in [`case-study/`](case-study/).

## About Amelia Wolfire
Brand strategist who combines customer intelligence, business analysis and emerging technology to make stronger strategic decisions.
Focus: brand strategy, customer intelligence and growth strategy in travel, hospitality, outdoor and lifestyle.
