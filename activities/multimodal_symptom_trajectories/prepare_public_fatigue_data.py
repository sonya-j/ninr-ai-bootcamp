"""Download and prepare the open wearable-fatigue teaching dataset.

Official source: https://doi.org/10.5281/zenodo.4266157 (version 1, CC BY 4.0)

The original files are downloaded unchanged, checked against the MD5 values in
the Zenodo record, and kept under data/raw/ (gitignored). A daily analytic file
and machine-readable documentation are written to the tracked activity folders.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import urllib.request
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
RECORD_ID = "4266157"
VERSION = "v1"
SOURCE_PAGE = f"https://zenodo.org/records/{RECORD_ID}"
API_URL = f"https://zenodo.org/api/records/{RECORD_ID}"
RAW_DIR = ROOT / "data" / "raw" / "multimodal_symptom_trajectories" / f"zenodo_{RECORD_ID}"
OUTPUT_DIR = ROOT / "data" / "processed" / "multimodal_symptom_trajectories"
METADATA_DIR = ROOT / "metadata" / "multimodal_symptom_trajectories"

FATIGUE_QUESTION = (
    "Describe fatigue on a scale of 1 to 10, where 1 means you don’t feel tired "
    "at all and 10 means the worst tiredness you can imagine"
)

SENSOR_COLUMNS = [
    "ActivityCounts",
    "EnergyExpenditure",
    "HR",
    "HRV",
    "RESP",
    "Steps",
    "SkinTemperature",
]


def file_digest(path: Path, algorithm: str = "sha256") -> str:
    digest = hashlib.new(algorithm)
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fetch_json(url: str) -> dict:
    with urllib.request.urlopen(url) as response:  # noqa: S310 - fixed official URL
        return json.load(response)


def download_originals(raw_dir: Path) -> dict:
    raw_dir.mkdir(parents=True, exist_ok=True)
    record = fetch_json(API_URL)
    for item in record["files"]:
        destination = raw_dir / item["key"]
        expected = item["checksum"].split(":", 1)[1]
        if destination.exists() and file_digest(destination, "md5") == expected:
            continue
        urllib.request.urlretrieve(item["links"]["self"], destination)  # noqa: S310
        actual = file_digest(destination, "md5")
        if actual != expected:
            raise ValueError(f"Checksum mismatch for {destination.name}")
    return record


def load_record_for_existing_source(source_dir: Path) -> dict:
    """Use live metadata when possible and a minimal local record otherwise."""
    try:
        return fetch_json(API_URL)
    except Exception:
        return {
            "metadata": {"license": {"id": "cc-by-4.0"}},
            "files": [
                {
                    "key": path.name,
                    "size": path.stat().st_size,
                    "checksum": f"md5:{file_digest(path, 'md5')}",
                }
                for path in sorted(source_dir.glob("*.csv"))
            ],
        }


def normalize_question(text: object) -> str:
    return str(text).replace("�", "’").strip()


def prepare_pro(source_dir: Path) -> pd.DataFrame:
    pro = pd.read_csv(source_dir / "fatiguePROs.csv")
    pro["date"] = pd.to_datetime(pro["DateTime"], format="%d.%m.%y %H:%M").dt.normalize()
    pro["PROquestion"] = pro["PROquestion"].map(normalize_question)

    fatigue_rows = pro[pro["PROquestion"] == FATIGUE_QUESTION].copy()
    fatigue = fatigue_rows[["SubjectID", "date", "PROanswer_value"]].rename(
        columns={"SubjectID": "participant_id", "PROanswer_value": "fatigue_today"}
    )
    fatigue["fatigue_today"] = pd.to_numeric(fatigue["fatigue_today"], errors="coerce")

    choice_map = {
        "Are you feeling better, worse or the same as yesterday?": "change_vs_yesterday",
        "Physically, today how often did you feel exhausted?": "physical_exhaustion",
        "Mentally, today how often did you feel exhausted?": "mental_exhaustion",
        "Did you do sport today?": "sport_today",
    }
    choices = pro[pro["PROquestion"].isin(choice_map)].copy()
    choices["variable"] = choices["PROquestion"].map(choice_map)
    choices = choices.pivot_table(
        index=["SubjectID", "date"],
        columns="variable",
        values="PROanswer_choice",
        aggfunc="first",
    ).reset_index().rename(columns={"SubjectID": "participant_id"})

    daily = fatigue.merge(choices, on=["participant_id", "date"], how="left")
    return daily.drop_duplicates(["participant_id", "date"])


def prepare_sensors(source_dir: Path) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for path in sorted(source_dir.glob("subjectID_*.csv")):
        participant_id = int(path.stem.split("_")[-1])
        sensor = pd.read_csv(path, usecols=lambda col: col == "Timestamp" or col in SENSOR_COLUMNS)
        sensor["date"] = pd.to_datetime(
            sensor["Timestamp"], format="%d.%m.%y %H:%M", errors="coerce"
        ).dt.normalize()
        for column in SENSOR_COLUMNS:
            if column not in sensor:
                sensor[column] = np.nan
            sensor[column] = pd.to_numeric(sensor[column], errors="coerce")

        grouped = sensor.groupby("date", dropna=True)
        daily = grouped[SENSOR_COLUMNS].agg(["mean", "std"])
        daily.columns = [f"{name.lower()}_{stat}" for name, stat in daily.columns]
        daily["wear_minutes"] = grouped.size()
        daily["participant_id"] = participant_id
        frames.append(daily.reset_index())
    return pd.concat(frames, ignore_index=True)


def build_daily_dataset(source_dir: Path) -> pd.DataFrame:
    pro = prepare_pro(source_dir)
    sensors = prepare_sensors(source_dir)
    daily = pro.merge(sensors, on=["participant_id", "date"], how="inner")
    daily = daily.sort_values(["participant_id", "date"]).reset_index(drop=True)
    daily["day_of_week"] = daily["date"].dt.day_name()
    daily["weekend"] = daily["date"].dt.dayofweek.ge(5).astype(int)
    daily["study_day"] = daily.groupby("participant_id")["date"].transform(
        lambda values: (values - values.min()).dt.days + 1
    )
    daily["next_date"] = daily.groupby("participant_id")["date"].shift(-1)
    daily["fatigue_tomorrow"] = daily.groupby("participant_id")["fatigue_today"].shift(-1)
    daily["days_to_next_report"] = (daily["next_date"] - daily["date"]).dt.days
    daily.loc[daily["days_to_next_report"] != 1, "fatigue_tomorrow"] = np.nan
    daily = daily.drop(columns=["next_date", "days_to_next_report"])
    daily["date"] = daily["date"].dt.strftime("%Y-%m-%d")
    ordered = [
        "participant_id", "date", "study_day", "day_of_week", "weekend",
        "fatigue_today", "change_vs_yesterday", "physical_exhaustion",
        "mental_exhaustion", "sport_today", "wear_minutes",
    ] + [
        f"{column.lower()}_{stat}"
        for column in SENSOR_COLUMNS
        for stat in ("mean", "std")
    ] + ["fatigue_tomorrow"]
    return daily[ordered]


def dictionary_rows() -> list[dict[str, str]]:
    rows = [
        ("participant_id", "linkage", "integer", "De-identified subject identifier from the source files.", "", "identifier"),
        ("date", "time context", "date", "Calendar date derived from the source timestamp (YYYY-MM-DD).", "", "potential identity/time proxy"),
        ("study_day", "time context", "integer", "Days since that participant's first matched date, beginning at 1.", "", "trajectory index"),
        ("day_of_week", "time context", "categorical", "Day name derived from date.", "Monday–Sunday", "context"),
        ("weekend", "time context", "binary", "Whether date is Saturday or Sunday.", "0=no; 1=yes", "context"),
        ("fatigue_today", "patient-reported", "numeric", "Daily response to the 1–10 overall fatigue question.", "1=not tired at all; 10=worst tiredness imaginable", "strong autoregressive predictor"),
        ("change_vs_yesterday", "patient-reported", "categorical", "Response to whether the participant feels better, worse, or the same as yesterday.", "Better; Same; Worse", "may overlap conceptually with outcome"),
        ("physical_exhaustion", "patient-reported", "ordinal", "Daily reported frequency of physical exhaustion.", "Never; Sometimes; Regularly; Often; Always", "predictor"),
        ("mental_exhaustion", "patient-reported", "ordinal", "Daily reported frequency of mental exhaustion.", "Never; Sometimes; Regularly; Often; Always", "predictor"),
        ("sport_today", "patient-reported", "binary categorical", "Whether the participant reported doing sport that day.", "No; Yes", "behavior/context"),
        ("wear_minutes", "wearable", "integer", "Number of one-minute sensor rows available for that participant-date.", "", "missingness/device-use proxy"),
    ]
    official = {
        "activitycounts": "Activity counts",
        "energyexpenditure": "Energy expenditure",
        "hr": "Heart rate",
        "hrv": "Heart-rate variability",
        "resp": "Respiratory rate",
        "steps": "Steps",
        "skintemperature": "Skin temperature",
    }
    for name, label in official.items():
        for stat in ("mean", "std"):
            rows.append((
                f"{name}_{stat}", "wearable", "numeric",
                f"Daily {stat} of the source {label} sensor field.", "Source device units; see the official study article.",
                "predictor; missingness may reflect non-wear",
            ))
    rows.append((
        "fatigue_tomorrow", "outcome", "numeric",
        "The next calendar day's fatigue_today response within the same participant.",
        "1=not tired at all; 10=worst tiredness imaginable",
        "outcome; never include as a predictor",
    ))
    return [
        {"variable": name, "modality": modality, "data_type": dtype, "definition": definition,
         "value_labels_or_units": labels, "risk_flag": risk}
        for name, modality, dtype, definition, labels, risk in rows
    ]


def write_artifacts(daily: pd.DataFrame, record: dict, source_dir: Path) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "participant_day.csv"
    daily.to_csv(output_path, index=False)

    dictionary = pd.DataFrame(dictionary_rows())
    dictionary.to_csv(METADATA_DIR / "data_dictionary.csv", index=False)
    (METADATA_DIR / "data_dictionary.json").write_text(
        json.dumps(dictionary.to_dict(orient="records"), indent=2), encoding="utf-8"
    )
    missing = pd.DataFrame({
        "variable": daily.columns,
        "missing_n": daily.isna().sum().values,
        "missing_percent": (daily.isna().mean().values * 100).round(2),
        "missing_value_code": "blank/NA",
    })
    missing.to_csv(METADATA_DIR / "missing_values.csv", index=False)

    risk_flags = dictionary.loc[dictionary["risk_flag"] != "", ["variable", "risk_flag"]]
    risk_flags.to_csv(METADATA_DIR / "risk_flags.csv", index=False)

    predictors = [column for column in daily.columns if column != "fatigue_tomorrow"]
    checks = {
        "official source files present": (source_dir / "fatiguePROs.csv").exists(),
        "participant-day unique": not daily.duplicated(["participant_id", "date"]).any(),
        "all outcomes in official 1-10 range": daily["fatigue_tomorrow"].dropna().between(1, 10).all(),
        "patient-reported modality present": any(dictionary.set_index("variable").loc[p, "modality"] == "patient-reported" for p in predictors),
        "wearable modality present": any(dictionary.set_index("variable").loc[p, "modality"] == "wearable" for p in predictors),
        "time context present": any(dictionary.set_index("variable").loc[p, "modality"] == "time context" for p in predictors),
        "EHR modality correctly marked absent": "EHR" not in set(dictionary["modality"]),
    }
    validation = {
        "passed": bool(all(checks.values())),
        "checks": {name: bool(value) for name, value in checks.items()},
        "rows": int(len(daily)),
        "participants": int(daily["participant_id"].nunique()),
        "rows_with_next_day_outcome": int(daily["fatigue_tomorrow"].notna().sum()),
    }
    (METADATA_DIR / "validation_report.json").write_text(
        json.dumps(validation, indent=2), encoding="utf-8"
    )
    if not validation["passed"]:
        raise ValueError(f"Validation failed: {validation}")

    file_manifest = [
        {"name": item["key"], "size": item["size"], "md5": item["checksum"].split(":", 1)[-1]}
        for item in record.get("files", [])
    ]
    provenance = {
        "dataset_title": "Continuous multi-sensor wearable data and daily subject-reported fatigue of healthy adults",
        "official_source": SOURCE_PAGE,
        "doi": "10.5281/zenodo.4266157",
        "dataset_version": VERSION,
        "publication_date": "2020-11-10",
        "access_date": date.today().isoformat(),
        "access_right": "open",
        "license": record.get("metadata", {}).get("license", {}).get("id", "cc-by-4.0"),
        "original_files_preserved_under": RAW_DIR.relative_to(ROOT).as_posix(),
        "original_files_tracked_in_git": False,
        "original_file_manifest": file_manifest,
        "transformations": [
            "Parsed original participant and timestamp fields without changing source files.",
            "Pivoted five official daily PRO questions to one participant-day row.",
            "Aggregated selected 1-minute wearable fields to daily mean and standard deviation.",
            "Counted available one-minute rows as wear_minutes.",
            "Derived study_day, day_of_week, and weekend from source timestamps.",
            "Defined fatigue_tomorrow only when the next within-person report occurred exactly one calendar day later.",
        ],
        "important_scope_note": "The public source has patient-reported, wearable, and time-context data; it does not contain EHR data.",
        "processed_sha256": file_digest(output_path),
        "software": {"python": platform.python_version(), "pandas": pd.__version__, "numpy": np.__version__},
    }
    (METADATA_DIR / "provenance.json").write_text(
        json.dumps(provenance, indent=2), encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source-dir",
        type=Path,
        help="Optional directory already containing the unchanged Zenodo CSV files.",
    )
    args = parser.parse_args()
    if args.source_dir:
        source_dir = args.source_dir.resolve()
        record = load_record_for_existing_source(source_dir)
    else:
        source_dir = RAW_DIR
        record = download_originals(source_dir)
    daily = build_daily_dataset(source_dir)
    write_artifacts(daily, record, source_dir)
    validation = json.loads((METADATA_DIR / "validation_report.json").read_text())
    print(
        f"Wrote {validation['rows']:,} participant-days from {validation['participants']} participants; "
        f"{validation['rows_with_next_day_outcome']:,} rows have a next-day outcome."
    )


if __name__ == "__main__":
    main()
