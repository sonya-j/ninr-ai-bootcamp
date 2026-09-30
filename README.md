# NINR AI Summer Research Intensive — reproducible health-data pipeline

This repository acquires, preserves, prepares, documents, and validates a participant-ready clinical dataset. The pipeline uses only the official UCI Machine Learning Repository record, its original archive, and the original article archived by NIH PubMed Central. It does not use Kaggle or another mirror.

## Included dataset and current version

**Diabetes 130-US Hospitals for Years 1999–2008** contains 101,766 inpatient diabetes encounters from 130 U.S. hospitals and integrated delivery networks.

- Official source: [UCI dataset record](https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008)
- Dataset DOI: [10.24432/C5230J](https://doi.org/10.24432/C5230J)
- Dataset years: 1999–2008
- UCI record version: last updated September 24, 2024
- Pipeline access date: September 30, 2026
- UCI files: `diabetic_data.csv` and `IDS_mapping.csv`
- Original article: Strack et al. (2014), [DOI 10.1155/2014/781670](https://doi.org/10.1155/2014/781670), [NIH record](https://pubmed.ncbi.nlm.nih.gov/24804245/)
- License: CC BY 4.0

The exact official ZIP and source files are pinned with SHA-256 checksums in `config/datasets.json`. The original files under `data/raw/` are never rewritten by the preparation step.

## Reproduce the pipeline

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements-pipeline.txt
python pipeline.py all
python -m unittest discover -s tests -v
```

Commands can also be run separately:

```bash
python pipeline.py acquire   # download/verify official originals and documentation
python pipeline.py prepare   # rebuild all derived files
python pipeline.py validate  # run automated integrity and content checks
```

Use `python pipeline.py acquire --force` only when intentionally refreshing the downloaded copies. A changed UCI archive will fail the pinned checksum until its new version is reviewed and the manifest is deliberately updated.

## Participant dataset

The pipeline deterministically selects 5,000 encounters by SHA-256 ranking of `seed:encounter_id`; this avoids dependence on dataframe row order or a library-specific random sampler. The output contains 26 variables relevant to demographics, health services use, encounter intensity, glycemic testing, treatment, and readmission:

`data/processed/diabetes_130_hospitals_participant.csv`

The official three-category outcome is retained:

- `<30`: inpatient readmission in less than 30 days;
- `>30`: inpatient readmission after 30 days;
- `NO`: no recorded readmission.

The pipeline also derives `readmitted_30d`, equal to 1 only for `<30` and 0 otherwise. The participant sample contains 561 `<30`, 1,753 `>30`, and 2,686 `NO` encounters (11.22% early readmission).

Raw `?` missing-value codes are converted to blank/NA only in the derived participant CSV. `None` for `A1Cresult` and `max_glu_serum` means the test was not taken and is retained as a category. Official `NULL`, `Not Available`, `Not Mapped`, and `Unknown/Invalid` ID-mapping labels are retained and documented rather than silently recoded.

When loading the participant CSV with pandas, preserve the official literal `NULL` label while treating blank fields as missing:

```python
import pandas as pd

data = pd.read_csv(path, keep_default_na=False, na_values=[""])
```

The source provides no survey or analytic weighting variable. It is a clinical database, not a documented probability sample; participant analyses should not be presented as nationally representative.

## Documentation and audit artifacts

- `metadata/data_dictionary.csv` and `.json`: official definitions plus derived-field lineage, missing codes, selection status, and risk flags.
- `metadata/value_labels.csv`: official categorical labels, including the bundled ID mappings.
- `metadata/missing_values.csv`: missing/unavailable codes and observed raw counts.
- `metadata/risk_flags.csv`: leakage, timing, confounding, and proxy-discrimination flags.
- `metadata/provenance.json`: URLs, access date, version, checksums, transformations, output hash, and software environment.
- `metadata/dataset_summary.json`: outcome definition, counts, dimensions, and weighting status.
- `metadata/validation_report.json`: machine-readable results of 19 automated checks.
- `docs/research_questions_and_risks.md`: five possible research questions and analytic cautions.
- `data/raw/uci_diabetes_296/documentation/`: the official UCI API record and the original article’s full-text XML from NIH.

Variable meanings are taken from the official UCI metadata, `IDS_mapping.csv`, and the original article. Where the source does not provide a label set (for example, a full payer-code crosswalk), the project does not invent one.

## Teaching notebooks

The notebooks in `notebooks/` load the validated participant CSV and then select a smaller set of introductory variables for Day 1 exercises. The full 26-variable derivative supports later work on readmission, responsible modeling, health-service utilization, and subgroup assessment.

## Repository structure

```text
config/datasets.json                 pinned source manifest
pipeline.py                          acquisition, preparation, and validation CLI
data/raw/                            unchanged official archive/files/docs
data/processed/                      participant-ready CSV
metadata/                            dictionaries, provenance, labels, and reports
docs/                                research questions and teaching documentation
notebooks/                           participant and solution notebooks
tests/                               automated artifact tests
requirements-pipeline.txt            pinned pipeline dependency
```
