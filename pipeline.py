"""Acquire, prepare, document, and validate the NINR public-health dataset.

The raw UCI archive and its extracted files are checksum-pinned. Derived files are
rebuildable with ``python pipeline.py all``.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import shutil
import tempfile
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config" / "datasets.json"
RAW_ROOT = ROOT / "data" / "raw" / "uci_diabetes_296"
ARCHIVE_PATH = RAW_ROOT / "uci_diabetes_296.zip"
ORIGINAL_DIR = RAW_ROOT / "original"
DOCUMENTATION_DIR = RAW_ROOT / "documentation"
PROCESSED_DIR = ROOT / "data" / "processed"
METADATA_DIR = ROOT / "metadata"
GENERATED_DOCS_DIR = ROOT / "docs" / "generated"


def load_config() -> dict[str, Any]:
    payload = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    datasets = payload.get("datasets", [])
    if len(datasets) != 1:
        raise ValueError("This release expects exactly one configured dataset")
    return datasets[0]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def download(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "NINR-dataset-pipeline/1.0"})
    with urllib.request.urlopen(request, timeout=120) as response, tempfile.NamedTemporaryFile(
        delete=False, dir=destination.parent
    ) as temporary:
        shutil.copyfileobj(response, temporary)
        temporary_path = Path(temporary.name)
    temporary_path.replace(destination)


def assert_hash(path: Path, expected: str) -> None:
    actual = sha256(path)
    if actual.lower() != expected.lower():
        raise ValueError(f"Checksum mismatch for {path}: expected {expected}, got {actual}")


def acquire(force: bool = False) -> None:
    config = load_config()
    RAW_ROOT.mkdir(parents=True, exist_ok=True)
    DOCUMENTATION_DIR.mkdir(parents=True, exist_ok=True)

    if force or not ARCHIVE_PATH.exists():
        download(config["archive_url"], ARCHIVE_PATH)
    assert_hash(ARCHIVE_PATH, config["archive_sha256"])

    for filename, expected_hash in config["original_files"].items():
        output = ORIGINAL_DIR / filename
        if force or not output.exists():
            ORIGINAL_DIR.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(ARCHIVE_PATH) as archive:
                member_names = set(archive.namelist())
                if filename not in member_names:
                    raise ValueError(f"Official archive is missing {filename}")
                with archive.open(filename) as source, output.open("wb") as target:
                    shutil.copyfileobj(source, target)
        assert_hash(output, expected_hash)

    docs = {
        "uci_dataset_296_metadata.json": config["metadata_url"],
        "strack_2014_pmc_fulltext.xml": config["article_fulltext_url"],
    }
    for filename, url in docs.items():
        destination = DOCUMENTATION_DIR / filename
        if force or not destination.exists():
            download(url, destination)


def parse_id_mappings(path: Path) -> dict[str, dict[int, str]]:
    mappings: dict[str, dict[int, str]] = {}
    current: str | None = None
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.reader(handle):
            if not row or not any(cell.strip() for cell in row):
                current = None
                continue
            if row[0].strip() in {
                "admission_type_id",
                "discharge_disposition_id",
                "admission_source_id",
            }:
                current = row[0].strip()
                mappings[current] = {}
                continue
            if current and row[0].strip():
                mappings[current][int(row[0])] = row[1].strip()
    return mappings


def stable_rank(encounter_id: Any, seed: str) -> str:
    return hashlib.sha256(f"{seed}:{encounter_id}".encode("utf-8")).hexdigest()


def categorical_labels() -> dict[str, dict[str, str]]:
    """Labels transcribed from the official UCI metadata descriptions."""
    medication = {
        "No": "drug was not prescribed",
        "Steady": "drug was prescribed and dosage did not change",
        "Up": "dosage was increased during the encounter",
        "Down": "dosage was decreased during the encounter",
    }
    labels = {
        "race": {
            "Caucasian": "Caucasian", "Asian": "Asian",
            "AfricanAmerican": "African American", "Hispanic": "Hispanic", "Other": "other",
        },
        "gender": {"Male": "male", "Female": "female", "Unknown/Invalid": "unknown/invalid"},
        "age": {f"[{start}-{start + 10})": f"age {start} to less than {start + 10} years" for start in range(0, 100, 10)},
        "max_glu_serum": {
            "None": "test was not taken", "Norm": "normal",
            ">200": "greater than 200", ">300": "greater than 300",
        },
        "A1Cresult": {
            "None": "test was not taken", "Norm": "less than 7%",
            ">7": "greater than 7% and less than 8%", ">8": "greater than 8%",
        },
        "change": {"Ch": "change in diabetes medication", "No": "no change in diabetes medication"},
        "diabetesMed": {"Yes": "diabetes medication prescribed", "No": "no diabetes medication prescribed"},
        "readmitted": {
            "<30": "inpatient readmission in less than 30 days",
            ">30": "inpatient readmission after 30 days",
            "NO": "no recorded readmission",
        },
    }
    for name in [
        "metformin", "repaglinide", "nateglinide", "chlorpropamide",
        "glimepiride", "acetohexamide", "glipizide", "glyburide",
        "tolbutamide", "pioglitazone", "rosiglitazone", "acarbose",
        "miglitol", "troglitazone", "tolazamide", "examide",
        "citoglipton", "insulin", "glyburide-metformin",
        "glipizide-metformin", "glimepiride-pioglitazone",
        "metformin-rosiglitazone", "metformin-pioglitazone",
    ]:
        labels[name] = medication
    return labels


def risk_annotations() -> dict[str, dict[str, str]]:
    return {
        "encounter_id": {
            "risk": "leakage",
            "note": "Identifier; exclude from model predictors.",
        },
        "patient_nbr": {
            "risk": "leakage",
            "note": "Patient identifier; repeated patients can cross validation folds. Excluded from participant file.",
        },
        "race": {
            "risk": "proxy_discrimination|confounding",
            "note": "Sensitive demographic attribute. Audit subgroup performance and avoid causal interpretation without design justification.",
        },
        "gender": {
            "risk": "proxy_discrimination|confounding",
            "note": "Sensitive demographic attribute with an Unknown/Invalid category in the source.",
        },
        "age": {
            "risk": "proxy_discrimination|confounding",
            "note": "Demographic attribute and strong clinical risk factor; may also proxy protected status.",
        },
        "discharge_disposition_id": {
            "risk": "post_outcome_measurement|leakage",
            "note": "Known at discharge, not at admission; includes death/hospice destinations. Prediction-time availability must be explicit.",
        },
        "time_in_hospital": {
            "risk": "post_outcome_measurement",
            "note": "Complete length of stay is known only at discharge.",
        },
        "num_lab_procedures": {
            "risk": "post_outcome_measurement|confounding",
            "note": "Accumulates during the encounter and may reflect illness severity and care intensity.",
        },
        "num_procedures": {
            "risk": "post_outcome_measurement|confounding",
            "note": "Accumulates during the encounter and may reflect illness severity and care intensity.",
        },
        "num_medications": {
            "risk": "post_outcome_measurement|confounding",
            "note": "Encounter-level treatment intensity may reflect severity and care decisions.",
        },
        "A1Cresult": {
            "risk": "post_outcome_measurement|confounding",
            "note": "Measured during the encounter; testing is a care-process decision and None means not measured.",
        },
        "max_glu_serum": {
            "risk": "post_outcome_measurement|confounding",
            "note": "Measured during the encounter; None means the test was not taken.",
        },
        "insulin": {
            "risk": "post_outcome_measurement|confounding",
            "note": "Treatment status/change during the encounter is affected by clinical severity and clinician decisions.",
        },
        "change": {
            "risk": "post_outcome_measurement|confounding",
            "note": "Diabetes medication change occurs during the encounter and is not an admission-time predictor.",
        },
        "diabetesMed": {
            "risk": "post_outcome_measurement|confounding",
            "note": "Prescription during the encounter may be affected by severity and clinician decisions.",
        },
        "readmitted": {
            "risk": "outcome|leakage",
            "note": "Official target; never include as a predictor of readmitted_30d.",
        },
        "readmitted_30d": {
            "risk": "outcome|leakage",
            "note": "Derived binary outcome; never include as a predictor.",
        },
    }


def build_dictionary(
    metadata: dict[str, Any],
    raw: pd.DataFrame,
    participant_columns: list[str],
    mappings: dict[str, dict[int, str]],
) -> pd.DataFrame:
    official = {item["name"]: item for item in metadata["data"]["variables"]}
    labels = categorical_labels()
    risks = risk_annotations()
    records: list[dict[str, Any]] = []
    for column in raw.columns:
        source = official[column]
        observed_missing = int((raw[column].astype("string") == "?").sum())
        record = {
            "variable": column,
            "source_variable": column,
            "derived": False,
            "selected_for_participant": column in participant_columns,
            "role": source.get("role"),
            "type": source.get("type", "").strip(),
            "demographic": source.get("demographic"),
            "description": source.get("description"),
            "units": source.get("units"),
            "official_missing_values": source.get("missing_values"),
            "raw_missing_code": "?" if observed_missing else "",
            "participant_missing_representation": "blank/NA" if observed_missing else "",
            "categorical_value_labels": json.dumps(labels.get(column, []), ensure_ascii=False),
            "weighting_variable": False,
            "risk_flags": risks.get(column, {}).get("risk", ""),
            "risk_note": risks.get(column, {}).get("note", ""),
            "definition_source": "UCI API metadata for dataset 296",
        }
        if column in mappings:
            record["categorical_value_labels"] = json.dumps(mappings[column], ensure_ascii=False)
            record["definition_source"] = "UCI IDS_mapping.csv"
        records.append(record)

    derived = [
        ("admission_type", "admission_type_id", "Official admission type label from IDS_mapping.csv"),
        ("discharge_disposition", "discharge_disposition_id", "Official discharge disposition label from IDS_mapping.csv"),
        ("admission_source", "admission_source_id", "Official admission source label from IDS_mapping.csv"),
        ("readmitted_30d", "readmitted", "1 when official readmitted value is <30; otherwise 0"),
    ]
    for variable, source_variable, description in derived:
        records.append({
            "variable": variable,
            "source_variable": source_variable,
            "derived": True,
            "selected_for_participant": variable in participant_columns,
            "role": "Derived label" if variable != "readmitted_30d" else "Derived outcome",
            "type": "Categorical" if variable != "readmitted_30d" else "Integer",
            "demographic": "",
            "description": description,
            "units": "",
            "official_missing_values": "no",
            "raw_missing_code": "",
            "participant_missing_representation": "",
            "categorical_value_labels": json.dumps([0, 1]) if variable == "readmitted_30d" else "",
            "weighting_variable": False,
            "risk_flags": risks.get(variable, {}).get("risk", ""),
            "risk_note": risks.get(variable, {}).get("note", ""),
            "definition_source": "Deterministic transformation of official source field",
        })
    return pd.DataFrame.from_records(records)


def prepare() -> None:
    config = load_config()
    source_path = ORIGINAL_DIR / "diabetic_data.csv"
    metadata_path = DOCUMENTATION_DIR / "uci_dataset_296_metadata.json"
    mapping_path = ORIGINAL_DIR / "IDS_mapping.csv"
    for required in [source_path, metadata_path, mapping_path]:
        if not required.exists():
            raise FileNotFoundError(f"Missing {required}; run `python pipeline.py acquire`")

    raw = pd.read_csv(source_path, dtype={"diag_1": "string", "diag_2": "string", "diag_3": "string"})
    metadata = json.loads(metadata_path.read_text(encoding="utf-8-sig"))
    mappings = parse_id_mappings(mapping_path)

    working = raw.copy()
    working = working.replace("?", pd.NA)
    for source_name, output_name in [
        ("admission_type_id", "admission_type"),
        ("discharge_disposition_id", "discharge_disposition"),
        ("admission_source_id", "admission_source"),
    ]:
        working[output_name] = working[source_name].map(mappings[source_name]).astype("string")
    working["readmitted_30d"] = (working["readmitted"] == "<30").astype("int8")
    working["_sample_rank"] = working["encounter_id"].map(
        lambda value: stable_rank(value, config["sample_seed"])
    )
    participant = (
        working.sort_values("_sample_rank", kind="stable")
        .head(config["sample_size"])[config["participant_columns"]]
        .sort_values("encounter_id")
        .reset_index(drop=True)
    )

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    GENERATED_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    participant_path = PROCESSED_DIR / "diabetes_130_hospitals_participant.csv"
    participant.to_csv(participant_path, index=False, lineterminator="\n")

    dictionary = build_dictionary(metadata, raw, config["participant_columns"], mappings)
    dictionary.to_csv(METADATA_DIR / "data_dictionary.csv", index=False, lineterminator="\n")
    (METADATA_DIR / "data_dictionary.json").write_text(
        json.dumps(dictionary.to_dict(orient="records"), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    value_label_rows = []
    for variable, values in categorical_labels().items():
        for value, label in values.items():
            value_label_rows.append({
                "variable": variable,
                "code": value,
                "label": label,
                "source": "UCI API metadata for dataset 296",
            })
    for variable, mapping in mappings.items():
        for code, label in mapping.items():
            value_label_rows.append({
                "variable": variable,
                "code": code,
                "label": label,
                "source": "UCI IDS_mapping.csv",
            })
    pd.DataFrame(value_label_rows).to_csv(
        METADATA_DIR / "value_labels.csv", index=False, lineterminator="\n"
    )

    risk_rows = [
        {"variable": variable, **annotation}
        for variable, annotation in risk_annotations().items()
    ]
    pd.DataFrame(risk_rows).to_csv(
        METADATA_DIR / "risk_flags.csv", index=False, lineterminator="\n"
    )

    missing_rows = []
    for column in raw.columns:
        count = int((raw[column].astype("string") == "?").sum())
        if count:
            missing_rows.append({
                "variable": column,
                "raw_code": "?",
                "raw_count": count,
                "participant_representation": "blank/NA",
                "source": "UCI metadata marks variable as missing; count verified in original file",
            })
    missing_rows.extend([
        {
            "variable": "max_glu_serum",
            "raw_code": "None",
            "raw_count": int((raw["max_glu_serum"] == "None").sum()),
            "participant_representation": "None (retained category)",
            "source": "UCI description: test was not taken",
        },
        {
            "variable": "A1Cresult",
            "raw_code": "None",
            "raw_count": int((raw["A1Cresult"] == "None").sum()),
            "participant_representation": "None (retained category)",
            "source": "UCI description: test was not taken",
        },
    ])
    for variable, mapping in mappings.items():
        for code, label in mapping.items():
            normalized = label.lower()
            if any(token in normalized for token in ["null", "not available", "not mapped", "unknown/invalid"]):
                missing_rows.append({
                    "variable": variable,
                    "raw_code": code,
                    "raw_count": int((raw[variable] == code).sum()),
                    "participant_representation": f"{label} (retained source-defined category)",
                    "source": "UCI IDS_mapping.csv",
                })
    pd.DataFrame(missing_rows).to_csv(
        METADATA_DIR / "missing_values.csv", index=False, lineterminator="\n"
    )

    provenance = {
        "dataset": config,
        "observed_at_build": datetime.now(timezone.utc).isoformat(),
        "raw_files": {
            str(ARCHIVE_PATH.relative_to(ROOT)): {"sha256": sha256(ARCHIVE_PATH), "bytes": ARCHIVE_PATH.stat().st_size},
            str(source_path.relative_to(ROOT)): {"sha256": sha256(source_path), "bytes": source_path.stat().st_size},
            str(mapping_path.relative_to(ROOT)): {"sha256": sha256(mapping_path), "bytes": mapping_path.stat().st_size},
            str(metadata_path.relative_to(ROOT)): {"sha256": sha256(metadata_path), "bytes": metadata_path.stat().st_size},
            str((DOCUMENTATION_DIR / "strack_2014_pmc_fulltext.xml").relative_to(ROOT)): {
                "sha256": sha256(DOCUMENTATION_DIR / "strack_2014_pmc_fulltext.xml"),
                "bytes": (DOCUMENTATION_DIR / "strack_2014_pmc_fulltext.xml").stat().st_size,
            },
        },
        "transformations": [
            "Verified the official ZIP and both bundled files against pinned SHA-256 checksums.",
            "Loaded diabetic_data.csv without modifying the original file.",
            "Replaced the raw '?' missing-value code with blank/NA only in the participant derivative.",
            "Decoded three integer ID fields with the bundled official IDS_mapping.csv.",
            "Derived readmitted_30d as 1 for readmitted='<30' and 0 for '>30' or 'NO'.",
            "Selected 5,000 encounters using the lowest SHA-256 ranks of sample_seed:encounter_id.",
            "Sorted the participant derivative by encounter_id and wrote UTF-8 CSV with LF line endings.",
        ],
        "weighting": {
            "weighting_variables": [],
            "note": "The official UCI metadata and source files provide no survey or analytic weighting variable.",
        },
        "output": {
            "path": str(participant_path.relative_to(ROOT)),
            "sha256": sha256(participant_path),
            "rows": len(participant),
            "columns": len(participant.columns),
        },
        "software": {
            "python": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "pandas": pd.__version__,
        },
    }
    (METADATA_DIR / "provenance.json").write_text(
        json.dumps(provenance, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    outcome_counts = participant["readmitted"].value_counts(dropna=False).to_dict()
    summary = {
        "participant_rows": len(participant),
        "participant_columns": len(participant.columns),
        "outcome_definition": {
            "official_readmitted": "<30 = inpatient readmission in less than 30 days; >30 = inpatient readmission after 30 days; NO = no recorded readmission.",
            "derived_readmitted_30d": "1 when readmitted is <30; otherwise 0.",
            "source": "UCI dataset 296 metadata",
        },
        "outcome_counts": outcome_counts,
        "early_readmission_rate": float(participant["readmitted_30d"].mean()),
        "weighting_variables": [],
    }
    (METADATA_DIR / "dataset_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )


def validate() -> dict[str, Any]:
    config = load_config()
    checks: list[dict[str, Any]] = []

    def check(name: str, condition: bool, detail: str) -> None:
        checks.append({"name": name, "passed": bool(condition), "detail": detail})

    assert_hash(ARCHIVE_PATH, config["archive_sha256"])
    for filename, expected in config["original_files"].items():
        assert_hash(ORIGINAL_DIR / filename, expected)
    raw = pd.read_csv(ORIGINAL_DIR / "diabetic_data.csv", low_memory=False)
    # keep_default_na=False preserves the official IDS_mapping.csv label "NULL".
    participant = pd.read_csv(
        PROCESSED_DIR / "diabetes_130_hospitals_participant.csv", keep_default_na=False
    )

    check("raw row count", len(raw) == config["expected_rows"], f"observed {len(raw)}")
    check("raw column count", len(raw.columns) == config["expected_columns"], f"observed {len(raw.columns)}")
    official_metadata = json.loads(
        (DOCUMENTATION_DIR / "uci_dataset_296_metadata.json").read_text(encoding="utf-8-sig")
    )
    official_headers = [item["name"] for item in official_metadata["data"]["variables"]]
    check("raw headers match official metadata", raw.columns.tolist() == official_headers, "ordered headers agree with UCI API record")
    check("raw encounter ID unique", raw["encounter_id"].is_unique, "encounter_id must identify encounters")
    check("official target values", set(raw["readmitted"]) == {"<30", ">30", "NO"}, str(sorted(raw["readmitted"].unique())))
    check("time in hospital range", raw["time_in_hospital"].between(1, 14).all(), "official inclusion range is 1-14 days")
    check("participant row count", len(participant) == config["sample_size"], f"observed {len(participant)}")
    check("participant columns", participant.columns.tolist() == config["participant_columns"], "ordered columns match manifest")
    check("participant variable count", 10 <= len(participant.columns) <= 30, f"observed {len(participant.columns)}")
    check("participant encounter ID unique", participant["encounter_id"].is_unique, "no duplicate encounter IDs")
    ranked_ids = (
        raw.assign(
            _sample_rank=raw["encounter_id"].map(
                lambda value: stable_rank(value, config["sample_seed"])
            )
        )
        .sort_values("_sample_rank", kind="stable")
        .head(config["sample_size"])["encounter_id"]
    )
    check(
        "deterministic sample membership",
        set(participant["encounter_id"]) == set(ranked_ids),
        "participant IDs are the lowest configured SHA-256 ranks",
    )
    check("no raw missing code", not participant.astype("string").eq("?").any().any(), "participant CSV uses blank/NA")
    expected_binary = (participant["readmitted"] == "<30").astype(int)
    check("binary outcome derivation", participant["readmitted_30d"].equals(expected_binary), "1 iff readmitted is <30")
    check("all outcome classes retained", set(participant["readmitted"]) == {"<30", ">30", "NO"}, str(participant["readmitted"].value_counts().to_dict()))
    check("decoded admission type complete", participant["admission_type"].notna().all(), "all IDs mapped")
    check("decoded discharge complete", participant["discharge_disposition"].notna().all(), "all IDs mapped")
    check("decoded admission source complete", participant["admission_source"].notna().all(), "all IDs mapped")
    check("dictionary covers participant", set(participant.columns).issubset(set(pd.read_csv(METADATA_DIR / "data_dictionary.csv")["variable"])), "all participant variables documented")
    provenance = json.loads((METADATA_DIR / "provenance.json").read_text(encoding="utf-8"))
    check(
        "participant checksum matches provenance",
        sha256(PROCESSED_DIR / "diabetes_130_hospitals_participant.csv")
        == provenance["output"]["sha256"],
        "derived artifact hash agrees with provenance.json",
    )

    report = {
        "validated_at": datetime.now(timezone.utc).isoformat(),
        "passed": all(item["passed"] for item in checks),
        "checks": checks,
    }
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    (METADATA_DIR / "validation_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    if not report["passed"]:
        failures = [item["name"] for item in checks if not item["passed"]]
        raise AssertionError(f"Validation failed: {', '.join(failures)}")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["acquire", "prepare", "validate", "all"])
    parser.add_argument("--force", action="store_true", help="redownload and re-extract official source files")
    args = parser.parse_args()
    if args.command in {"acquire", "all"}:
        acquire(force=args.force)
    if args.command in {"prepare", "all"}:
        prepare()
    if args.command in {"validate", "all"}:
        report = validate()
        print(f"Validation passed: {len(report['checks'])} checks")


if __name__ == "__main__":
    main()
