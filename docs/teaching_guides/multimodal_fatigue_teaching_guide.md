# Teaching Guide: Multimodal Prediction of Next-Day Fatigue

## Purpose

This activity helps beginning learners translate an ambitious multimodal-AI question into a defensible prediction task. It emphasizes longitudinal thinking, modality auditing, baselines, participant-level splitting, missingness, and limits on claims.

The instructional goal is **not** to produce a clinically useful fatigue model. It is to help learners recognize what a dataset can and cannot answer.

## Learning objectives

By the end, participants should be able to:

1. define the unit, prediction time, inputs, and outcome for a longitudinal prediction task;
2. distinguish patient-reported, wearable, contextual, and EHR data;
3. explain why rows from one participant must not cross the train/test boundary;
4. compare a multimodal model with a clinically meaningful simple baseline;
5. identify leakage, missingness, selection, and generalizability risks;
6. state conclusions that match the available evidence;
7. propose a responsible EHR extension without pretending EHR data are present.

## Dataset facts to state accurately

- Source: [Zenodo record 4266157](https://doi.org/10.5281/zenodo.4266157), published by the original investigators.
- Version: v1, released November 10, 2020.
- License: CC BY 4.0.
- Population: healthy adults, not a clinical fatigue cohort.
- Original collection: 28 participants and 973 recording days.
- Article's matched analysis: 27 participants and 405 recording days.
- Repository preparation: 450 matched participant-days; 336 have an immediately following daily fatigue outcome.
- Modalities available: daily patient reports, one-minute wearable sensor measurements, and derived time context.
- Modality absent: EHR.

Do not describe the wearable fields as EHR data, and do not describe the sample as patients. “Patient-reported outcome” is a measurement category used by the source study; the participants in this dataset were healthy adults.

## Preparation

Before the session:

1. Open the [Colab notebook](https://colab.research.google.com/github/sonya-j/ninr-ai-bootcamp/blob/main/notebooks/02_multimodal_symptom_trajectories.ipynb).
2. Select **Runtime → Run all** and confirm every cell finishes.
3. Review the [participant walkthrough](../activities/multimodal_fatigue_walkthrough.md).
4. Decide whether learners will work individually, in pairs, or in groups of three.
5. Prepare a shared space for each group to record its final evidence statement and EHR extension.

No accounts or credentials are required beyond access to Google Colab. A local Jupyter environment also works after installing the repository requirements.

## Suggested 75-minute lesson

| Time | Segment | Instructor action | Learner product |
|---:|---|---|---|
| 0–8 min | Frame the north-star question | Ask what “trajectory” and “multimodal” mean | Initial modality list |
| 8–15 min | Scope the public data | Reveal that EHR is absent; narrow the question | Testable prediction statement |
| 15–27 min | Explore trajectories | Demonstrate the participant selector | One observation and one caveat |
| 27–37 min | Missingness and time | Discuss non-wear and consecutive-day outcomes | Missingness hypothesis |
| 37–48 min | Split and baseline | Contrast participant split with row split | Leakage explanation |
| 48–60 min | Compare models/modalities | Have groups report MAE and plots | Evidence table |
| 60–68 min | Error and equity | Inspect participant-level errors | One follow-up check |
| 68–75 min | EHR extension and debrief | Ask groups to specify timing and actionability | Calibrated conclusion |

## Facilitation script

### Opening prompt

“Imagine a nurse wants an alert before a patient's fatigue worsens tomorrow. What information would be available by the end of today, and what would only become known tomorrow?”

Use responses to establish the prediction cutoff. Information recorded after the cutoff is unavailable at prediction time, even if it exists in the final dataset.

### Modality audit

Ask groups to place each variable into one of five bins: patient report, wearable, context, EHR, or outcome. When learners reach the empty EHR bin, emphasize:

> Missing a modality changes the question. It does not justify creating a proxy and calling it EHR.

### Baseline discussion

Today's fatigue is a strong baseline because symptoms often persist. If a complex multimodal model cannot improve on that baseline, its extra burden may not be justified. A model should also be compared on unseen people, not only unseen rows.

### Result discussion

Do not promise a specific winning feature set. Results may change slightly with software versions, and this small dataset has heterogeneous follow-up. Grade the reasoning, not whether learners obtain the lowest MAE.

## Key concepts and likely misconceptions

| Misconception | Response |
|---|---|
| “Wearable vital signs are EHR data.” | They are participant-generated sensor data. They could later be stored in an EHR, but this source did not extract them from one. |
| “More variables must improve the model.” | Additional variables can add noise, missingness, burden, and overfitting. Compare with a simple baseline. |
| “A random row split is fine because dates differ.” | Days from the same person remain correlated. Keep people entirely in one set for person-generalization. |
| “Low MAE proves clinical usefulness.” | Clinical usefulness also requires representative validation, uncertainty, workflow fit, actionability, safety, and prospective evaluation. |
| “Missing wearable values mean zero activity.” | Missingness may reflect non-wear or technical failure. Zero is a measured value; missing is not. |
| “The model predicts a disease symptom.” | This dataset measures non-pathological fatigue in healthy adults. |

## Assessment rubric

Score each item 0–2 for a 10-point quick assessment.

| Criterion | 0 | 1 | 2 |
|---|---|---|---|
| Prediction task | Undefined | Partly defined | Unit, cutoff, inputs, and outcome are explicit |
| Validation | Row split or unclear | Participant split named | Participant split explained correctly |
| Baseline | No comparison | Baseline reported | Baseline interpreted against data burden |
| Evidence statement | Overclaim | Some caveats | Population, metric, comparison, and limits all stated |
| EHR extension | Calls a proxy EHR | Names an EHR field | Adds timing, harmonization, missingness, and nursing action |

## Responsible-AI discussion prompts

- Who is excluded when a study requires continuous wearable use?
- Could fatigue increase non-wear or missed reporting?
- Would an alert burden patients or nurses if no effective response is available?
- How should a model communicate uncertainty?
- What performance differences would matter clinically rather than statistically?
- How might work schedules, caregiving, disability, device type, or skin tone affect measurements or missingness?

## EHR extension examples

Acceptable ideas include prior diagnoses, medication burden, recent medication changes, laboratory results available before the cutoff, recent encounters, and treatment exposure. Learners must specify the timestamp used. A medication ordered tomorrow cannot predict tomorrow's fatigue from today's vantage point.

For an advanced group, ask whether EHR availability is itself a proxy for access, utilization, or illness severity.

## Technical notes

- The notebook uses median/mode imputation inside each training pipeline.
- Categorical variables are one-hot encoded.
- Continuous variables are standardized for ridge regression.
- Test participants are selected with a fixed grouped split for reproducibility.
- MAE is the primary metric because it is interpretable in fatigue-scale points.
- The notebook retains an observed-versus-predicted plot and participant-level MAE so learners do not rely on one aggregate number.

## Reproduce the prepared data

```bash
python activities/multimodal_symptom_trajectories/prepare_public_fatigue_data.py
python -m unittest discover -s tests -v
```

The first command downloads every original CSV from Zenodo, verifies its published MD5 checksum, preserves it under gitignored `data/raw/`, and recreates the tracked participant-day file and metadata.

## Citation

De Luca V, Luo H, and Clay I. *Continuous multi-sensor wearable data and daily subject-reported fatigue of healthy adults*, version 1. Zenodo, 2020. [https://doi.org/10.5281/zenodo.4266157](https://doi.org/10.5281/zenodo.4266157)

Luo H, Lee P-A, Clay I, Jaggi M, De Luca V. Assessment of Fatigue Using Wearable Sensors: A Pilot Study. *Digital Biomarkers*. 2020;4(Suppl 1):59–72. [Open-access article](https://pmc.ncbi.nlm.nih.gov/articles/PMC7768149/)
