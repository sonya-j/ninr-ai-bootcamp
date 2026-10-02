# Activity Walkthrough: Predict Tomorrow's Fatigue

## What you will investigate

You will use real, openly available longitudinal data to answer:

> Can today's patient-reported fatigue, wearable signals, and time context predict tomorrow's fatigue rating?

This is one testable part of the broader question about combining patient reports, wearables, EHRs, and context. The dataset does not contain EHR data, so you will not make claims about EHR contribution.

**Time:** 60–75 minutes  
**Experience needed:** None beyond running notebook cells  
**Tool:** Google Colab in a web browser

## Before you begin

Open the [interactive notebook in Google Colab](https://colab.research.google.com/github/sonya-j/ninr-ai-bootcamp/blob/main/notebooks/02_multimodal_symptom_trajectories.ipynb), then select **Runtime → Run all**. If Colab asks whether you trust the notebook, choose **Run anyway**; the notebook reads the activity CSV from this public repository and does not request credentials.

Work through the numbered sections below. Record brief answers in your own notes or in the notebook's reflection cells.

## 1. Translate the broad question into a prediction task

A useful prediction question specifies four things:

| Element | Definition in this activity |
|---|---|
| Unit | One participant-day |
| Prediction time | End of the current day |
| Inputs | Information available on the current day |
| Outcome | The participant's 1–10 fatigue rating on the next calendar day |

**Checkpoint:** Why would a same-day fatigue outcome be less useful for testing a future prediction?

## 2. Audit the modalities

In the notebook, inspect the modality table and data dictionary.

- Patient-reported variables describe how the participant felt or what they reported doing.
- Wearable variables summarize one-minute sensor measurements over the day.
- Time context describes when the observation occurred.
- EHR variables are absent.

**Checkpoint:** Write one variable you expected but did not find. Would it be a patient report, wearable measure, EHR field, or contextual measure?

## 3. Explore one person's trajectory

Use the participant selector. The plot shows today's fatigue, tomorrow's fatigue target, and daily heart rate on aligned dates.

Look for periods when fatigue changes, gaps in reports or sensors, whether heart rate appears to move with fatigue, and how many consecutive next-day outcomes are available.

**Checkpoint:** Does a visible association in one participant establish that the wearable predicts fatigue? Why or why not?

## 4. Understand missingness

Review the missingness plot. A blank sensor value can mean sensor failure, non-wear, a device limitation, or a processing issue. A blank next-day outcome usually means the participant did not report on the immediately following calendar day.

**Checkpoint:** Could non-wear itself be related to fatigue? If so, what bias might simple deletion introduce?

## 5. Split by participant

The notebook keeps each participant entirely in either training or testing data. It does not randomly split participant-days. Measurements from the same person tend to resemble each other. If one person's days appeared in both sets, the model could partly recognize that person and produce an overly optimistic result.

**Checkpoint:** In one sentence, explain why the test participants are a stronger challenge than randomly held-out rows.

## 6. Compare meaningful baselines

The notebook compares four feature sets:

1. **Today's fatigue only** — a persistence baseline.
2. **Wearable only** — sensor summaries without today's self-report.
3. **Patient report + wearable** — combines subjective and objective measures.
4. **All available** — adds time context; still no EHR.

Use mean absolute error (MAE): the average absolute difference between predicted and observed fatigue points. Lower is better. Also inspect the observed-versus-predicted plot rather than relying only on one number.

**Checkpoint:** Does the multimodal model beat today's-fatigue-only baseline? If yes, is the difference large enough to justify the added collection burden?

## 7. Change the model

Use the model selector to compare ridge regression with a random forest. Ridge regression is a relatively simple linear model. A random forest can represent nonlinear relationships but may overfit a small dataset.

**Checkpoint:** Did the more flexible model help on unseen participants? Why might a complex model perform worse here?

## 8. Interpret participant-level error

Inspect errors by test participant. Large differences can indicate heterogeneity, sparse observations, missingness, or a model that fits some people better than others. With only a few test participants, this is a diagnostic—not a fairness conclusion.

**Checkpoint:** Which participant has the largest MAE? What should you investigate before attributing the difference to the person?

## 9. Answer the question at the right level

Complete this sentence:

> In this small sample of healthy adults, a model using __________ had an MAE of __________ for next-day fatigue among held-out participants. Compared with the today's-fatigue baseline, performance was __________. This does not establish __________.

Good final statements distinguish what the activity measured, what the result suggests, what the data cannot test, and what evidence would be needed before clinical use.

## 10. Design the EHR extension

Choose one possible EHR contribution—such as diagnoses, medication changes, laboratory results, recent encounters, or treatment exposure. Then specify:

1. why it might predict tomorrow's fatigue;
2. when it must be recorded to avoid future-information leakage;
3. how it would be harmonized with the daily timeline;
4. whose records might be missing or incomplete;
5. what nursing action a prediction could support.

## Optional extensions

- Predict a binary high-fatigue outcome instead of the 1–10 score.
- Use the previous three days rather than only the current day.
- Require a minimum number of wearable minutes and examine the tradeoff.
- Compare global models with person-specific baselines.
- Add uncertainty intervals or calibration checks.

## Source and citation

De Luca V, Luo H, and Clay I. *Continuous multi-sensor wearable data and daily subject-reported fatigue of healthy adults*, version 1. Zenodo, 2020. [https://doi.org/10.5281/zenodo.4266157](https://doi.org/10.5281/zenodo.4266157)

The associated study is available from [PubMed Central](https://pmc.ncbi.nlm.nih.gov/articles/PMC7768149/).
