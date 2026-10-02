"""Generate the synthetic longitudinal cohort used in the multimodal AI activity.

The output is entirely synthetic. It is not an export, sample, or statistical
reconstruction of All of Us participant records.
"""

from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "data" / "processed" / "multimodal_symptom_trajectories"
METADATA_DIR = ROOT / "metadata" / "multimodal_symptom_trajectories"
SEED = 20271002
N_PARTICIPANTS = 240
N_DAYS = 35


VARIABLES = [
    ("participant_id", "linkage", "Synthetic participant identifier.", "string", "", "identifier_leakage"),
    ("day_index", "time", "Study day, beginning with day 1.", "integer", "day", "time_trend"),
    ("age_group", "context", "Synthetic age band assigned at baseline.", "category", "", "proxy_discrimination"),
    ("chronic_condition_count", "EHR", "Synthetic count of chronic conditions recorded before follow-up.", "integer", "conditions", "confounding"),
    ("medication_count", "EHR", "Synthetic count of active medications at baseline.", "integer", "medications", "confounding"),
    ("recent_encounter", "EHR", "Whether an inpatient, outpatient, or emergency encounter occurred in the prior 7 days.", "binary", "", "care_seeking|reverse_causation"),
    ("medication_change", "EHR", "Whether a medication was started, stopped, or changed in the prior 7 days.", "binary", "", "confounding_by_indication"),
    ("care_message", "EHR", "Whether a patient-clinician portal message was recorded in the prior 7 days.", "binary", "", "care_seeking"),
    ("pain_today", "patient-reported", "Patient-reported pain today on a 0-10 teaching scale.", "continuous", "score", "same_day_measurement"),
    ("fatigue_today", "patient-reported", "Patient-reported fatigue today on a 0-10 teaching scale.", "continuous", "score", "same_day_measurement"),
    ("mood_today", "patient-reported", "Patient-reported mood today on a 0-10 scale; higher is better.", "continuous", "score", "same_day_measurement"),
    ("sleep_quality_today", "patient-reported", "Patient-reported sleep quality today on a 0-10 scale; higher is better.", "continuous", "score", "same_day_measurement"),
    ("steps", "wearable", "Synthetic daily step count.", "integer", "steps/day", "device_missingness"),
    ("active_minutes", "wearable", "Synthetic daily minutes of moderate activity.", "integer", "minutes/day", "device_missingness"),
    ("resting_heart_rate", "wearable", "Synthetic daily resting heart rate.", "continuous", "beats/minute", "device_missingness"),
    ("sleep_minutes", "wearable", "Synthetic sleep duration from the wearable.", "integer", "minutes/day", "device_missingness"),
    ("weekend", "context", "Whether the study day is Saturday or Sunday.", "binary", "", "calendar_context"),
    ("temperature_c", "context", "Synthetic daily ambient temperature linked to the participant-day.", "continuous", "degrees Celsius", "geographic_proxy"),
    ("air_quality_index", "context", "Synthetic daily air quality index linked to the participant-day.", "continuous", "AQI", "geographic_proxy"),
    ("social_support", "context", "Synthetic baseline perceived social-support score from 1-5.", "integer", "score", "proxy_discrimination"),
    ("symptom_score_today", "patient-reported", "Composite symptom severity today from 0-10; higher is worse.", "continuous", "score", "autoregressive_predictor"),
    ("symptom_score_tomorrow", "outcome", "Composite symptom severity on the next study day from 0-10; higher is worse.", "continuous", "score", "target_leakage"),
]


def clip_score(value: float) -> float:
    return float(np.clip(value, 0, 10))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build_cohort() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    records: list[dict[str, object]] = []

    for number in range(1, N_PARTICIPANTS + 1):
        participant_id = f"P{number:04d}"
        age_group = rng.choice(["18-39", "40-59", "60-79", "80+"], p=[0.18, 0.34, 0.36, 0.12])
        chronic_conditions = int(np.clip(rng.poisson(1.5), 0, 5))
        medication_count = int(np.clip(rng.poisson(2 + chronic_conditions * 1.2), 0, 14))
        social_support = int(rng.integers(1, 6))
        person_effect = rng.normal(0, 0.65)
        symptom = clip_score(2.4 + chronic_conditions * 0.55 + person_effect + rng.normal(0, 0.8))
        person_days: list[dict[str, object]] = []

        for day in range(1, N_DAYS + 1):
            weekend = int((day - 1) % 7 in {5, 6})
            seasonal_wave = np.sin((day + number % 18) / 6)
            temperature = 18 + 8 * seasonal_wave + rng.normal(0, 2.5)
            air_quality = np.clip(48 + 15 * np.cos((day + number % 11) / 5) + rng.normal(0, 12), 5, 180)

            recent_encounter = int(rng.random() < 0.035 + symptom * 0.012)
            medication_change = int(rng.random() < 0.025 + recent_encounter * 0.20)
            care_message = int(rng.random() < 0.04 + symptom * 0.008)

            sleep_minutes = int(np.clip(445 - symptom * 11 + social_support * 5 + rng.normal(0, 42), 180, 650))
            steps = int(np.clip(8200 - symptom * 520 - chronic_conditions * 260 + weekend * 550 + rng.normal(0, 1500), 250, 18000))
            active_minutes = int(np.clip(18 + steps / 420 + rng.normal(0, 8), 0, 120))
            resting_hr = float(np.clip(62 + symptom * 1.45 + chronic_conditions * 1.2 + rng.normal(0, 4), 45, 120))

            pain = clip_score(symptom + rng.normal(0, 0.9))
            fatigue = clip_score(symptom + (420 - sleep_minutes) / 75 + rng.normal(0, 0.8))
            mood = clip_score(8.2 - symptom * 0.62 + social_support * 0.18 + rng.normal(0, 0.8))
            sleep_quality = clip_score(2.2 + sleep_minutes / 75 - symptom * 0.22 + rng.normal(0, 0.7))

            person_days.append({
                "participant_id": participant_id,
                "day_index": day,
                "age_group": age_group,
                "chronic_condition_count": chronic_conditions,
                "medication_count": medication_count,
                "recent_encounter": recent_encounter,
                "medication_change": medication_change,
                "care_message": care_message,
                "pain_today": round(pain, 1),
                "fatigue_today": round(fatigue, 1),
                "mood_today": round(mood, 1),
                "sleep_quality_today": round(sleep_quality, 1),
                "steps": steps,
                "active_minutes": active_minutes,
                "resting_heart_rate": round(resting_hr, 1),
                "sleep_minutes": sleep_minutes,
                "weekend": weekend,
                "temperature_c": round(float(temperature), 1),
                "air_quality_index": round(float(air_quality), 1),
                "social_support": social_support,
                "symptom_score_today": round(symptom, 1),
            })

            next_symptom = (
                0.66 * symptom
                + 0.10 * pain
                + 0.09 * fatigue
                - 0.000045 * steps
                - 0.0012 * (sleep_minutes - 420)
                + 0.008 * max(air_quality - 50, 0)
                + 0.18 * recent_encounter
                - 0.14 * medication_change
                - 0.08 * social_support
                + 1.35
                + rng.normal(0, 0.52)
            )
            symptom = clip_score(next_symptom)

        for index in range(N_DAYS - 1):
            row = person_days[index]
            row["symptom_score_tomorrow"] = person_days[index + 1]["symptom_score_today"]
            records.append(row)

    frame = pd.DataFrame(records)

    # Modality-specific missingness is added only to predictors. The outcome is complete.
    for column in ["pain_today", "fatigue_today", "mood_today", "sleep_quality_today"]:
        frame.loc[rng.random(len(frame)) < 0.05, column] = pd.NA
    for column in ["steps", "active_minutes", "resting_heart_rate", "sleep_minutes"]:
        frame.loc[rng.random(len(frame)) < 0.08, column] = pd.NA

    return frame


def write_outputs(frame: pd.DataFrame) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "participant_day.csv"
    frame.to_csv(output_path, index=False, lineterminator="\n")

    dictionary = [
        {
            "variable": name,
            "modality": modality,
            "description": description,
            "type": variable_type,
            "units": units,
            "timing": "available by end of current day" if name != "symptom_score_tomorrow" else "next-day outcome",
            "risk_flags": risks,
            "definition_source": "NINR synthetic teaching schema",
        }
        for name, modality, description, variable_type, units, risks in VARIABLES
    ]
    pd.DataFrame(dictionary).to_csv(METADATA_DIR / "data_dictionary.csv", index=False, lineterminator="\n")
    (METADATA_DIR / "data_dictionary.json").write_text(
        json.dumps(dictionary, indent=2), encoding="utf-8"
    )

    missingness = [
        {
            "variable": column,
            "missing_count": int(frame[column].isna().sum()),
            "missing_percent": round(float(frame[column].isna().mean() * 100), 2),
            "representation": "blank/NA",
        }
        for column in frame.columns
        if frame[column].isna().any()
    ]
    pd.DataFrame(missingness).to_csv(METADATA_DIR / "missing_values.csv", index=False, lineterminator="\n")

    risk_rows = [
        {"variable": name, "risk_flags": risks, "note": description}
        for name, _, description, _, _, risks in VARIABLES
        if risks
    ]
    pd.DataFrame(risk_rows).to_csv(METADATA_DIR / "risk_flags.csv", index=False, lineterminator="\n")

    provenance = {
        "title": "Synthetic multimodal symptom trajectories teaching cohort",
        "status": "Synthetic teaching data; contains no real participant records",
        "real_world_destination": "NIH All of Us Research Program Registered Tier CDR v9",
        "real_world_destination_url": "https://www.researchallofus.org/data-tools/methods/",
        "data_dictionary_url": "https://support.researchallofus.org/hc/en-us/articles/360033200232-Data-Dictionaries",
        "access_note": "Individual-level All of Us data must be analyzed inside the secure Researcher Workbench and are not redistributed here.",
        "generation_seed": SEED,
        "participants": N_PARTICIPANTS,
        "days_generated_per_participant": N_DAYS,
        "participant_day_rows": len(frame),
        "columns": len(frame.columns),
        "outcome": "symptom_score_tomorrow",
        "participant_file_sha256": sha256(output_path),
        "software": {"python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__},
        "transformations": [
            "Generated independent participant-level baseline attributes from fixed probability distributions.",
            "Generated 35-day autocorrelated symptom, wearable, EHR-like, and contextual time series.",
            "Created the next-day symptom outcome by shifting symptom_score_today within participant.",
            "Retained days 1-34, yielding 8,160 participant-day observations.",
            "Introduced 5% patient-reported and 8% wearable predictor missingness with a fixed random seed.",
        ],
    }
    (METADATA_DIR / "provenance.json").write_text(json.dumps(provenance, indent=2), encoding="utf-8")


def validate(frame: pd.DataFrame) -> None:
    expected_columns = [item[0] for item in VARIABLES]
    checks = {
        "expected shape": frame.shape == (N_PARTICIPANTS * (N_DAYS - 1), len(expected_columns)),
        "expected columns": frame.columns.tolist() == expected_columns,
        "participant-day unique": not frame.duplicated(["participant_id", "day_index"]).any(),
        "outcome complete": frame["symptom_score_tomorrow"].notna().all(),
        "outcome range": frame["symptom_score_tomorrow"].between(0, 10).all(),
        "all four modalities present": {"patient-reported", "wearable", "EHR", "context"}.issubset({item[1] for item in VARIABLES}),
    }
    checks = {name: bool(value) for name, value in checks.items()}
    report = {"passed": all(checks.values()), "checks": checks}
    (METADATA_DIR / "validation_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    if not report["passed"]:
        raise AssertionError(report)


def main() -> None:
    frame = build_cohort()
    write_outputs(frame)
    validate(frame)
    print(f"Wrote {len(frame):,} synthetic participant-days; validation passed")


if __name__ == "__main__":
    main()
