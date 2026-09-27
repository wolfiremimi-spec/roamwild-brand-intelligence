> Copied from the ROAMWILD case study project; file paths refer to that project's models. In this app, the scenario model lives in `engine/finance.py`.

# Assumptions

Every assumption is also an editable blue cell in `dashboard/brand_strategy_dashboard.xlsx` (17_ASSUMPTIONS and 14_FINANCIAL_MODEL).

## Synthetic data generation (`models/synthetic_data_generator.py`, seed 42)
- 1,500 customers drawn from six latent profiles; the segmentation model never sees these labels.
- Survey scores are rounded normal draws on a 1-10 scale, clipped.
- **Income → price sensitivity:** price sensitivity is lowered by 0.45 points per standard deviation of log income within a profile (overall r = -0.62).
- **Younger → more social influence:** −0.05 points per year of age above the profile mean.
- **Trip spend** rises with income (elasticity 0.35) and luxury preference (+5% per point).
- **ROAMWILD booking value** ≈ 78% of average trip spend, +3% per point of personalization interest.
- **Satisfaction (NPS 0-10)** = profile fit with today's offer + interaction of personalization interest and planning preference + noise (sd 1.6).
- **Repeat booking** ~ Bernoulli(logistic(−2.0 + 0.7·(NPS−7) + 0.18·(loyalty−5) + 0.12·(community−5))).
- **Engagement and referrals** rise with community interest, social influence and NPS; referrals ~ Poisson.
- **Stated premium** = profile mean − 0.8 × (price sensitivity − 5), clipped to 0-40%.
- **CAC** by channel: paid social $330, paid search $285, marketplace $300, travel advisor $240, creator $210, organic $85, referral $60, email/CRM $40, each × lognormal noise (sd 0.25).
- **CLV** = booking value × 31% gross margin × bookings per year × (1 − r⁵)/(1 − r), r = repeat probability.

## Business and scenario inputs
| Input | Value | Why |
|---|---|---|
| Gross margin today | 31% | Typical for curated small-group trips |
| Prior-year customers | 10,000 | Company scale |
| Signature premium | 12% | Well below the target's mean stated premium (23.7%) |
| Adoption buffer | 1.5x | Stated WTP overstates real WTP |
| Share of premium spent delivering it | 35% | Extra guide time, recovery partners, matching |
| Sessions (baseline / strategy / upside) | 1.05M / 1.00M / 1.06M | Strategy narrows paid reach |
| Conversion | 0.72% / 0.76% / 0.82% | Positioning and Fit Profile |
| Acquisition efficiency | 0% / 5% / 10% | Positioning-led creative |
| Repeat uplift | 0 / +2 pts / +4 pts | Recovery, community, next-level trips |
| Brand investment | $400K / $900K / $1.0M | Roadmap brand initiatives |
| Strategic one-off investment | $0 / $450K / $450K | Fit Profile, guide certification, Signature tier, agent pilot |
| Target share of new customers | 16% / 24% / 30% | Mix shift from targeting |
| EVC components | Lodging $1,650; guide $1,050; recovery $450; transport $300; planning time $900; fit and group +$450; flexibility −$200 | Do-it-yourself reference for a 5-night trip |

## Judgment scores
Growth potential, competitive whitespace, business feasibility, brand credibility, long-term defensibility and competitor attribute scores. Each has a written rationale in `models/opportunity_scoring.py` and the workbook.

## Marketing plan inputs
| Input | Value |
|---|---|
| Paid social · prospecting (Acquisition, Awareness) | 24% of acquisition budget; 14% of new customers; 30% of sessions |
| Paid social · retargeting (Acquisition, Consideration) | 10% of acquisition budget; 7% of new customers; 8% of sessions |
| Paid search (brand + non-brand) (Acquisition, Booking) | 26% of acquisition budget; 18% of new customers; 11% of sessions |
| Creator partnerships (Acquisition, Awareness) | 16% of acquisition budget; 13% of new customers; 14% of sessions |
| Travel advisor commissions (Acquisition, Booking) | 9% of acquisition budget; 6% of new customers; 1% of sessions |
| Marketplace / OTA fees (Acquisition, Booking) | 6% of acquisition budget; 4% of new customers; 3% of sessions |
| Referral credits (Acquisition, Advocacy) | 9% of acquisition budget; 16% of new customers; 5% of sessions |
| Organic content, SEO & AI search (Brand, Consideration) | 26% of brand budget; 16% of new customers; 22% of sessions |
| Lifecycle & CRM (platform, content, SMS) (Brand, Retention) | 14% of brand budget; 6% of new customers; 6% of sessions |
| Brand film & creative production (Brand, Awareness) | 18% of brand budget; 0% of new customers; 0% of sessions |
| PR, media & advisor trips (Brand, Awareness) | 12% of brand budget; 0% of new customers; 0% of sessions |
| Community & alumni events (Brand, Advocacy) | 12% of brand budget; 0% of new customers; 0% of sessions |
| Prep & recovery experience content (Brand, Experience) | 8% of brand budget; 0% of new customers; 0% of sessions |
| Brand tracking & testing tools (Brand, Awareness) | 10% of brand budget; 0% of new customers; 0% of sessions |
| Monthly spend phasing (Jan-Dec) | 6%, 6%, 7%, 10%, 11%, 10%, 9%, 8%, 8%, 8%, 8%, 9% |
| Monthly new-customer phasing | 7%, 7%, 8%, 8%, 10%, 10%, 9%, 8%, 8%, 8%, 8%, 9% |
| Paid social cpm | 14.0 |
| Trip page share of sessions | 0.45 |
| Checkout to booking | 0.35 |
| Email list | 60000 |
| Email sends per week | 1 |
| Promoter share | 0.34 |
| Alpha | 0.05 |
| Power | 0.8 |
| Lifecycle KPI targets | See 13C_LIFECYCLE_CRM |
