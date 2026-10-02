# Multimodal Symptom Trajectory Activity

## Research question

> Can multimodal AI predict symptom trajectories using patient-reported, wearable, EHR, and contextual data?

This activity gives beginners a concrete way to explore that question without distributing protected patient records. Participants examine repeated observations, explore one person’s trajectory, turn data modalities on and off, compare models, and discuss whether the result would be useful or responsible in nursing research or practice.

[Open the interactive notebook in Google Colab](https://colab.research.google.com/github/sonya-j/ninr-ai-bootcamp/blob/main/notebooks/02_multimodal_symptom_trajectories.ipynb)

## Dataset decision

### Real-world research destination: NIH All of Us

The **NIH All of Us Research Program** is the best fit for the full research question because its individual-level research tiers include:

- participant-provided survey information;
- longitudinal EHR conditions, visits, procedures, drugs, and measurements organized with the OMOP Common Data Model;
- Fitbit activity, sleep, and heart-rate tables;
- demographic, calendar, survey, and privacy-appropriate geographic context.

The activity targets **Registered Tier CDR v9**, release `R2025Q4R6` dated June 26, 2026, with a January 1, 2025 data cutoff. Researchers must register, complete required training, agree to the data-use code, and analyze individual-level records inside the secure Researcher Workbench.

Official references:

- [All of Us data types and organization](https://support.researchallofus.org/hc/en-us/articles/4619151535508-Data-Types-and-Organization)
- [All of Us data methods](https://www.researchallofus.org/data-tools/methods/)
- [Current curated data dictionaries and releases](https://support.researchallofus.org/hc/en-us/articles/360033200232-Data-Dictionaries)
- [All of Us data access tiers](https://allofus.nih.gov/protecting-data-and-privacy/research-projects-all-us-data)

### Public workshop dataset: transparent synthetic cohort

Individual-level All of Us data cannot be redistributed through GitHub. The hands-on lab therefore uses a deterministic synthetic cohort containing:

- 240 synthetic participants;
- 34 prediction days per participant;
- 8,160 participant-day observations;
- 22 documented variables;
- four predictor modalities and a next-day symptom outcome.

The teaching data are not an All of Us extract, sample, or statistical reconstruction. They contain no real participant records and are not intended to reproduce the distribution of any protected dataset. Their purpose is to make the analytic structure, modeling choices, and responsible-AI issues visible.

Artifacts:

- [participant-day CSV](../data/processed/multimodal_symptom_trajectories/participant_day.csv)
- [machine-readable data dictionary](../metadata/multimodal_symptom_trajectories/data_dictionary.csv)
- [missingness report](../metadata/multimodal_symptom_trajectories/missing_values.csv)
- [risk flags](../metadata/multimodal_symptom_trajectories/risk_flags.csv)
- [provenance](../metadata/multimodal_symptom_trajectories/provenance.json)
- [validation report](../metadata/multimodal_symptom_trajectories/validation_report.json)
- [reproducible generator](../activities/multimodal_symptom_trajectories/generate_teaching_data.py)

## Modality map

| Modality | Teaching variables | Authorized All of Us analogue |
|---|---|---|
| Patient-reported | pain, fatigue, mood, sleep quality, current symptom score | Participant-provided information and selected survey concepts |
| Wearable | steps, active minutes, resting heart rate, sleep minutes | Fitbit activity, heart-rate, and sleep tables |
| EHR | chronic-condition count, medication count, recent encounter, medication change, care message | OMOP condition, drug, visit, measurement, and related EHR domains |
| Context | age group, weekend, temperature, air quality, social support, study day | Survey/demographic context and privacy-permitted temporal or geographic linkage |
| Outcome | next-day composite symptom score | A prespecified, validated symptom concept selected for the authorized study |

The synthetic composite symptom score is a teaching construct, not a validated patient-reported outcome. An applied project must select an official survey concept or validated clinical outcome and document its scoring.

## Suggested 75-minute facilitation plan

| Time | Activity | Teaching emphasis |
|---:|---|---|
| 10 min | Frame the question and inspect the four modalities | Unit of observation, modality, trajectory |
| 10 min | Explore one synthetic participant | Within-person change and missingness |
| 10 min | Define the next-day prediction task | Prediction time, outcome, leakage |
| 20 min | Turn modalities on and off | Baseline comparison and incremental value |
| 10 min | Compare age-group error | Subgroup evaluation without causal overclaiming |
| 15 min | Team discussion | Burden, equity, actionability, validation, governance |

## Expected learning pattern

Because the generator intentionally makes tomorrow’s symptom level autocorrelated with today’s symptoms, patient-reported data will often be highly predictive. Wearable, EHR-like, and contextual variables provide smaller complementary signals. Participants should not be graded on obtaining a particular MAE. The learning goal is to explain why performance changes and whether the added data burden is justified.

## Responsible-AI guardrails

- Split by participant, not by row, so one person does not appear in both training and test data.
- Define exactly when prediction occurs and exclude information recorded after that time.
- Treat wearable non-wear and missed surveys as potentially informative missingness.
- Compare performance across relevant groups, but do not interpret subgroup error as a biological difference without evidence.
- Consider who lacks compatible devices, reliable connectivity, portal access, or time for repeated surveys.
- Do not treat a lower test error in synthetic data as evidence of clinical benefit.
- Specify the nursing decision or intervention that a prediction would support before proposing deployment.
- Keep authorized All of Us data and outputs inside the environments and disclosure rules required by the program.

## Reproduce the teaching data

```bash
python activities/multimodal_symptom_trajectories/generate_teaching_data.py
python -m unittest discover -s tests -v
```

The fixed seed, equations, missingness rates, output hash, and software versions are recorded in the generator and provenance file.
