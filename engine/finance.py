"""
Growth scenario model, ported line for line from the ROAMWILD case study (models/financial_model.py)
and its Excel decision model (14_FINANCIAL_MODEL). With default inputs it reproduces the case study's
Baseline and Strategy case exactly (see tests/test_finance.py).

Labels: segment economics = SOURCE DATA (synthetic); inputs = ASSUMPTION; outputs = MODELED SCENARIO.
"""
from dataclasses import dataclass, field, replace
import numpy as np
import pandas as pd

SEGMENTS = ["Restorative Adventurers", "Purposeful Explorers", "Experience Collectors", "Budget Social Travelers", "Adventure Purists"]
TARGET = "Restorative Adventurers"


@dataclass(frozen=True)
class Inputs:
    sessions: float
    conversion: float
    cac_efficiency: float          # share by which acquisition cost per customer falls
    repeat_uplift: float           # added to the repeat rate (points, as a fraction)
    brand_investment: float
    strategic_investment: float
    mix: dict | None               # share of new customers by segment; None = today's customer mix
    signature_premium: float = 0.0 # price premium of the Signature tier (0 = not launched)
    gross_margin_base: float = 0.31
    adoption_buffer: float = 1.5
    tier_cost_of_premium: float = 0.35
    prior_year_customers: float = 10_000
    clv_years: int = 5


def segment_table(customers: pd.DataFrame, premium: float, gm_base: float, buffer: float, tier_cost: float) -> pd.DataFrame:
    g = customers.groupby("segment")
    t = pd.DataFrame({
        "baseline_abv": g["avg_booking_value"].mean(),
        "likely_adopter_share": g["wtp_premium_pct"].apply(lambda s: (s >= premium * 100 * buffer).mean()) if premium > 0 else 0.0,
        "repeat_rate": g["repeat_booking"].mean(),
        "booking_frequency": g["booking_frequency"].mean(),
        "cac": g["cac"].mean(),
        "mix_baseline": g.size() / len(customers),
    })
    t["abv_uplift_pct"] = t["likely_adopter_share"] * premium
    t["strategy_abv"] = t["baseline_abv"] * (1 + t["abv_uplift_pct"])
    t["gross_margin_strategy"] = (gm_base + t["likely_adopter_share"] * premium * (1 - tier_cost) / (1 + premium)).clip(upper=0.45)
    return t


def clv(abv, gm, bf, r, years=5):
    r = min(max(r, 0.01), 0.95)
    return abv * gm * bf * (1 - r ** years) / (1 - r)


def run(customers: pd.DataFrame, x: Inputs) -> dict:
    t = segment_table(customers, x.signature_premium, x.gross_margin_base, x.adoption_buffer, x.tier_cost_of_premium)
    mix = (pd.Series(x.mix) if x.mix else t["mix_baseline"]).reindex(t.index).fillna(0)
    mix = mix / mix.sum()
    premium = x.signature_premium > 0
    abv_s = t["strategy_abv"] if premium else t["baseline_abv"]
    gm_s = t["gross_margin_strategy"] if premium else pd.Series(x.gross_margin_base, index=t.index)
    new = x.sessions * x.conversion
    blended_abv = float((mix * abv_s).sum())
    blended_bf = float((mix * t["booking_frequency"]).sum())
    blended_gm = float((mix * abv_s * gm_s).sum() / (mix * abv_s).sum())
    repeat_new = float((mix * t["repeat_rate"]).sum()) + x.repeat_uplift
    repeat_prior = float((t["mix_baseline"] * t["repeat_rate"]).sum()) + x.repeat_uplift
    returning = x.prior_year_customers * repeat_prior
    prior_abv = float((t["mix_baseline"] * abv_s).sum())
    acq_cac = float((mix * t["cac"]).sum()) * (1 - x.cac_efficiency)
    acq_spend = new * acq_cac
    revenue = new * blended_bf * blended_abv + returning * float((t["mix_baseline"] * t["booking_frequency"]).sum()) * prior_abv
    gp = revenue * blended_gm
    marketing = acq_spend + x.brand_investment
    loaded_cac = marketing / new
    clv_new = clv(blended_abv, blended_gm, blended_bf, repeat_new, x.clv_years)
    return {"new_customers": new, "returning_customers": returning, "avg_booking_value": blended_abv, "revenue": revenue,
            "gross_margin": blended_gm, "gross_profit": gp, "acquisition_spend": acq_spend, "acquisition_cac": acq_cac,
            "brand_investment": x.brand_investment, "strategic_investment": x.strategic_investment,
            "marketing_investment": marketing, "cac_fully_loaded": loaded_cac, "repeat_rate_new": repeat_new,
            "clv_new_customer": clv_new, "clv_to_cac": clv_new / loaded_cac, "target_share_of_new": float(mix[TARGET]),
            "conversion": x.conversion}


def compare(base: dict, s: dict) -> dict:
    inc_inv = (s["marketing_investment"] + s["strategic_investment"]) - (base["marketing_investment"] + base["strategic_investment"])
    inc_gp = s["gross_profit"] - base["gross_profit"]
    return {"revenue_growth": s["revenue"] / base["revenue"] - 1, "incremental_revenue": s["revenue"] - base["revenue"],
            "incremental_gross_profit": inc_gp, "incremental_investment": inc_inv,
            "marketing_roi": (inc_gp - inc_inv) / inc_inv if inc_inv > 0 else np.nan,
            "payback_months": inc_inv / (inc_gp / 12) if inc_gp > 0 and inc_inv > 0 else np.nan}


def preset(model_inputs: dict, name: str) -> Inputs:
    a, s = model_inputs["assumptions"], model_inputs["scenarios"][name]
    return Inputs(sessions=s["sessions"], conversion=s["conversion"], cac_efficiency=s["cac_efficiency"], repeat_uplift=s["repeat_uplift"],
                  brand_investment=s["brand_investment"], strategic_investment=s["strategic_investment"], mix=s["mix"],
                  signature_premium=0.0 if name == "Baseline" else a["signature_premium"], gross_margin_base=a["gross_margin_base"],
                  adoption_buffer=a["adoption_buffer"], tier_cost_of_premium=a["tier_cost_of_premium"],
                  prior_year_customers=a["prior_year_customers"], clv_years=a["clv_years"])


def mix_with_target(base_mix: dict, target_share: float) -> dict:
    """Set the target's share of new customers and rescale the other segments proportionally."""
    others = {k: v for k, v in base_mix.items() if k != TARGET}
    tot = sum(others.values())
    out = {k: v / tot * (1 - target_share) for k, v in others.items()}
    out[TARGET] = target_share
    return out
