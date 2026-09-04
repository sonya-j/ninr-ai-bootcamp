# Day 1 Data Dictionary

These are the variables emphasized in the beginner notebook. Names follow the UCI dataset.

| Variable | What it represents | Type | Why we use it on Day 1 |
|---|---|---|---|
| `encounter_id` | Unique hospital encounter identifier | ID | Practice inspecting identifiers |
| `race` | Recorded race category | Categorical | Grouping/counts and discussion of context |
| `gender` | Recorded gender | Categorical | Grouping/counts |
| `age` | Age group (10-year categories) | Categorical | Basic distribution |
| `time_in_hospital` | Days in hospital | Integer | Summary statistics and visualization |
| `num_lab_procedures` | Number of laboratory procedures during encounter | Integer | Distribution |
| `num_procedures` | Number of non-laboratory procedures | Integer | Distribution/comparison |
| `num_medications` | Number of medications administered | Integer | Distribution/comparison |
| `number_outpatient` | Outpatient visits in prior year | Integer | Healthcare utilization |
| `number_emergency` | Emergency visits in prior year | Integer | Healthcare utilization |
| `number_inpatient` | Inpatient visits in prior year | Integer | Healthcare utilization |
| `A1Cresult` | HbA1c test result category | Categorical | Missingness and simple counts |
| `diabetesMed` | Whether diabetes medication was prescribed | Categorical | Counts/grouping |
| `readmitted` | Readmission category (<30 days, >30 days, or no record) | Outcome/categorical | End-of-day exploratory question |

**Important:** The `readmitted` field is used on Day 1 only for simple description/group comparison. No predictive modeling is performed.
