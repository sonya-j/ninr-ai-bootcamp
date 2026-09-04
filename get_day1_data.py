"""Download the UCI Diabetes 130-US Hospitals dataset and create the Day 1 teaching subset."""
from pathlib import Path
import pandas as pd
from ucimlrepo import fetch_ucirepo

out = Path("data")
out.mkdir(exist_ok=True)

diabetes = fetch_ucirepo(id=296)
full = pd.concat([diabetes.data.features, diabetes.data.targets], axis=1)
keep_cols = [
    "encounter_id", "race", "gender", "age", "time_in_hospital",
    "num_lab_procedures", "num_procedures", "num_medications",
    "number_outpatient", "number_emergency", "number_inpatient",
    "A1Cresult", "diabetesMed", "readmitted"
]
teaching = full[keep_cols].sample(n=5000, random_state=42).reset_index(drop=True)
teaching.to_csv(out / "diabetes_day1.csv", index=False)
print(f"Created {len(teaching):,} rows at {out / 'diabetes_day1.csv'}")
