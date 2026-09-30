# Research questions and analytic cautions

These questions are possible teaching starting points, not prespecified causal analyses. Variable definitions come from the official UCI metadata and the original Strack et al. article; the cautions below are analytic judgments.

## Possible research questions

1. How does early readmission (less than 30 days) vary by prior-year inpatient, emergency, and outpatient utilization?
2. Is inpatient HbA1c testing/result category associated with early readmission, and how does that association change after describing age, admission type, diagnosis burden, and prior utilization?
3. Are there differences in early readmission by recorded race, gender, or age group, and do missingness and subgroup sample size affect those comparisons?
4. Is a change in diabetes medication during the encounter associated with early readmission, recognizing that treatment decisions may reflect illness severity and other clinical factors?
5. How do length of stay and encounter-level care intensity (laboratory procedures, non-laboratory procedures, and number of medications) differ across readmission categories?

## Timing, leakage, and confounding

- `encounter_id` and the excluded `patient_nbr` are identifiers, not predictors. Repeated patients can leak across model splits if `patient_nbr` is ignored in the full source data.
- `readmitted` and `readmitted_30d` are outcomes. Including either as a predictor of the other is direct target leakage.
- `discharge_disposition`, `time_in_hospital`, procedure counts, medication counts, laboratory results, insulin status, medication change, and diabetes-medication prescription are known or completed during/by the end of the encounter. They are unavailable for an admission-time prediction question.
- Treatment and testing variables can be confounded by indication, severity, clinician practice, and access to care. Their associations should not be interpreted as treatment effects without a suitable causal design.
- Race, gender, and age are sensitive or potentially proxying variables. Report subgroup sample sizes, missingness, and performance; do not treat observed disparities as biological effects.
- The official source supplies no survey or analytic weights. This convenience clinical database is not documented as a probability sample, so estimates should not be presented as nationally representative.

The machine-readable version of these flags is `metadata/risk_flags.csv` and is also included in the data dictionary.
