# NINR AI Summer Research Intensive

### Participant-ready health data for learning responsible AI

> **20 documented datasets · beginner-friendly CSV files · official sources only · reproducible preparation**

This repository supports hands-on learning for nursing scientists at the **NINR Artificial Intelligence Summer Research Intensive**. Every dataset now centers a direct nursing-science topic: clinical care, symptoms, patient outcomes, screening, health behavior, caregiving, health services, workforce, patient experience, or population and environmental health. Original public data are turned into approachable workshop files while preserving the documentation, provenance, and analytic cautions needed for responsible health research.

No prior Python or machine-learning experience is required to begin.

▶ **[Watch the two-minute video tour](media/ninr_ai_bootcamp_walkthrough.mp4)** for a narrated overview of the datasets, learning activities, and teaching materials.

## Start here

| I want to… | Go to… |
|---|---|
| Complete the guided Day 1 activity | [`01_day1_python_and_clinical_data.ipynb`](notebooks/01_day1_python_and_clinical_data.ipynb) |
| Explore multimodal symptom prediction with real public data | [Interactive Activity 2](docs/multimodal_symptom_trajectory_activity.md) |
| Choose a dataset for a team or capstone | [Dataset Explorer](docs/dataset_catalog.md) |
| Learn how the files fit together | [Participant Quick Start](docs/participant_quickstart.md) |
| See the Day 1 variable definitions | [Day 1 data dictionary](docs/day1_data_dictionary.md) |
| Reproduce or audit the data preparation | [Reproducibility guide](#reproduce-and-verify) |

### The shortest path for participants

1. Open the [guided notebook](notebooks/01_day1_python_and_clinical_data.ipynb) in Google Colab.
2. Upload [`diabetes_130_hospitals_participant.csv`](data/processed/diabetes_130_hospitals_participant.csv).
3. Run the notebook from top to bottom, changing one question, variable, or plot as you go.

For a project beyond the guided lab, use the [Dataset Explorer](docs/dataset_catalog.md) to compare 20 options by research area, outcome, size, and analytic caution.

## What is included

The collection spans four workshop-friendly pathways:

| Pathway | Example topics | Suggested starting point |
|---|---|---|
| **Clinical care and outcomes** | readmission, serious illness, acute care, clinical trials | [Diabetes readmission](docs/dataset_catalog.md#diabetes-readmission) |
| **Symptoms, screening, and monitoring** | Parkinson symptoms, fetal monitoring, EEG, temperature screening | [Parkinson telemonitoring](docs/dataset_catalog.md#parkinsons-telemonitoring) |
| **Health behavior, aging, and workforce** | obesity, substance use, sleep, caregiving, health-service use, absenteeism | [Healthy aging](docs/dataset_catalog.md#healthy-aging-poll) |
| **Environment and care quality** | air quality, nurse communication, discharge information, patient experience | [Hospital HCAHPS](docs/dataset_catalog.md#hospital-patient-experience) |

Each portfolio dataset includes:

- a participant-ready CSV;
- a machine-readable data dictionary;
- documented missing-value codes and categorical labels;
- outcome and weighting-variable documentation;
- potential research questions;
- leakage, confounding, timing, and proxy-discrimination flags;
- provenance and an automated validation report.

## A responsible-AI learning path

```text
Research question → Understand the data → Explore quality and bias
                  → Build a simple model → Evaluate across groups
                  → Explain limitations and next steps
```

The datasets are teaching resources, not plug-and-play clinical tools. Most are convenience samples and should not be described as nationally representative. Define the prediction time before selecting predictors, check whether repeated observations come from the same person, and review the supplied risk flags before modeling.

## Reproduce and verify

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements-pipeline.txt

python portfolio_pipeline.py acquire
python portfolio_pipeline.py verify-lock
python portfolio_pipeline.py prepare
python -m unittest discover -s tests -v
```

The raw portfolio downloads are preserved unchanged under `data/raw/portfolio/` and excluded from Git because they can be rebuilt. Their official URLs, versions, and SHA-256 hashes are pinned in [`portfolio_sources.lock.json`](config/portfolio_sources.lock.json). Participant files and metadata are committed under `data/processed/portfolio/` and `metadata/portfolio/`.

The detailed diabetes pipeline can be rebuilt separately:

```bash
python pipeline.py all
```

Use `python pipeline.py acquire --force` only when intentionally refreshing the source. A changed archive fails checksum verification until the new version has been reviewed and deliberately accepted.

## Data standards

- **Official sources:** original contributor records and official government releases, including CMS patient-experience data, plus the original diabetes study article archived by NIH PubMed Central.
- **No mirrors:** no Kaggle or third-party dataset copies when an original source is available.
- **Originals preserved:** preparation never rewrites the downloaded source files.
- **Deterministic samples:** participant subsets can be reproduced from the same source and configuration.
- **Definitions traceable:** variable meanings come from official codebooks and source documentation; undocumented meanings are not invented.
- **Audit-friendly:** every transformation, checksum, dependency, and validation result is recorded.

## Repository map

```text
notebooks/                         guided participant and solution notebooks
activities/                        reproducible public-data preparation scripts
docs/dataset_catalog.md            visual dataset explorer and research questions
docs/participant_quickstart.md     plain-language orientation for participants
docs/multimodal_symptom_trajectory_activity.md  Activity 2 overview and source rationale
docs/activities/                   step-by-step participant walkthroughs
docs/teaching_guides/              facilitation plans, prompts, and rubrics
data/processed/portfolio/          20 participant-ready CSV files
metadata/portfolio/                dictionaries, labels, risks, provenance, validation
config/portfolio.json              reviewed dataset and variable selections
config/portfolio_sources.lock.json official source versions and checksums
portfolio_pipeline.py              portfolio acquisition, preparation, and validation
pipeline.py                        detailed diabetes pipeline
tests/                             automated artifact checks
```

## Detailed diabetes teaching dataset

The guided Day 1 notebook uses **Diabetes 130-US Hospitals for Years 1999–2008**, an official UCI dataset with 101,766 inpatient encounters. The reproducible participant file contains 5,000 encounters and 26 variables related to demographics, health-services use, encounter intensity, glycemic testing, treatment, and readmission.

- [Official UCI record](https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008)
- [Dataset DOI: 10.24432/C5230J](https://doi.org/10.24432/C5230J)
- [Original study article](https://pubmed.ncbi.nlm.nih.gov/24804245/)
- Dataset years: 1999–2008
- License: CC BY 4.0

The official readmission outcome is retained as `<30`, `>30`, or `NO`, and the derived `readmitted_30d` field is documented in the data dictionary. See [research questions and analytic risks](docs/research_questions_and_risks.md) for appropriate ways to use it.
