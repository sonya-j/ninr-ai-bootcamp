# Participant Walkthrough: Can AI Predict Tomorrow's Fatigue?

## Welcome

This activity is for people with **no previous AI, machine-learning, or coding experience**. You will not write code. You will run prepared steps, use menus and sliders, study the results, and make a careful scientific interpretation.

You will learn how a basic prediction study works by answering:

> Can information available today—patient-reported fatigue, wearable signals, and time context—help predict tomorrow's fatigue rating?

This is a learning activity, not a clinical tool. The dataset contains healthy adults and does not contain EHR data.

- **Time:** approximately 75 minutes
- **What you need:** a web browser and internet connection
- **What you will produce:** a short evidence statement and a plan for an EHR extension

## Your learning path

- [ ] Understand the question and key vocabulary
- [ ] Make a prediction yourself
- [ ] Identify the available data modalities
- [ ] Explore one person's trajectory
- [ ] Investigate missing data
- [ ] Understand training and testing
- [ ] Compare a simple rule with ML
- [ ] Interpret error without overclaiming
- [ ] Design a responsible EHR extension

## Before you open the notebook

### What do “AI” and “machine learning” mean here?

**Artificial intelligence (AI)** is a broad label for computer systems that perform tasks such as recognizing patterns or making predictions.

**Machine learning (ML)** is one way to build an AI system. Instead of programming every decision rule, we give an algorithm earlier examples. The algorithm estimates a pattern connecting the available information to the outcome.

In this activity:

```text
information available today → learned pattern → predicted fatigue tomorrow
```

The model does not understand fatigue, know why someone is tired, or decide what a nurse should do. It calculates a prediction from patterns in data.

### Essential vocabulary

| Term | Plain-language meaning | Activity example |
|---|---|---|
| Participant-day | One person observed on one day | Participant 24 on study day 12 |
| Trajectory | How something changes over time | Fatigue ratings across several days |
| Input or feature | Information available when predicting | Today's fatigue or mean heart rate |
| Outcome or target | What we want to predict | Tomorrow's fatigue rating |
| Model | The pattern learned from earlier examples | A ridge-regression model |
| Training data | Examples used to learn the pattern | Days from the training participants |
| Test data | Separate examples used for an honest exam | Days from participants not used in learning |
| Baseline | A simple comparison rule | Predict that tomorrow equals today |
| Error | Distance between prediction and observation | Predicted 4, observed 6: error is 2 |
| Modality | A type or source of data | Patient report or wearable sensor |
| Leakage | Accidentally giving the model information it would not truly have | Using tomorrow's value to predict tomorrow |

## Open the activity

1. Open the [interactive notebook in Google Colab](https://colab.research.google.com/github/sonya-j/ninr-ai-bootcamp/blob/main/notebooks/02_multimodal_symptom_trajectories.ipynb).
2. If Google displays a warning, select **Run anyway**. The notebook only reads public files from this repository.
3. Select **Runtime → Run all**.
4. Wait until the spinning indicator stops. You do not need to edit the code.
5. Begin at Step 1 in the notebook and move downward.

If a cell has not run, select the triangular play button on its left. A number or check mark appears when it finishes.

## Step 1 · Turn the broad idea into a precise task

The broad workshop question mentions patient reports, wearables, EHRs, and context. The public dataset has only three of those sources. Our answerable question is therefore narrower.

| Question part | Definition |
|---|---|
| Who? | Healthy adults in the public pilot dataset |
| Unit | One participant-day |
| Prediction time | End of the current day |
| Available inputs | Today's reports, today's wearable summaries, and time context |
| Outcome | Fatigue reported on the next calendar day |

### Stop and write

Why is “tomorrow's fatigue” not allowed as an input?

<details><summary>Suggested answer</summary>It is not known at the end of today. Using it would leak future information into the prediction.</details>

## Step 2 · Make a prediction before using ML

Find **Make a prediction yourself** in the notebook.

1. Choose Example 1.
2. Read the information available today.
3. Move the slider to your best guess for tomorrow's fatigue.
4. Select **Reveal tomorrow**.
5. Record your absolute error.
6. Repeat for at least three examples.

| Example | Your prediction | Observed tomorrow | Absolute error |
|---:|---:|---:|---:|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |

To calculate absolute error, ignore whether the prediction was too high or too low:

```text
absolute error = |observed value − predicted value|
```

Example: predicted 4, observed 6, so the absolute error is 2 fatigue points.

### Stop and write

What informal rule did you use? Did you rely mostly on today's fatigue, heart rate, steps, or intuition?

## Step 3 · Audit the data modalities

The notebook displays five rows. Read them before modeling.

- **Patient-reported:** what participants said about fatigue, exhaustion, and sport.
- **Wearable:** measurements such as heart rate, activity, respiration, and skin temperature.
- **Time context:** study day, day of week, and weekend.
- **EHR:** absent. There are no diagnoses, medications, encounters, laboratory results, or clinical notes.
- **Outcome:** next-day fatigue.

### Stop and write

Name one EHR variable you might want. Do not substitute a wearable variable and call it EHR.

## Step 4 · Explore a trajectory

Find the participant menu and plot.

1. Select the participant already shown.
2. Follow today's fatigue line from left to right.
3. Locate at least one increase, decrease, or stable period.
4. Look for gaps.
5. Compare the fatigue line with mean heart rate.
6. Repeat with one other participant.

### Record two observations

- I notice: ________________________________________________
- I wonder: _______________________________________________

An “I notice” statement describes the plot. An “I wonder” statement proposes a question. Neither establishes causation.

## Step 5 · Investigate missingness

The missingness chart shows the percentage of unavailable values in each variable.

1. Identify the variable with the most missingness.
2. Decide whether a blank could mean non-wear, a missed report, technical failure, or something else.
3. Ask whether fatigue itself could make missingness more likely.

### Knowledge check

If a participant has no step value, should it automatically be changed to zero?

<details><summary>Suggested answer</summary>No. Zero means the device measured no steps. Missing means the value was not available, which can happen for several reasons.</details>

## Step 6 · Understand training and testing

The algorithm learns from the **training participants**. It is evaluated on different **test participants**.

Think of this as practice and an exam:

```text
training participants → algorithm learns a pattern
test participants     → pattern takes an honest exam
```

All days from one person stay together. Otherwise, the algorithm could see some days from a person during training and appear unusually accurate on that same person's test days.

### Stop and explain to a partner—or write one sentence

Why is testing on new participants more difficult and more informative?

## Step 7 · Establish the no-ML baseline

Before asking whether ML helps, use this simple rule:

> Predict that tomorrow's fatigue will be the same as today's fatigue.

This rule is reasonable because symptoms often persist. It also requires only one input and no learned algorithm.

In the notebook, choose **No-ML rule: tomorrow = today**. Record its mean absolute error (MAE):

**Baseline MAE:** __________ fatigue points

MAE is the average absolute error across test observations. Lower is better.

## Step 8 · Compare inputs using one ML method

Keep the model set to **Ridge regression**. You do not need to understand its equation. For this activity, think of it as a method that learns a weighted combination of the inputs.

Try each option and record the test MAE:

| Inputs | MAE | Better than baseline? |
|---|---:|---|
| No-ML rule |  | — |
| Wearable only |  |  |
| Patient reports only |  |  |
| Patient reports + wearable |  |  |
| All available, without EHR |  |  |

### Interpret the comparison

- Lower MAE means predictions were closer on average.
- A small improvement may not justify more devices, missing data, cost, or participant burden.
- More inputs do not guarantee a better model.
- This comparison cannot tell us whether EHR data would help because EHR data are absent.

## Step 9 · Read the prediction plot

In the observed-versus-predicted plot:

- the horizontal axis is what participants actually reported;
- the vertical axis is what the approach predicted;
- the diagonal line represents perfect predictions;
- points far from the line have larger errors.

### Stop and write

Does the model tend to miss more at very low or very high fatigue levels? What might that mean for someone using an alert?

## Step 10 · Look beyond one average

The participant-level error plot shows whether the approach works similarly for every test participant.

1. Identify the participant with the largest MAE.
2. Check how many observations that participant contributes.
3. Consider missingness and individual differences before drawing conclusions.

A difference between a few participants is not automatically evidence of unfairness. It is a signal to investigate with a larger and more representative dataset.

## Step 11 · Optional level-up: change the algorithm

After completing the core activity, switch from **Ridge regression** to **Random forest**.

A random forest combines many decision trees and can learn more complicated patterns. Complicated does not automatically mean better. With a small dataset, a flexible algorithm can learn quirks that do not generalize.

### Stop and write

Did random forest improve test MAE? Why is “more advanced” not the same as “more useful”?

## Step 12 · Write the evidence statement

Complete this template:

> In this small sample of healthy adults, the __________ approach used __________ and had a test MAE of __________ fatigue points among participants not used for training. Compared with the no-ML rule, its MAE was __________. These results suggest __________, but they do not establish __________.

Your statement should include:

- the population;
- the inputs;
- the test metric;
- the baseline comparison;
- at least one limitation.

Avoid claims about clinical readiness, causation, patients with illness, or EHR value.

## Step 13 · Design the EHR extension

Choose one actual EHR field: a diagnosis, medication, medication change, laboratory result, recent encounter, or treatment exposure.

Complete the plan:

| Design question | Your answer |
|---|---|
| What EHR field would you add? |  |
| Why might it predict tomorrow's fatigue? |  |
| When must it be recorded to be available today? |  |
| How would you align it with participant-days? |  |
| Whose EHR information might be incomplete? |  |
| What nursing action could the prediction support? |  |

## Final check

You should now be able to explain:

- what the model predicts;
- what information it uses;
- how training differs from testing;
- why a baseline matters;
- what MAE means;
- why missingness matters;
- why this dataset cannot answer the EHR part of the broad question;
- why a predictive result alone is not enough for clinical use.

## Source and citation

De Luca V, Luo H, and Clay I. *Continuous multi-sensor wearable data and daily subject-reported fatigue of healthy adults*, version 1. Zenodo, 2020. [https://doi.org/10.5281/zenodo.4266157](https://doi.org/10.5281/zenodo.4266157)

The associated study is available from [PubMed Central](https://pmc.ncbi.nlm.nih.gov/articles/PMC7768149/).
