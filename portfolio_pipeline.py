"""Build the 20-dataset NINR teaching portfolio from official UCI sources."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import shutil
import tempfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config" / "portfolio.json"
LOCK_PATH = ROOT / "config" / "portfolio_sources.lock.json"
RAW_ROOT = ROOT / "data" / "raw" / "portfolio"
PROCESSED_ROOT = ROOT / "data" / "processed" / "portfolio"
METADATA_ROOT = ROOT / "metadata" / "portfolio"
CATALOG_PATH = ROOT / "docs" / "dataset_catalog.md"
API_URL = "https://archive.ics.uci.edu/api/dataset?id={uci_id}"


def load_config() -> dict[str, Any]:
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    if len(config["datasets"]) != 20:
        raise ValueError("The portfolio manifest must contain exactly 20 datasets")
    return config


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def download(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": "NINR-dataset-portfolio/1.0"})
    with urllib.request.urlopen(request, timeout=180) as response, tempfile.NamedTemporaryFile(
        delete=False, dir=destination.parent
    ) as temporary:
        shutil.copyfileobj(response, temporary)
        temporary_path = Path(temporary.name)
    temporary_path.replace(destination)


def dataset_paths(spec: dict[str, Any]) -> dict[str, Path]:
    raw_dir = RAW_ROOT / spec["slug"]
    processed_dir = PROCESSED_ROOT / spec["slug"]
    metadata_dir = METADATA_ROOT / spec["slug"]
    return {
        "raw_dir": raw_dir,
        "metadata": raw_dir / "official_metadata.json",
        "data": raw_dir / "official_data.csv",
        "processed_dir": processed_dir,
        "participant": processed_dir / "participant.csv",
        "metadata_dir": metadata_dir,
    }


def acquire_dataset(spec: dict[str, Any], force: bool = False) -> dict[str, Any]:
    paths = dataset_paths(spec)
    metadata_url = API_URL.format(uci_id=spec["uci_id"])
    if force or not paths["metadata"].exists():
        download(metadata_url, paths["metadata"])
    payload = json.loads(paths["metadata"].read_text(encoding="utf-8-sig"))
    if payload.get("status") != 200:
        raise ValueError(f"UCI metadata request failed for {spec['slug']}: {payload}")
    metadata = payload["data"]
    if metadata["uci_id"] != spec["uci_id"]:
        raise ValueError(f"UCI ID mismatch for {spec['slug']}")
    data_url = metadata.get("data_url")
    if not data_url:
        raise ValueError(f"No official CSV data URL for {spec['slug']}")
    if force or not paths["data"].exists():
        download(data_url, paths["data"])
    return metadata


def acquire(force: bool = False) -> None:
    for spec in load_config()["datasets"]:
        print(f"Acquiring {spec['slug']} (UCI {spec['uci_id']})")
        acquire_dataset(spec, force=force)


def normalize_lookup(columns: list[str]) -> dict[str, str]:
    lookup: dict[str, str] = {}
    for column in columns:
        lookup.setdefault(column, column)
        lookup.setdefault(column.strip(), column)
        lookup.setdefault(column.lower(), column)
        lookup.setdefault(column.strip().lower(), column)
    return lookup


def clean_text(value: Any) -> str:
    """Remove source-formatting whitespace without changing substantive text."""
    if value is None:
        return ""
    return "\n".join(line.rstrip() for line in str(value).strip().splitlines())


def resolve_column(name: str, lookup: dict[str, str]) -> str | None:
    return lookup.get(name) or lookup.get(name.strip()) or lookup.get(name.lower()) or lookup.get(name.strip().lower())


def choose_columns(raw: pd.DataFrame, metadata: dict[str, Any], spec: dict[str, Any]) -> list[str]:
    columns = raw.columns.tolist()
    lookup = normalize_lookup(columns)
    variables = metadata.get("variables") or []
    roles: dict[str, list[str]] = {"ID": [], "Feature": [], "Target": []}
    demographics: list[str] = []
    for item in variables:
        resolved = resolve_column(str(item.get("name", "")), lookup)
        if not resolved:
            continue
        role = str(item.get("role") or "Feature")
        roles.setdefault(role, []).append(resolved)
        if item.get("demographic"):
            demographics.append(resolved)

    selected: list[str] = []

    def add(names: list[str]) -> None:
        for name in names:
            resolved = resolve_column(name, lookup)
            if resolved and resolved not in selected:
                selected.append(resolved)

    add(spec.get("priority_variables", []))
    add(roles.get("ID", []))
    add(demographics)
    add(spec.get("weight_variables", []))
    add(roles.get("Target", []))
    add(roles.get("Feature", []))
    add(columns)

    targets = []
    for name in roles.get("Target", []):
        if name not in targets:
            targets.append(name)
    chosen = selected[:30]
    for target in targets:
        if target not in chosen:
            if len(chosen) >= 30:
                chosen[-1] = target
            else:
                chosen.append(target)
    if len(chosen) < min(10, len(columns)):
        raise ValueError(f"Too few usable columns for {spec['slug']}: {len(chosen)}")
    return chosen


def source_missing_symbols(metadata: dict[str, Any], spec: dict[str, Any]) -> list[str]:
    symbol = metadata.get("missing_values_symbol")
    if symbol is None:
        symbols = [""]
    elif isinstance(symbol, list):
        symbols = [str(value) for value in symbol if value is not None]
    else:
        symbols = [str(symbol)]
    return list(dict.fromkeys(["", *symbols, *spec.get("additional_missing_symbols", [])]))


def replace_missing_code(frame: pd.DataFrame, symbol: str) -> pd.DataFrame:
    frame = frame.replace(symbol, pd.NA)
    try:
        numeric = float(symbol)
    except (TypeError, ValueError):
        return frame
    return frame.replace(numeric, pd.NA)


def count_missing_code(values: pd.DataFrame | pd.Series, symbol: str) -> int:
    count = int(values.astype("string").eq(symbol).sum().sum() if isinstance(values, pd.DataFrame) else values.astype("string").eq(symbol).sum())
    try:
        numeric = float(symbol)
    except (TypeError, ValueError):
        return count
    numeric_values = values.apply(pd.to_numeric, errors="coerce") if isinstance(values, pd.DataFrame) else pd.to_numeric(values, errors="coerce")
    numeric_count = int(numeric_values.eq(numeric).sum().sum() if isinstance(numeric_values, pd.DataFrame) else numeric_values.eq(numeric).sum())
    return max(count, numeric_count)


def stable_key(slug: str, seed: str, row_number: int, row: pd.Series, id_columns: list[str]) -> str:
    identity = "|".join(str(row[column]) for column in id_columns) if id_columns else str(row_number)
    return hashlib.sha256(f"{seed}:{slug}:{identity}:{row_number}".encode("utf-8")).hexdigest()


def risk_for_variable(variable: str, official: dict[str, Any], spec: dict[str, Any]) -> tuple[str, str]:
    flags: list[str] = []
    notes: list[str] = []
    role = str(official.get("role") or "")
    if role == "ID":
        flags.append("identifier_leakage")
        notes.append("Identifier; do not use as a model predictor.")
    if role == "Target":
        flags.extend(["outcome", "target_leakage"])
        notes.append("Official target; do not use to predict itself or another directly derived outcome.")
    if variable in spec.get("sensitive_variables", []) or official.get("demographic"):
        flags.append("proxy_discrimination")
        notes.append("Sensitive or demographic attribute; audit subgroup representation and errors.")
    if variable in spec.get("post_outcome_variables", []):
        flags.append("post_outcome_measurement")
        notes.append("Timing may be at or after the prediction point; define the prediction horizon before use.")
    return "|".join(dict.fromkeys(flags)), " ".join(dict.fromkeys(notes))


def prepare_dataset(spec: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    paths = dataset_paths(spec)
    payload = json.loads(paths["metadata"].read_text(encoding="utf-8-sig"))
    metadata = payload["data"]
    raw = pd.read_csv(paths["data"], keep_default_na=False, low_memory=False)
    raw.columns = [str(column) for column in raw.columns]
    selected = choose_columns(raw, metadata, spec)
    missing_symbols = source_missing_symbols(metadata, spec)
    working = raw[selected].copy()
    for symbol in missing_symbols:
        if symbol != "":
            working = replace_missing_code(working, symbol)
    working = working.replace("", pd.NA)

    official_by_name: dict[str, dict[str, Any]] = {}
    lookup = normalize_lookup(raw.columns.tolist())
    for item in metadata.get("variables") or []:
        resolved = resolve_column(str(item.get("name", "")), lookup)
        if resolved:
            official_by_name.setdefault(resolved, item)
    id_columns = [
        column for column in selected
        if str(official_by_name.get(column, {}).get("role") or "") == "ID"
    ]
    ranks = [
        stable_key(spec["slug"], config["sample_seed"], index, raw.loc[index], id_columns)
        for index in raw.index
    ]
    sample_n = min(config["sample_size"], len(raw))
    chosen_index = pd.Series(ranks, index=raw.index).sort_values(kind="stable").head(sample_n).index
    participant = working.loc[chosen_index].copy()
    participant.insert(0, "portfolio_row_id", range(1, len(participant) + 1))

    paths["processed_dir"].mkdir(parents=True, exist_ok=True)
    paths["metadata_dir"].mkdir(parents=True, exist_ok=True)
    participant.to_csv(paths["participant"], index=False, lineterminator="\n")

    dictionary_rows: list[dict[str, Any]] = []
    risk_rows: list[dict[str, Any]] = []
    missing_rows: list[dict[str, Any]] = []
    for column in raw.columns:
        official = official_by_name.get(column, {})
        risk_flags, risk_note = risk_for_variable(column, official, spec)
        series = raw[column]
        observed_codes: list[str] = []
        if str(official.get("type") or "").lower() == "categorical" or series.nunique(dropna=False) <= 25:
            observed_codes = sorted({str(value) for value in series.unique()})[:100]
        missing_count = sum(count_missing_code(series, symbol) for symbol in missing_symbols)
        dictionary_rows.append({
            "variable": column,
            "selected_for_participant": column in selected,
            "role": official.get("role", ""),
            "type": official.get("type", ""),
            "demographic": official.get("demographic", ""),
            "description": clean_text(official.get("description", "")),
            "units": official.get("units", ""),
            "official_missing_values": official.get("missing_values", ""),
            "official_missing_symbol": json.dumps(missing_symbols),
            "observed_codes": json.dumps(observed_codes, ensure_ascii=False),
            "weighting_variable": column in spec.get("weight_variables", []),
            "risk_flags": risk_flags,
            "risk_note": risk_note,
            "definition_source": f"UCI API metadata, dataset {spec['uci_id']}",
        })
        if risk_flags:
            risk_rows.append({"variable": column, "risk_flags": risk_flags, "note": risk_note})
        if missing_count:
            missing_rows.append({
                "variable": column,
                "raw_missing_symbols": json.dumps(missing_symbols),
                "raw_missing_count": missing_count,
                "participant_representation": "blank/NA",
            })

    dictionary_rows.insert(0, {
        "variable": "portfolio_row_id",
        "selected_for_participant": True,
        "role": "Derived ID",
        "type": "Integer",
        "demographic": "",
        "description": "Sequential row identifier assigned after deterministic sampling.",
        "units": "",
        "official_missing_values": "no",
        "official_missing_symbol": "[]",
        "observed_codes": "[]",
        "weighting_variable": False,
        "risk_flags": "identifier_leakage",
        "risk_note": "Derived identifier; do not use as a model predictor.",
        "definition_source": "NINR portfolio deterministic transformation",
    })
    dictionary = pd.DataFrame(dictionary_rows)
    dictionary.to_csv(paths["metadata_dir"] / "data_dictionary.csv", index=False, lineterminator="\n")
    (paths["metadata_dir"] / "data_dictionary.json").write_text(
        json.dumps(dictionary_rows, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    pd.DataFrame(risk_rows, columns=["variable", "risk_flags", "note"]).to_csv(
        paths["metadata_dir"] / "risk_flags.csv", index=False, lineterminator="\n"
    )
    pd.DataFrame(missing_rows, columns=[
        "variable", "raw_missing_symbols", "raw_missing_count", "participant_representation"
    ]).to_csv(paths["metadata_dir"] / "missing_values.csv", index=False, lineterminator="\n")

    value_label_rows: list[dict[str, Any]] = []
    for row in dictionary_rows:
        codes = json.loads(row["observed_codes"])
        if not codes:
            continue
        for code in codes:
            if code in missing_symbols:
                continue
            value_label_rows.append({
                "variable": row["variable"],
                "code": code,
                "official_description": row["description"],
                "label_status": "Raw category code observed in official source; use the official description/codebook for meaning.",
            })
    pd.DataFrame(value_label_rows, columns=[
        "variable", "code", "official_description", "label_status"
    ]).to_csv(paths["metadata_dir"] / "value_labels.csv", index=False, lineterminator="\n")

    targets = [
        {
            "variable": column,
            "description": clean_text(official_by_name.get(column, {}).get("description", "")),
            "observed_values": sorted({str(value) for value in raw[column].unique()})[:100]
            if raw[column].nunique(dropna=False) <= 100 else [],
        }
        for column in selected
        if str(official_by_name.get(column, {}).get("role") or "") == "Target"
    ]
    provenance = {
        "uci_id": spec["uci_id"],
        "title": clean_text(metadata["name"]),
        "official_source": config["official_repository"],
        "repository_url": metadata["repository_url"],
        "data_url": metadata["data_url"],
        "dataset_doi": metadata.get("dataset_doi"),
        "dataset_year": metadata.get("year_of_dataset_creation"),
        "current_record_version": f"UCI record last updated {metadata.get('last_updated')}",
        "access_date": config["access_date"],
        "license": metadata.get("license"),
        "raw_data_sha256": sha256(paths["data"]),
        "official_metadata_sha256": sha256(paths["metadata"]),
        "raw_rows": len(raw),
        "raw_columns": len(raw.columns),
        "participant_rows": len(participant),
        "participant_columns": len(participant.columns),
        "participant_sha256": sha256(paths["participant"]),
        "selected_variables": ["portfolio_row_id", *selected],
        "missing_value_codes": missing_symbols,
        "weighting_variables": spec.get("weight_variables", []),
        "outcomes": targets,
        "transformations": [
            "Downloaded the official UCI normalized CSV and API metadata without modifying the raw files.",
            "Selected 10-30 source variables using the reviewed manifest, official roles, and source order.",
            "Converted documented source missing symbols to blank/NA only in the participant derivative.",
            f"Selected {sample_n} rows by deterministic SHA-256 rank using the portfolio seed.",
            "Added portfolio_row_id after sampling and wrote UTF-8 CSV with LF line endings.",
        ],
        "software": {
            "python": platform.python_version(),
            "pandas": pd.__version__,
            "platform": platform.platform(),
        },
    }
    (paths["metadata_dir"] / "provenance.json").write_text(
        json.dumps(provenance, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return {"metadata": metadata, "provenance": provenance, "selected": selected, "raw": raw}


def validate_dataset(spec: dict[str, Any], prepared: dict[str, Any] | None = None) -> dict[str, Any]:
    paths = dataset_paths(spec)
    payload = json.loads(paths["metadata"].read_text(encoding="utf-8-sig"))
    metadata = payload["data"]
    raw = pd.read_csv(paths["data"], keep_default_na=False, low_memory=False)
    participant = pd.read_csv(paths["participant"], keep_default_na=False)
    dictionary = pd.read_csv(paths["metadata_dir"] / "data_dictionary.csv", keep_default_na=False)
    provenance = json.loads((paths["metadata_dir"] / "provenance.json").read_text(encoding="utf-8"))
    checks: list[dict[str, Any]] = []

    def check(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    metadata_rows = metadata.get("num_instances")
    expected_rows = spec.get("expected_normalized_rows", metadata_rows)
    check("official source has rows", len(raw) > 0, f"observed {len(raw)}")
    check(
        "row count agrees with official metadata",
        expected_rows is None or len(raw) == int(expected_rows),
        f"metadata={metadata_rows}, expected official CSV={expected_rows}, observed={len(raw)}"
        + (f"; {spec['source_count_note']}" if spec.get("source_count_note") else ""),
    )
    check("participant row range", 700 <= len(participant) <= 10000, f"observed {len(participant)}")
    check("participant variable range", 10 <= len(participant.columns) <= 31, f"observed {len(participant.columns)} including derived ID")
    check("derived row ID unique", participant["portfolio_row_id"].is_unique, "portfolio_row_id is unique")
    check("dictionary covers participant", set(participant.columns).issubset(set(dictionary["variable"])), "all participant variables documented")
    configured_missing = source_missing_symbols(metadata, spec)
    residual_missing_codes = {
        symbol: count_missing_code(participant, symbol)
        for symbol in configured_missing if symbol
    }
    check(
        "raw missing codes removed from participant file",
        not any(residual_missing_codes.values()),
        str(residual_missing_codes),
    )
    check("participant hash matches provenance", sha256(paths["participant"]) == provenance["participant_sha256"], "checksum verified")
    check("raw hash matches provenance", sha256(paths["data"]) == provenance["raw_data_sha256"], "checksum verified")
    check("official URL recorded", provenance["data_url"] == metadata["data_url"], metadata["data_url"])
    target_names = {
        str(item["name"]).strip().lower()
        for item in (metadata.get("variables") or [])
        if item.get("role") == "Target"
    }
    selected_names = {column.strip().lower() for column in participant.columns}
    check("official target retained", not target_names or bool(target_names & selected_names), f"targets={sorted(target_names)}")

    report = {
        "dataset": spec["slug"],
        "validated_at": datetime.now(timezone.utc).isoformat(),
        "passed": all(item["passed"] for item in checks),
        "checks": checks,
    }
    (paths["metadata_dir"] / "validation_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    return report


def prepare_and_validate() -> list[dict[str, Any]]:
    config = load_config()
    summaries = []
    failures = []
    for spec in config["datasets"]:
        print(f"Preparing {spec['slug']}")
        prepared = prepare_dataset(spec, config)
        report = validate_dataset(spec, prepared)
        if not report["passed"]:
            failures.append(spec["slug"])
        summaries.append({"spec": spec, **prepared, "report": report})
    write_catalog(summaries)
    write_catalog_csv(summaries)
    if failures:
        raise AssertionError(f"Portfolio validation failed: {', '.join(failures)}")
    return summaries


def write_catalog_csv(summaries: list[dict[str, Any]]) -> None:
    METADATA_ROOT.mkdir(parents=True, exist_ok=True)
    rows = []
    for item in summaries:
        metadata = item["metadata"]
        provenance = item["provenance"]
        rows.append({
            "slug": item["spec"]["slug"],
            "uci_id": item["spec"]["uci_id"],
            "title": clean_text(metadata["name"]),
            "category": item["spec"]["category"],
            "raw_rows": provenance["raw_rows"],
            "participant_rows": provenance["participant_rows"],
            "participant_columns": provenance["participant_columns"],
            "dataset_year": provenance["dataset_year"],
            "record_version": provenance["current_record_version"],
            "repository_url": provenance["repository_url"],
            "doi": provenance["dataset_doi"],
            "weighting_variables": "|".join(provenance["weighting_variables"]),
            "validation_passed": item["report"]["passed"],
        })
    pd.DataFrame(rows).to_csv(METADATA_ROOT / "catalog.csv", index=False, lineterminator="\n")


def write_catalog(summaries: list[dict[str, Any]]) -> None:
    config = load_config()
    by_slug = {item["spec"]["slug"]: item for item in summaries}
    pathways = [
        (
            "Clinical care and outcomes",
            "Hospital care, prognosis, complications, trials, and infectious disease",
            [
                "diabetes_readmission",
                "support2_serious_illness",
                "myocardial_infarction_complications",
                "aids_clinical_trial_175",
                "hepatitis_c_treatment",
            ],
        ),
        (
            "Symptoms, screening, and monitoring",
            "Physiologic signals, symptom severity, diagnostic support, and measurement",
            [
                "cardiotocography",
                "parkinsons_telemonitoring",
                "diabetic_retinopathy",
                "infrared_thermography_temperature",
                "eeg_eye_state",
            ],
        ),
        (
            "Health behavior, SDOH, and workforce",
            "Behavior, substance use, work, education, income, and community conditions",
            [
                "obesity_lifestyle",
                "drug_consumption",
                "workplace_absenteeism",
                "student_dropout_sdoh",
                "adult_income_sdoh",
                "communities_crime_sdoh",
            ],
        ),
        (
            "Environment and sensors",
            "Air quality, indoor environments, sensing, and physical-activity settings",
            [
                "air_quality_sensors",
                "beijing_pm25",
                "room_occupancy_environment",
                "bike_sharing_environment",
            ],
        ),
    ]
    lines = [
        "# Dataset Explorer",
        "",
        "### Choose a workshop dataset by question, not by algorithm",
        "",
        "> **20 documented options · 4 research pathways · official sources · participant-ready files**",
        "",
        "This page helps NINR AI Summer Research Intensive participants move from an area of interest to a manageable dataset and research question. Every definition comes from the official UCI Machine Learning Repository record supplied by the original contributor; no Kaggle or third-party mirror is used. Versions were checked on " + config["access_date"] + ".",
        "",
        "Participant files contain approximately 1,000–5,000 observations and 10–30 source variables, plus `portfolio_row_id`. The occupational absenteeism source contains only 740 records, so its participant file retains all 740 and is the documented size exception.",
        "",
        "[How to use the files](participant_quickstart.md) · [Return to the workshop home](../README.md)",
        "",
        "## Good first choices",
        "",
        "| If you want to practice… | Start with… | A question you could ask |",
        "|---|---|---|",
        "| Classification with a clear clinical outcome | [Diabetes readmission](#diabetes-readmission) | Which pre-admission utilization measures are associated with early readmission? |",
        "| Regression with repeated observations | [Parkinson telemonitoring](#parkinsons-telemonitoring) | Which voice features track symptom severity? |",
        "| Health behavior and a multiclass outcome | [Obesity and lifestyle](#obesity-lifestyle) | How are activity and eating patterns associated with obesity category? |",
        "| Fairness and social determinants | [Adult income](#adult-income-sdoh) | How do model errors differ across demographic groups? |",
        "| Sensor-based classification | [Room occupancy](#room-occupancy-environment) | Which indoor sensors best distinguish occupancy levels? |",
        "| A small, approachable workforce dataset | [Workplace absenteeism](#workplace-absenteeism) | Which work and health factors relate to absence duration? |",
        "",
        "These are starting points, not rankings. Choose the dataset whose population, timing, and limitations best fit your question.",
        "",
        "## Browse by research area",
        "",
    ]
    for pathway, description, slugs in pathways:
        lines.extend([
            f"### {pathway}",
            "",
            description + ".",
            "",
            "| Dataset | Participant file | Outcome | Best for |",
            "|---|---:|---|---|",
        ])
        for slug in slugs:
            item = by_slug[slug]
            spec = item["spec"]
            metadata = item["metadata"]
            provenance = item["provenance"]
            outcomes = provenance["outcomes"]
            if len(outcomes) > 3:
                outcome_text = f"{len(outcomes)} documented targets"
            else:
                outcome_text = (
                    ", ".join(f"`{value['variable']}`" for value in outcomes)
                    or "Choose based on question"
                )
            lines.append(
                f"| [{clean_text(metadata['name'])}](#{slug.replace('_', '-')}) | "
                f"{provenance['participant_rows']:,} × {provenance['participant_columns'] - 1} | {outcome_text} | {spec['fit']} |"
            )
        lines.append("")
    lines.extend([
        "## Compare all 20",
        "",
        "| Dataset | Research area | Shape | Weight |",
        "|---|---|---:|---|",
    ])
    for item in summaries:
        spec = item["spec"]
        metadata = item["metadata"]
        provenance = item["provenance"]
        weight = ", ".join(provenance["weighting_variables"]) or "None supplied"
        lines.append(
            f"| [{clean_text(metadata['name'])}](#{spec['slug'].replace('_', '-')}) | {spec['category']} | "
            f"{provenance['participant_rows']:,} × {provenance['participant_columns'] - 1} | {weight} |"
        )
    lines.extend([
        "",
        "## Pause before modeling",
        "",
        "> A high-performing model can still answer the wrong question, use information unavailable at decision time, or reproduce inequity.",
        "",
        "- UCI-hosted clinical and sensor datasets are generally convenience samples, not nationally representative surveys. Only use weights when the source explicitly provides one.",
        "- Define the prediction time before selecting variables. Measurements collected after admission, treatment, or outcome determination can create leakage.",
        "- Demographic and geographic variables can encode structural inequity and proxy protected characteristics. Audit missingness, representation, and subgroup errors.",
        "- Community-level associations do not establish individual-level relationships; avoid ecological fallacy.",
        "- The obesity dataset includes synthetic records according to its official documentation; it is useful for teaching but not population inference.",
        "- Dataset age, geography, and collection context limit transportability to current clinical practice or other populations.",
        "",
        "## Full dataset cards",
        "",
        "Open a card to see the official source, version, selected variables, research questions, and audit files.",
        "",
    ])
    for item in summaries:
        spec = item["spec"]
        metadata = item["metadata"]
        provenance = item["provenance"]
        outcomes = provenance["outcomes"]
        outcome_text = ", ".join(f"`{value['variable']}`" for value in outcomes) or "No official target designated"
        selected = ", ".join(f"`{name}`" for name in provenance["selected_variables"] if name != "portfolio_row_id")
        lines.extend([
            f"<a id=\"{spec['slug'].replace('_', '-')}\"></a>",
            "",
            "<details>",
            f"<summary><strong>{clean_text(metadata['name'])}</strong> — {spec['fit']}</summary>",
            "",
            f"- **Theme:** {spec['category']}",
            f"- **Why choose it:** {spec['fit']}",
            f"- **Official source:** [UCI dataset {spec['uci_id']}]({metadata['repository_url']})",
            f"- **Version:** dataset year {metadata.get('year_of_dataset_creation')}; record last updated {metadata.get('last_updated')}",
            f"- **Source/participant size:** {provenance['raw_rows']:,} source rows; {provenance['participant_rows']:,} participant rows; {provenance['participant_columns'] - 1} source variables",
            *( [f"- **Source count caveat:** {spec['source_count_note']}"] if spec.get("source_count_note") else [] ),
            f"- **Official target(s):** {outcome_text}",
            f"- **Weighting:** {', '.join(provenance['weighting_variables']) if provenance['weighting_variables'] else 'No weighting variable supplied'}",
            f"- **Selected variables:** {selected}",
            "- **Potential research questions:**",
            "",
        ])
        lines.extend(f"  {index}. {question}" for index, question in enumerate(spec["questions"], 1))
        lines.extend([
            "",
            f"Artifacts: [`participant.csv`](../data/processed/portfolio/{spec['slug']}/participant.csv) · "
            f"[`data dictionary`](../metadata/portfolio/{spec['slug']}/data_dictionary.csv) · "
            f"[`provenance`](../metadata/portfolio/{spec['slug']}/provenance.json) · "
            f"[`risk flags`](../metadata/portfolio/{spec['slug']}/risk_flags.csv) · "
            f"[`validation`](../metadata/portfolio/{spec['slug']}/validation_report.json)",
            "",
            "</details>",
            "",
        ])
    CATALOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CATALOG_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_lock() -> None:
    config = load_config()
    datasets = []
    for spec in config["datasets"]:
        paths = dataset_paths(spec)
        payload = json.loads(paths["metadata"].read_text(encoding="utf-8-sig"))["data"]
        datasets.append({
            "slug": spec["slug"],
            "uci_id": spec["uci_id"],
            "name": payload["name"],
            "data_url": payload["data_url"],
            "repository_url": payload["repository_url"],
            "dataset_year": payload.get("year_of_dataset_creation"),
            "last_updated": payload.get("last_updated"),
            "data_sha256": sha256(paths["data"]),
            "metadata_sha256": sha256(paths["metadata"]),
        })
    LOCK_PATH.write_text(
        json.dumps({"access_date": config["access_date"], "datasets": datasets}, indent=2),
        encoding="utf-8",
    )


def verify_lock() -> None:
    if not LOCK_PATH.exists():
        raise FileNotFoundError("Missing source lock; run `python portfolio_pipeline.py lock` after review")
    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    failures = []
    for item in lock["datasets"]:
        spec = next(spec for spec in load_config()["datasets"] if spec["slug"] == item["slug"])
        paths = dataset_paths(spec)
        if sha256(paths["data"]) != item["data_sha256"] or sha256(paths["metadata"]) != item["metadata_sha256"]:
            failures.append(item["slug"])
    if failures:
        raise ValueError(f"Source-lock checksum mismatch: {', '.join(failures)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["acquire", "prepare", "validate", "catalog", "lock", "verify-lock", "all"])
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if args.command in {"acquire", "all"}:
        acquire(force=args.force)
    if args.command in {"prepare", "all"}:
        prepare_and_validate()
    elif args.command == "validate":
        failures = [spec["slug"] for spec in load_config()["datasets"] if not validate_dataset(spec)["passed"]]
        if failures:
            raise AssertionError(f"Portfolio validation failed: {', '.join(failures)}")
    elif args.command == "catalog":
        summaries = []
        config = load_config()
        for spec in config["datasets"]:
            paths = dataset_paths(spec)
            summaries.append({
                "spec": spec,
                "metadata": json.loads(paths["metadata"].read_text(encoding="utf-8-sig"))["data"],
                "provenance": json.loads((paths["metadata_dir"] / "provenance.json").read_text(encoding="utf-8")),
                "report": json.loads((paths["metadata_dir"] / "validation_report.json").read_text(encoding="utf-8")),
            })
        write_catalog(summaries)
        write_catalog_csv(summaries)
    elif args.command == "lock":
        write_lock()
    elif args.command == "verify-lock":
        verify_lock()
    print("Portfolio command completed successfully")


if __name__ == "__main__":
    main()
