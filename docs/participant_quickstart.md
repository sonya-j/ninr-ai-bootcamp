# Participant Quick Start

Welcome to the data workspace for the **NINR Artificial Intelligence Summer Research Intensive**. This guide is designed for researchers with strong subject-matter or statistical experience and any level of Python experience—including none.

## Choose your route

### Route A · Follow the guided Day 1 lab

Use this route if you are new to Python, Google Colab, or health-data coding.

1. Download or open [`01_day1_python_and_clinical_data.ipynb`](../notebooks/01_day1_python_and_clinical_data.ipynb).
2. Open the notebook in [Google Colab](https://colab.research.google.com/).
3. Upload [`diabetes_130_hospitals_participant.csv`](../data/processed/diabetes_130_hospitals_participant.csv) when the notebook asks for it.
4. Run one cell at a time. Read the output before moving on.

**You will practice:** loading a dataset, viewing a table, checking variable types and missingness, calculating descriptive statistics, and making a simple plot.

### Route B · Explore a research question

Use this route if you are ready to compare datasets or begin a team project.

1. Open the [Dataset Explorer](dataset_catalog.md).
2. Start with a research area or workshop activity—not with an algorithm.
3. Read the dataset’s “why choose it,” official outcome, and research questions.
4. Open its `participant.csv`, `data dictionary`, and `risk flags` together.
5. Write down the outcome, candidate predictors, unit of observation, prediction time, and one important limitation before analyzing.

### Route C · Try multimodal AI

Use this route after the Day 1 lab to explore real repeated fatigue reports, wearable measures, and time context. The activity also shows why EHR data cannot be evaluated when the selected public dataset does not contain them.

1. Open [Activity 2: Multimodal Fatigue Trajectories](multimodal_symptom_trajectory_activity.md).
2. Follow the [participant activity walkthrough](activities/multimodal_fatigue_walkthrough.md).
3. Launch the notebook in Google Colab and inspect a real participant trajectory.
4. Compare today's-fatigue, wearable-only, combined, and context-enhanced models.
5. Discuss data burden, missingness, participant-level error, and what a responsible EHR extension would require.

## What each file tells you

| File | Use it to answer… |
|---|---|
| `participant.csv` | What data will I analyze? |
| `data_dictionary.csv` | What does each variable mean? |
| `value_labels.csv` | What do coded categories mean? |
| `missing_values.csv` | Which values mean missing or unavailable? |
| `risk_flags.csv` | Which variables may leak the outcome, act as proxies, or occur too late? |
| `provenance.json` | Where did the data come from, and how were they transformed? |
| `validation_report.json` | Did the automated quality checks pass? |

## A five-minute dataset check

Before building a model, complete these five sentences:

1. **My unit of observation is** …
2. **My outcome is measured as** …
3. **My predictors would be available at** …
4. **The population represented is** …
5. **A result could be misleading if** …

If any answer is unclear, pause and use the official source, data dictionary, and provenance file. Do not infer a variable meaning from its name alone.

## Load any participant CSV in Colab

```python
import pandas as pd

path = "participant.csv"
data = pd.read_csv(path, keep_default_na=False, na_values=[""])

print(data.shape)
display(data.head())
```

Using `keep_default_na=False` protects legitimate text labels such as the word `NULL`; blank fields are still treated as missing.

## Responsible-analysis checklist

- **Timing:** Were all predictors available before the outcome or decision?
- **Leakage:** Does a variable directly contain, determine, or summarize the target?
- **Repeated measures:** Are multiple rows from the same participant split across training and test data?
- **Representation:** Who is missing or underrepresented in the source sample?
- **Proxy discrimination:** Could geography, income, race, sex, or related fields encode structural inequities?
- **Subgroup performance:** Does the model perform differently across clinically or socially important groups?
- **Transportability:** Would the dataset’s place, time period, and care context match the intended use?
- **Interpretation:** Are you describing association, prediction, or causation—and is that claim supported?

## If something does not work

- Confirm that the uploaded filename matches the name used in the notebook.
- Run notebook cells from the top in order.
- Use **Runtime → Restart session** in Colab if variables are in an inconsistent state.
- Check the relevant `validation_report.json` before assuming the source file is broken.
- Ask what the error message says and which cell produced it; that is useful debugging information.

## Next step

Return to the [Dataset Explorer](dataset_catalog.md) and choose one question you would genuinely want to investigate. A specific, well-timed research question is more important than a complicated model.
