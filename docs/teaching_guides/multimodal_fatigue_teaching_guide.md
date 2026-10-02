# Teaching Guide: Multimodal Prediction of Next-Day Fatigue

## Purpose

This activity helps beginning learners translate an ambitious multimodal-AI question into a defensible prediction task. It emphasizes longitudinal thinking, modality auditing, baselines, participant-level splitting, missingness, and limits on claims.

The instructional goal is **not** to produce a clinically useful fatigue model. It is to help learners recognize what a prediction is, how it is evaluated, and what a dataset can and cannot answer.

Assume participants do not know what a feature, target, model, train/test split, baseline, or error metric is. Introduce each idea only when learners need it. The notebook and participant walkthrough use a repeated rhythm:

1. **Learn** one plain-language idea.
2. **Do** one action.
3. **Notice** one result.
4. **Explain** it in the learner's own words.

## Core path and level-up path

The **core path** is appropriate for all participants:

- make a prediction manually;
- identify inputs and outcome;
- explore a trajectory and missingness;
- understand training versus testing;
- establish the no-ML rule;
- compare modality groups using ridge regression;
- interpret MAE and write a calibrated conclusion.

The **level-up path** is optional:

- compare ridge regression with random forest;
- discuss model flexibility and overfitting;
- examine participant-level error in more depth;
- propose time-window, high-fatigue, or person-specific extensions.

Do not let the optional algorithm comparison crowd out the core concepts.

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

### Recommended room setup

- Ask participants to work individually for the manual prediction and final evidence statement.
- Use pairs for the training/test explanation and EHR extension.
- Keep the participant walkthrough open in a second tab.
- Tell participants explicitly: “You are not expected to read, edit, or understand the Python code.”
- Demonstrate how to run a cell, use a dropdown, and recover with **Runtime → Run all**.

## Suggested 75-minute lesson

| Time | Segment | Instructor action | Learner product |
|---:|---|---|---|
| 0–8 min | Prediction without jargon | Learners make one manual prediction | Prediction and absolute error |
| 8–17 min | Vocabulary and task | Define input, outcome, model, and trajectory | Precise prediction statement |
| 17–27 min | Audit modalities | Sort available and absent sources | Completed modality audit |
| 27–38 min | Explore trajectories | Demonstrate the participant selector | “I notice / I wonder” pair |
| 38–47 min | Missingness | Separate zero from missing and discuss non-wear | Missingness hypothesis |
| 47–56 min | Training, testing, baseline | Use practice/exam analogy and no-ML rule | One-sentence leakage explanation |
| 56–67 min | Compare inputs | Keep ridge regression fixed; change modality groups | MAE comparison table |
| 67–75 min | Conclude and extend | Write evidence statement; name an EHR extension | Calibrated conclusion |

If you have 90 minutes, add the random-forest level-up and participant-level error discussion.

## Facilitation script

### Opening prompt

“Imagine a nurse wants an alert before a patient's fatigue worsens tomorrow. What information would be available by the end of today, and what would only become known tomorrow?”

Use responses to establish the prediction cutoff. Information recorded after the cutoff is unavailable at prediction time, even if it exists in the final dataset.

Before defining ML, have learners use the notebook's prediction game. Ask, “What rule did you use?” Then explain that an ML algorithm also develops a rule from earlier examples, although its rule is mathematical and learned systematically.

### Explain AI without anthropomorphism

Suggested wording:

> “The model does not understand fatigue. It estimates a number from patterns in examples. We evaluate the number, not the model's intentions or reasoning.”

Avoid phrases such as “the AI knows,” “the model thinks,” or “the model decides the patient is fatigued.”

### Modality audit

Ask groups to place each variable into one of five bins: patient report, wearable, context, EHR, or outcome. When learners reach the empty EHR bin, emphasize:

> Missing a modality changes the question. It does not justify creating a proxy and calling it EHR.

### Baseline discussion

Today's fatigue is a strong baseline because symptoms often persist. If a complex multimodal model cannot improve on that baseline, its extra burden may not be justified. A model should also be compared on unseen people, not only unseen rows.

Make clear that the baseline is a **rule, not ML**: tomorrow equals today. Learners should record its MAE before viewing ML results.

### Explain MAE with a worked example

Write three errors where everyone can see them:

```text
errors: 1 point, 1 point, 0 points
MAE = (1 + 1 + 0) / 3 = 0.67 fatigue points
```

Ask learners to interpret the unit. MAE is expressed in fatigue-scale points, not a percentage.

### Result discussion

Do not promise a specific winning feature set. Results may change slightly with software versions, and this small dataset has heterogeneous follow-up. Grade the reasoning, not whether learners obtain the lowest MAE.

## Checkpoint answer key

| Checkpoint | Essential idea |
|---|---|
| Why can tomorrow's fatigue not be an input? | It is not available at the end-of-today prediction time; using it is future-information leakage. |
| Does one correct manual prediction prove the rule works? | No. It may be luck; performance must be checked across separate examples. |
| Is missing steps the same as zero steps? | No. Zero is observed; missing is unavailable and may reflect non-wear or failure. |
| Why split by participant? | Days from the same person are correlated; a row split would create an easier and potentially misleading test. |
| Why use a baseline? | It shows whether added complexity and data collection improve on a simple reasonable rule. |
| Does lower MAE show causation? | No. Predictive association does not establish why fatigue changes. |
| Can this activity test EHR value? | No. The source contains no EHR data. |
| Does the best test MAE justify clinical use? | No. Clinical use requires representative validation, workflow fit, actionability, safety, and prospective evaluation. |

## Questions participants may ask

### “Is this really AI?”

Ridge regression and random forests are machine-learning methods commonly placed under the broad AI umbrella. The educational point is the prediction workflow, not whether a method sounds futuristic.

### “Why not use a neural network or generative AI?”

The sample is small, and the learning goal is interpretation. A more complicated method would add cognitive and statistical complexity without guaranteeing better generalization.

### “Why are there only 28 people?”

This was a pilot study. Repeated days provide many rows, but rows are not independent people. The small number of participants is a major limitation.

### “Which input caused fatigue?”

This activity evaluates prediction, not causation. Feature associations may reflect confounding, measurement differences, or chance.

### “Why is EHR missing if the workshop question includes it?”

Open longitudinal datasets containing all four modalities are rare. The absence is part of the lesson: research questions must be narrowed to match available data, and a full linked-data study requires additional access and governance.

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
