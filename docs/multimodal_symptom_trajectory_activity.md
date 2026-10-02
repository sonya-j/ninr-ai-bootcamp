# Multimodal Fatigue Trajectory Activity

## The question, made testable

The workshop's broad question is:

> Can multimodal AI predict symptom trajectories using patient-reported, wearable, EHR, and contextual data?

No single unrestricted public dataset located for this workshop contained all four modalities with repeated symptom outcomes. This activity therefore asks a narrower question that the selected public data can actually answer:

> **Can today's patient-reported fatigue, wearable signals, and time context predict tomorrow's fatigue rating?**

Electronic health record data are **not** present. The activity treats that absence as a scientific finding, not a gap to disguise. Participants first test the three available modalities, then design an EHR extension and identify what new governance, harmonization, and validation it would require.

No prior AI, machine-learning, statistics, or coding knowledge is assumed. The participant experience begins with a manual prediction, introduces one term at a time, uses a no-ML comparison rule before any algorithm, and provides “do / notice / explain” prompts throughout.

## Start here

- **Participants:** [follow the zero-background, step-by-step activity walkthrough](activities/multimodal_fatigue_walkthrough.md)
- **Instructors:** [use the teaching guide](teaching_guides/multimodal_fatigue_teaching_guide.md)
- **Interactive notebook:** [open in Google Colab](https://colab.research.google.com/github/sonya-j/ninr-ai-bootcamp/blob/main/notebooks/02_multimodal_symptom_trajectories.ipynb)

## Public dataset

The activity uses **Continuous multi-sensor wearable data and daily subject-reported fatigue of healthy adults**, version 1, published by the original investigators on Zenodo:

- [Official dataset record and downloads](https://doi.org/10.5281/zenodo.4266157)
- [Open-access study article](https://pmc.ncbi.nlm.nih.gov/articles/PMC7768149/)
- License: CC BY 4.0
- Original release: November 10, 2020
- Source data: 28 healthy adults and 973 recording days; the authors report 27 participants and 405 days with matched wearable and patient-reported data in their analysis

The repository preparation script independently joins daily reports to sensor dates. It produces 450 matched participant-days and 336 rows with a report on the next calendar day. These counts differ from the article's analyzed sample because this teaching pipeline does not reproduce the authors' preprocessing and imputation rules.

## What is—and is not—in the activity

| Modality | Available? | Examples used |
|---|---:|---|
| Patient-reported | Yes | Overall fatigue, physical exhaustion, mental exhaustion, change from yesterday, sport today |
| Wearable | Yes | Activity, energy expenditure, heart rate, HRV, respiration, steps, skin temperature, wear minutes |
| Time context | Yes | Study day, day of week, weekend |
| EHR | **No** | No diagnoses, medications, encounters, laboratory results, or clinical notes are supplied |
| Outcome | Yes | Next-calendar-day 1–10 fatigue rating |

## Reproducibility artifacts

- [Prepared participant-day CSV](../data/processed/multimodal_symptom_trajectories/participant_day.csv)
- [Machine-readable data dictionary](../metadata/multimodal_symptom_trajectories/data_dictionary.csv)
- [Missingness report](../metadata/multimodal_symptom_trajectories/missing_values.csv)
- [Risk flags](../metadata/multimodal_symptom_trajectories/risk_flags.csv)
- [Provenance record](../metadata/multimodal_symptom_trajectories/provenance.json)
- [Validation report](../metadata/multimodal_symptom_trajectories/validation_report.json)
- [Download and preparation script](../activities/multimodal_symptom_trajectories/prepare_public_fatigue_data.py)

The unchanged original files are downloaded from Zenodo into a gitignored `data/raw/` directory. Zenodo MD5 checksums are verified before preparation.

## Claims this activity permits

Participants may report comparative test-set performance within this small teaching sample. They may **not** claim that the model is clinically valid, works in people with illness, demonstrates benefit from EHR data, or should guide care. The sample contains healthy adults, is small, has repeated observations, and includes potentially informative sensor non-wear and missed reports.
