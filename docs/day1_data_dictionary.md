# Day 1 data dictionary

The notebooks use an introductory selection from the validated participant file. Definitions below are abbreviated from the official UCI metadata; the authoritative machine-readable dictionary for all raw, selected, and derived variables is in `metadata/data_dictionary.csv` and `metadata/data_dictionary.json`.

| Variable | Official meaning | Type |
|---|---|---|
| `encounter_id` | Unique encounter identifier | ID |
| `race` | Recorded race category | Categorical |
| `gender` | Recorded gender category | Categorical |
| `age` | Age grouped in 10-year intervals | Categorical |
| `time_in_hospital` | Integer days between admission and discharge | Integer |
| `num_lab_procedures` | Laboratory tests performed during the encounter | Integer |
| `num_procedures` | Non-laboratory procedures performed during the encounter | Integer |
| `num_medications` | Distinct generic medication names administered during the encounter | Integer |
| `number_outpatient` | Outpatient visits in the year preceding the encounter | Integer |
| `number_emergency` | Emergency visits in the year preceding the encounter | Integer |
| `number_inpatient` | Inpatient visits in the year preceding the encounter | Integer |
| `A1Cresult` | HbA1c result category; `None` means not measured | Categorical |
| `diabetesMed` | Whether a diabetes medication was prescribed | Categorical |
| `readmitted` | `<30`, `>30`, or `NO` recorded inpatient readmission | Outcome |

`readmitted` is used for description and group comparison in the introductory notebook. It must not be used as a predictor of the derived `readmitted_30d` outcome.
