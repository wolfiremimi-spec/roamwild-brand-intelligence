"""Checks that the app's model reproduces the case study's published scenarios exactly."""
import json
from pathlib import Path
import pandas as pd
import sys
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT))
from engine import finance as F

def test_reproduces_case_study():
    cust = pd.read_csv(ROOT / "data" / "customers.csv")
    mi = json.loads((ROOT / "data" / "model_inputs.json").read_text())
    ref = pd.read_csv(ROOT / "data" / "financial_scenarios_casestudy.csv").set_index("scenario")
    base = F.run(cust, F.preset(mi, "Baseline"))
    for name in ["Baseline", "Strategy case", "Upside case"]:
        out = F.run(cust, F.preset(mi, name)); cmp = F.compare(base, out)
        for k in ["revenue", "gross_profit", "clv_to_cac", "cac_fully_loaded", "clv_new_customer", "avg_booking_value", "gross_margin", "new_customers"]:
            assert abs(out[k] - ref.loc[name, k]) < 1e-6 * max(1, abs(ref.loc[name, k])), (name, k, out[k], ref.loc[name, k])
        if name != "Baseline":
            for k in ["marketing_roi", "payback_months", "incremental_gross_profit"]:
                assert abs(cmp[k] - ref.loc[name, k]) < 1e-6 * max(1, abs(ref.loc[name, k])), (name, k)

if __name__ == "__main__":
    test_reproduces_case_study(); print("finance model matches the case study: OK")
