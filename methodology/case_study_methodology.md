> Copied from the ROAMWILD case study project; file paths refer to that project's models. In this app, the scenario model lives in `engine/finance.py`.

# Methodology

The case study applies standard strategy and marketing frameworks in sequence. The brand strategy is the output of the analysis, not the starting point.

## Frameworks applied

| Framework | What it covers | Where it is used |
|---|---|---|
| 5C analysis | Customer, company, competition, collaborators, context | Gate 02 market landscape |
| Customer analysis and customer lifetime value (CLV) | Who creates value and how much over time | Gates 03, 04 and 11 |
| Segmentation, targeting and positioning (STP) | Group customers by needs, choose whom to serve, decide what to stand for | Gates 04 and 08 |
| Strategic positioning and trade-offs | Create value differently from rivals; avoid being stuck in the middle; find white space; choose activities that fit together | Gates 05, 06 and 08 |
| Unique value proposition | Three choices: which customers, which needs, what relative price | Gate 08 |
| Value stick and willingness to pay | Value created between customer willingness to pay and supplier cost | Gates 07 and 11 |
| Economic value to the customer (EVC) | Reference value of the next-best alternative, plus and minus differentiation | Gate 07 |
| Brand positioning statement | Target, frame of reference, point of difference, reasons to believe | Gate 08 |
| Brand equity and brand value | Brand health, customer-brand relationships, how brand value turns into business value | Gates 08 and 11 |
| Marketing mix (4Ps) | Product, price, place, promotion | Gate 10 |

## Gate structure
Every gate follows: **question → data → analysis → insight → strategic implication → decision**. If an analysis did not change a decision, it was removed.

| Gate | Question | Method | Output |
|---|---|---|---|
| 01 Business context | What is the business and its problem? | Business model review; baseline KPIs | Problem statement |
| 02 Market & 5C | What does the landscape look like? | 5C analysis (customer, company, competition, collaborators, context) | Top 5 implications |
| 03 Customer intelligence | Who creates value? | Descriptive statistics, percentiles, correlations, cross-tabs, channel economics | Value concentration |
| 04 Segmentation | Which groups exist? | k-means on 10 standardized variables, k = 4-6 by silhouette; weighted attractiveness scoring with sensitivity and 5,000-draw robustness | Primary and secondary target |
| 05 Competitive intelligence | Who else competes? | Category matrix (8 attributes), two perceptual maps | Crowded and open territory |
| 06 Whitespace | Where should we play? | Five territories on six criteria | Selected territory |
| 07 Customer value | What is it worth? | Jobs to be done, value map, EVC, stated WTP with an adoption buffer | Signature price |
| 08 Positioning | What do we stand for? | Positioning statement; UVP (customers, needs, relative price); points of parity/difference | Positioning and platform |
| 09 Experience | How must it change? | 10-stage blueprint | Experience interventions |
| 10 Go-to-market | How do we reach, convert and keep them? | 4Ps, channel funnel, campaign platform, messaging matrix, creative, content calendar, creator brief, lifecycle journeys, channel-level media plan, A/B test sizing (two-proportion power analysis), incrementality design, AI search visibility, measurement stack, roadmap | Marketing plan and budget |
| 11 Economics | Does it pay? | Mix-shift model, CLV, CLV:CAC, ROI, payback, downside tests | Scenarios |
| 12 AI intelligence | How do we keep learning? | Brand intelligence agent prototype with decision rights | Governance |
| 13 Recommendation | What should management do? | Synthesis | Decision |

## Segmentation details
Variables: travel frequency, log annual travel spend, adventure intensity, wellness interest, sustainability importance, community interest, price sensitivity, luxury preference, personalization interest, cultural interest. Standardized with z-scores. Silhouette scores are modest (0.21-0.23), typical for attitudinal data. Because the data is synthetic, recovered segments could be checked against the generating profiles (adjusted Rand index 0.75); this validation is not possible with real data.

## Scoring
Data-driven criteria are min-max scaled to 1-10 across segments. Judgment criteria (growth potential, competitive whitespace, business feasibility, brand credibility, long-term defensibility) carry written rationale, cite external facts where possible, and are tested by changing weights.

## Financial model
New customers = sessions × conversion. The new-customer mix shifts toward the target. Booking value and margin rise only for likely Signature adopters (stated premium at least 1.5× the 12% price premium). Returning customers come from a 10,000-customer prior base. CLV = booking value × gross margin × bookings per year × (1 − r⁵)/(1 − r). Marketing ROI = (incremental gross profit − incremental investment) / incremental investment.

## Marketing model
The media plan allocates the strategy case's acquisition and brand budgets across 14 lines. Each line carries a share of new customers and sessions, so implied CAC and conversion can be compared with the baseline CAC by channel. All totals are checked against the financial model. Test sample sizes use the two-sided two-proportion formula at 5% significance and 80% power; weekly volumes come from the media plan. Tests needing more than a quarter are flagged as underpowered.

## Limitations
1. All customer data is synthetic. Relationships were designed, not observed.
2. Segments are moderately separated; real data may be fuzzier.
3. Several scores are judgments; sensitivity analysis shows how much they matter.
4. Stated willingness to pay overstates real behavior; the adoption buffer is a simple correction.
5. Competitor scores describe category archetypes, not specific companies.
6. The financial model covers one year and assumes causal links (positioning → conversion, mix, retention) that must be tested.
7. Brand metric baselines are assumptions until a brand tracker runs.
8. Creative is concept work; illustrations stand in for photography. Media costs, CPMs and lifecycle targets are assumptions to be replaced with platform data.

## Evidence labels
FACT (cited) · SYNTHETIC (generated data) · ASSUMPTION (analyst input) · JUDGMENT (scored with rationale) · INFERENCE · SCENARIO · RECOMMENDATION.
