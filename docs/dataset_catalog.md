# Dataset Explorer

### Choose a workshop dataset by question, not by algorithm

> **20 documented options · 4 research pathways · official sources · participant-ready files**

This page helps NINR AI Summer Research Intensive participants move from an area of interest to a manageable dataset and research question. Definitions come from official government documentation or the original dataset record; no Kaggle or unofficial mirror is used. Versions were checked on 2026-10-01.

Participant files contain 714–5,000 observations and 10–30 source variables, plus `portfolio_row_id`. Four focused clinical or survey sources contain fewer than 1,000 records; those participant files retain every available observation rather than fabricating additional data.

[How to use the files](participant_quickstart.md) · [Return to the workshop home](../README.md)

## Good first choices

| If you want to practice… | Start with… | A question you could ask |
|---|---|---|
| Classification with a clear clinical outcome | [Diabetes readmission](#diabetes-readmission) | Which pre-admission utilization measures are associated with early readmission? |
| Regression with repeated observations | [Parkinson telemonitoring](#parkinsons-telemonitoring) | Which voice features track symptom severity? |
| Health behavior and a multiclass outcome | [Obesity and lifestyle](#obesity-lifestyle) | How are activity and eating patterns associated with obesity category? |
| Older-adult health and service use | [National Poll on Healthy Aging](#healthy-aging-poll) | Which health and sleep factors relate to doctor visits? |
| Pediatric assessment and clinical decisions | [Pediatric appendicitis](#pediatric-appendicitis) | Which early findings are associated with diagnosis or management? |
| A small, approachable workforce dataset | [Workplace absenteeism](#workplace-absenteeism) | Which work and health factors relate to absence duration? |
| Patient experience and nursing quality | [Hospital HCAHPS](#hospital-patient-experience) | How do nurse-communication ratings vary across hospitals? |

These are starting points, not rankings. Choose the dataset whose population, timing, and limitations best fit your question.

## Browse by research area

### Clinical care and outcomes

Hospital care, prognosis, complications, trials, and infectious disease.

| Dataset | Participant file | Outcome | Best for |
|---|---:|---|---|
| [Diabetes 130-US Hospitals for Years 1999-2008](#diabetes-readmission) | 5,000 × 30 | `readmitted` | Inpatient diabetes care, utilization, treatment, and 30-day readmission. |
| [SUPPORT2](#support2-serious-illness) | 5,000 × 30 | `hospdead`, `death`, `sfdm2` | Prognosis, mortality, physiology, function, and care decisions among seriously ill hospitalized adults. |
| [Myocardial infarction complications](#myocardial-infarction-complications) | 1,700 × 30 | 8 documented targets | Pre-admission history, acute measurements, treatment, and complications after myocardial infarction. |
| [AIDS Clinical Trials Group Study 175](#aids-clinical-trial-175) | 2,139 × 25 | `cid` | Randomized HIV treatment, immune markers, symptoms, and clinical progression. |
| [Hepatitis C Virus (HCV) for Egyptian patients](#hepatitis-c-treatment) | 1,385 × 29 | `Baselinehistological staging` | Symptoms, blood tests, viral RNA over time, and baseline liver histology among patients treated for HCV. |
| [Regensburg Pediatric Appendicitis](#pediatric-appendicitis) | 782 × 30 | `Management`, `Severity`, `Diagnosis` | Symptoms, physical examination, laboratory tests, ultrasound findings, diagnosis, management, and severity in children with abdominal pain. |

### Symptoms, screening, and monitoring

Physiologic signals, symptom severity, diagnostic support, and measurement.

| Dataset | Participant file | Outcome | Best for |
|---|---:|---|---|
| [Cardiotocography](#cardiotocography) | 2,126 × 23 | `CLASS`, `NSP` | Fetal heart-rate and uterine-contraction measurements with expert fetal-state classifications. |
| [Parkinsons Telemonitoring](#parkinsons-telemonitoring) | 5,000 × 22 | `motor_UPDRS`, `total_UPDRS` | Repeated voice measurements and Parkinson disease symptom-severity scores. |
| [Diabetic Retinopathy Debrecen](#diabetic-retinopathy) | 1,151 × 20 | `Class` | Retinal image-derived features for diabetic retinopathy screening. |
| [Infrared Thermography Temperature](#infrared-thermography-temperature) | 1,020 × 30 | `aveOralF`, `aveOralM` | Infrared facial temperatures, oral temperature, environment, and participant characteristics. |
| [EEG Eye State](#eeg-eye-state) | 5,000 × 15 | `eyeDetection` | EEG channel measurements paired with open-versus-closed eye state. |
| [Cervical Cancer (Risk Factors)](#cervical-cancer-screening) | 858 × 30 | 4 documented targets | Demographics, reproductive and sexual health history, smoking, contraception, sexually transmitted infections, and cervical screening results. |
| [Glioma Grading Clinical and Mutation Features](#glioma-grading) | 839 × 25 | `Grade` | Clinical and molecular features associated with lower-grade versus glioblastoma tumor classification. |

### Health behavior, aging, and workforce

Behavior, substance use, occupational health, sleep, aging, and health-service use.

| Dataset | Participant file | Outcome | Best for |
|---|---:|---|---|
| [Estimation of Obesity Levels Based On Eating Habits and Physical Condition](#obesity-lifestyle) | 2,111 × 17 | `NObeyesdad` | Eating habits, physical activity, transportation, anthropometrics, and obesity category. |
| [Drug Consumption (Quantified)](#drug-consumption) | 1,885 × 30 | 17 documented targets | Demographics, personality measures, sensation seeking, and self-reported substance-use categories. |
| [Absenteeism at work](#workplace-absenteeism) | 740 × 21 | `Absenteeism time in hours` | Worker characteristics, health behaviors, work context, reasons for absence, and absence duration. |
| [National Poll on Healthy Aging (NPHA)](#healthy-aging-poll) | 714 × 15 | `Number_of_Doctors_Visited` | Health, sleep, caregiving, insurance, medication, dental care, and health-service use among adults age 50 and older. |

### Environment and care quality

Environmental exposures, patient experience, and health-care quality.

| Dataset | Participant file | Outcome | Best for |
|---|---:|---|---|
| [Air Quality](#air-quality-sensors) | 5,000 × 15 | Choose based on question | Hourly air-pollutant reference measurements, sensor responses, temperature, and humidity. |
| [Beijing PM2.5](#beijing-pm25) | 5,000 × 13 | `pm2.5` | Hourly PM2.5, weather, wind direction, and precipitation measurements. |
| [Patient survey (HCAHPS) - Hospital](#hospital-patient-experience) | 5,000 × 22 | Choose based on question | Hospital-level HCAHPS measures of nurse communication, discharge information, care transitions, environment, ratings, and willingness to recommend. |

## Compare all 20

| Dataset | Research area | Shape | Weight |
|---|---|---:|---|
| [Diabetes 130-US Hospitals for Years 1999-2008](#diabetes-readmission) | Clinical outcomes and health services | 5,000 × 30 | None supplied |
| [SUPPORT2](#support2-serious-illness) | Clinical outcomes and serious illness | 5,000 × 30 | None supplied |
| [Myocardial infarction complications](#myocardial-infarction-complications) | Clinical outcomes and acute care | 1,700 × 30 | None supplied |
| [AIDS Clinical Trials Group Study 175](#aids-clinical-trial-175) | Clinical trials and infectious disease | 2,139 × 25 | None supplied |
| [Hepatitis C Virus (HCV) for Egyptian patients](#hepatitis-c-treatment) | Clinical outcomes and infectious disease | 1,385 × 29 | None supplied |
| [Cardiotocography](#cardiotocography) | Maternal and fetal health | 2,126 × 23 | None supplied |
| [Parkinsons Telemonitoring](#parkinsons-telemonitoring) | Symptoms and remote monitoring | 5,000 × 22 | None supplied |
| [Diabetic Retinopathy Debrecen](#diabetic-retinopathy) | Screening and diagnostic support | 1,151 × 20 | None supplied |
| [Infrared Thermography Temperature](#infrared-thermography-temperature) | Screening and measurement science | 1,020 × 30 | None supplied |
| [EEG Eye State](#eeg-eye-state) | Neurophysiology and monitoring | 5,000 × 15 | None supplied |
| [Estimation of Obesity Levels Based On Eating Habits and Physical Condition](#obesity-lifestyle) | Health behavior and chronic disease | 2,111 × 17 | None supplied |
| [Drug Consumption (Quantified)](#drug-consumption) | Health behavior and substance use | 1,885 × 30 | None supplied |
| [Absenteeism at work](#workplace-absenteeism) | Occupational health and workforce | 740 × 21 | None supplied |
| [Regensburg Pediatric Appendicitis](#pediatric-appendicitis) | Pediatric acute care | 782 × 30 | None supplied |
| [National Poll on Healthy Aging (NPHA)](#healthy-aging-poll) | Older-adult health and health services | 714 × 15 | None supplied |
| [Cervical Cancer (Risk Factors)](#cervical-cancer-screening) | Women's health and cancer screening | 858 × 30 | None supplied |
| [Air Quality](#air-quality-sensors) | Environmental health | 5,000 × 15 | None supplied |
| [Beijing PM2.5](#beijing-pm25) | Environmental health | 5,000 × 13 | None supplied |
| [Glioma Grading Clinical and Mutation Features](#glioma-grading) | Cancer care and precision health | 839 × 25 | None supplied |
| [Patient survey (HCAHPS) - Hospital](#hospital-patient-experience) | Patient experience and care quality | 5,000 × 22 | None supplied |

## Pause before modeling

> A high-performing model can still answer the wrong question, use information unavailable at decision time, or reproduce inequity.

- Many clinical and sensor datasets are convenience samples, not nationally representative surveys. Only use weights when the source explicitly provides one.
- Define the prediction time before selecting variables. Measurements collected after admission, treatment, or outcome determination can create leakage.
- Demographic and geographic variables can encode structural inequity and proxy protected characteristics. Audit missingness, representation, and subgroup errors.
- Community-level associations do not establish individual-level relationships; avoid ecological fallacy.
- The obesity dataset includes synthetic records according to its official documentation; it is useful for teaching but not population inference.
- Dataset age, geography, and collection context limit transportability to current clinical practice or other populations.

## Full dataset cards

Open a card to see the official source, version, selected variables, research questions, and audit files.

<a id="diabetes-readmission"></a>

<details>
<summary><strong>Diabetes 130-US Hospitals for Years 1999-2008</strong> — Inpatient diabetes care, utilization, treatment, and 30-day readmission.</summary>

- **Theme:** Clinical outcomes and health services
- **Nursing science connection:** Inpatient diabetes care, utilization, treatment, and 30-day readmission.
- **Official source:** [UCI dataset 296](https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008)
- **Version:** dataset year 2014; record last updated Tue Sep 24 2024
- **Source/participant size:** 101,766 source rows; 5,000 participant rows; 30 source variables
- **Official target(s):** `readmitted`
- **Weighting:** No weighting variable supplied
- **Selected variables:** `encounter_id`, `race`, `gender`, `age`, `admission_type_id`, `discharge_disposition_id`, `admission_source_id`, `time_in_hospital`, `medical_specialty`, `num_lab_procedures`, `num_procedures`, `num_medications`, `number_outpatient`, `number_emergency`, `number_inpatient`, `number_diagnoses`, `max_glu_serum`, `A1Cresult`, `insulin`, `change`, `diabetesMed`, `readmitted`, `patient_nbr`, `weight`, `payer_code`, `diag_1`, `diag_2`, `diag_3`, `metformin`, `repaglinide`
- **Potential research questions:**

  1. How does prior-year health care utilization relate to readmission within 30 days?
  2. Is inpatient HbA1c testing associated with early readmission after describing case mix and prior utilization?
  3. How do early-readmission patterns differ across recorded race, gender, and age groups?

Artifacts: [`participant.csv`](../data/processed/portfolio/diabetes_readmission/participant.csv) · [`data dictionary`](../metadata/portfolio/diabetes_readmission/data_dictionary.csv) · [`provenance`](../metadata/portfolio/diabetes_readmission/provenance.json) · [`risk flags`](../metadata/portfolio/diabetes_readmission/risk_flags.csv) · [`validation`](../metadata/portfolio/diabetes_readmission/validation_report.json)

</details>

<a id="support2-serious-illness"></a>

<details>
<summary><strong>SUPPORT2</strong> — Prognosis, mortality, physiology, function, and care decisions among seriously ill hospitalized adults.</summary>

- **Theme:** Clinical outcomes and serious illness
- **Nursing science connection:** Prognosis, mortality, physiology, function, and care decisions among seriously ill hospitalized adults.
- **Official source:** [UCI dataset 880](https://archive.ics.uci.edu/dataset/880/support2)
- **Version:** dataset year 1995; record last updated Mon Sep 09 2024
- **Source/participant size:** 9,105 source rows; 5,000 participant rows; 30 source variables
- **Official target(s):** `hospdead`, `death`, `sfdm2`
- **Weighting:** No weighting variable supplied
- **Selected variables:** `id`, `age`, `sex`, `race`, `edu`, `income`, `dzgroup`, `dzclass`, `num.co`, `scoma`, `meanbp`, `wblc`, `hrt`, `resp`, `temp`, `pafi`, `alb`, `bili`, `crea`, `sod`, `ph`, `glucose`, `bun`, `urine`, `adlp`, `adls`, `dnr`, `hospdead`, `death`, `sfdm2`
- **Potential research questions:**

  1. Which admission physiology and functional measures are associated with in-hospital mortality?
  2. How do prognostic estimates compare with observed survival across diagnostic groups?
  3. How are do-not-resuscitate decisions patterned by illness severity and patient characteristics?

Artifacts: [`participant.csv`](../data/processed/portfolio/support2_serious_illness/participant.csv) · [`data dictionary`](../metadata/portfolio/support2_serious_illness/data_dictionary.csv) · [`provenance`](../metadata/portfolio/support2_serious_illness/provenance.json) · [`risk flags`](../metadata/portfolio/support2_serious_illness/risk_flags.csv) · [`validation`](../metadata/portfolio/support2_serious_illness/validation_report.json)

</details>

<a id="myocardial-infarction-complications"></a>

<details>
<summary><strong>Myocardial infarction complications</strong> — Pre-admission history, acute measurements, treatment, and complications after myocardial infarction.</summary>

- **Theme:** Clinical outcomes and acute care
- **Nursing science connection:** Pre-admission history, acute measurements, treatment, and complications after myocardial infarction.
- **Official source:** [UCI dataset 579](https://archive.ics.uci.edu/dataset/579/myocardial+infarction+complications)
- **Version:** dataset year 2020; record last updated Fri Nov 03 2023
- **Source/participant size:** 1,700 source rows; 1,700 participant rows; 30 source variables
- **Official target(s):** `FIBR_PREDS`, `PREDS_TAH`, `FIBR_JELUD`, `OTEK_LANC`, `RAZRIV`, `ZSN`, `REC_IM`, `LET_IS`
- **Weighting:** No weighting variable supplied
- **Selected variables:** `ID`, `AGE`, `SEX`, `INF_ANAM`, `STENOK_AN`, `FK_STENOK`, `IBS_POST`, `IBS_NASL`, `GB`, `SIM_GIPERT`, `DLIT_AG`, `ZSN_A`, `S_AD_KBRIG`, `D_AD_KBRIG`, `K_BLOOD`, `NA_BLOOD`, `ALT_BLOOD`, `AST_BLOOD`, `L_BLOOD`, `ROE`, `TIME_B_S`, `ASP_S_n`, `FIBR_PREDS`, `PREDS_TAH`, `FIBR_JELUD`, `OTEK_LANC`, `RAZRIV`, `ZSN`, `REC_IM`, `LET_IS`
- **Potential research questions:**

  1. Which presenting characteristics are associated with life-threatening myocardial infarction complications?
  2. How do electrolyte and enzyme measurements differ across complication profiles?
  3. How sensitive are risk models to including treatments delivered after presentation?

Artifacts: [`participant.csv`](../data/processed/portfolio/myocardial_infarction_complications/participant.csv) · [`data dictionary`](../metadata/portfolio/myocardial_infarction_complications/data_dictionary.csv) · [`provenance`](../metadata/portfolio/myocardial_infarction_complications/provenance.json) · [`risk flags`](../metadata/portfolio/myocardial_infarction_complications/risk_flags.csv) · [`validation`](../metadata/portfolio/myocardial_infarction_complications/validation_report.json)

</details>

<a id="aids-clinical-trial-175"></a>

<details>
<summary><strong>AIDS Clinical Trials Group Study 175</strong> — Randomized HIV treatment, immune markers, symptoms, and clinical progression.</summary>

- **Theme:** Clinical trials and infectious disease
- **Nursing science connection:** Randomized HIV treatment, immune markers, symptoms, and clinical progression.
- **Official source:** [UCI dataset 890](https://archive.ics.uci.edu/dataset/890/aids+clinical+trials+group+study+175)
- **Version:** dataset year 1996; record last updated Fri Nov 03 2023
- **Source/participant size:** 2,139 source rows; 2,139 participant rows; 25 source variables
- **Official target(s):** `cid`
- **Weighting:** No weighting variable supplied
- **Selected variables:** `pidnum`, `age`, `homo`, `race`, `gender`, `cid`, `time`, `trt`, `wtkg`, `hemo`, `drugs`, `karnof`, `oprior`, `z30`, `zprior`, `preanti`, `str2`, `strat`, `symptom`, `treat`, `offtrt`, `cd40`, `cd420`, `cd80`, `cd820`
- **Potential research questions:**

  1. How do treatment arms differ in time to AIDS progression or death?
  2. How do baseline CD4 and CD8 counts relate to subsequent clinical progression?
  3. Do treatment effects or model errors differ across demographic subgroups?

Artifacts: [`participant.csv`](../data/processed/portfolio/aids_clinical_trial_175/participant.csv) · [`data dictionary`](../metadata/portfolio/aids_clinical_trial_175/data_dictionary.csv) · [`provenance`](../metadata/portfolio/aids_clinical_trial_175/provenance.json) · [`risk flags`](../metadata/portfolio/aids_clinical_trial_175/risk_flags.csv) · [`validation`](../metadata/portfolio/aids_clinical_trial_175/validation_report.json)

</details>

<a id="hepatitis-c-treatment"></a>

<details>
<summary><strong>Hepatitis C Virus (HCV) for Egyptian patients</strong> — Symptoms, blood tests, viral RNA over time, and baseline liver histology among patients treated for HCV.</summary>

- **Theme:** Clinical outcomes and infectious disease
- **Nursing science connection:** Symptoms, blood tests, viral RNA over time, and baseline liver histology among patients treated for HCV.
- **Official source:** [UCI dataset 503](https://archive.ics.uci.edu/dataset/503/hepatitis+c+virus+hcv+for+egyptian+patients)
- **Version:** dataset year 2017; record last updated Tue Apr 09 2024
- **Source/participant size:** 1,385 source rows; 1,385 participant rows; 29 source variables
- **Official target(s):** `Baselinehistological staging`
- **Weighting:** No weighting variable supplied
- **Selected variables:** `Age `, `Gender`, `Baselinehistological staging`, `BMI`, `Fever`, `Nausea/Vomting`, `Headache `, `Diarrhea `, `Fatigue & generalized bone ache `, `Jaundice `, `Epigastric pain `, `WBC`, `RBC`, `HGB`, `Plat`, `AST 1`, `ALT 1`, `ALT4`, `ALT 12`, `ALT 24`, `ALT 36`, `ALT 48`, `ALT after 24 w`, `RNA Base`, `RNA 4`, `RNA 12`, `RNA EOT`, `RNA EF`, `Baseline histological Grading`
- **Potential research questions:**

  1. Which baseline symptoms and laboratory measures are associated with histological stage?
  2. How do ALT and RNA measurements change across treatment time points?
  3. Can early RNA measurements identify patients with later end-of-treatment response?

Artifacts: [`participant.csv`](../data/processed/portfolio/hepatitis_c_treatment/participant.csv) · [`data dictionary`](../metadata/portfolio/hepatitis_c_treatment/data_dictionary.csv) · [`provenance`](../metadata/portfolio/hepatitis_c_treatment/provenance.json) · [`risk flags`](../metadata/portfolio/hepatitis_c_treatment/risk_flags.csv) · [`validation`](../metadata/portfolio/hepatitis_c_treatment/validation_report.json)

</details>

<a id="cardiotocography"></a>

<details>
<summary><strong>Cardiotocography</strong> — Fetal heart-rate and uterine-contraction measurements with expert fetal-state classifications.</summary>

- **Theme:** Maternal and fetal health
- **Nursing science connection:** Fetal heart-rate and uterine-contraction measurements with expert fetal-state classifications.
- **Official source:** [UCI dataset 193](https://archive.ics.uci.edu/dataset/193/cardiotocography)
- **Version:** dataset year 2000; record last updated Fri Mar 15 2024
- **Source/participant size:** 2,126 source rows; 2,126 participant rows; 23 source variables
- **Official target(s):** `CLASS`, `NSP`
- **Weighting:** No weighting variable supplied
- **Selected variables:** `CLASS`, `NSP`, `LB`, `AC`, `FM`, `UC`, `DL`, `DS`, `DP`, `ASTV`, `MSTV`, `ALTV`, `MLTV`, `Width`, `Min`, `Max`, `Nmax`, `Nzeros`, `Mode`, `Mean`, `Median`, `Variance`, `Tendency`
- **Potential research questions:**

  1. Which cardiotocographic measurements distinguish normal, suspect, and pathologic fetal states?
  2. How are accelerations, decelerations, and variability related to expert classification?
  3. Which fetal-state groups are most often confused by classification models?

Artifacts: [`participant.csv`](../data/processed/portfolio/cardiotocography/participant.csv) · [`data dictionary`](../metadata/portfolio/cardiotocography/data_dictionary.csv) · [`provenance`](../metadata/portfolio/cardiotocography/provenance.json) · [`risk flags`](../metadata/portfolio/cardiotocography/risk_flags.csv) · [`validation`](../metadata/portfolio/cardiotocography/validation_report.json)

</details>

<a id="parkinsons-telemonitoring"></a>

<details>
<summary><strong>Parkinsons Telemonitoring</strong> — Repeated voice measurements and Parkinson disease symptom-severity scores.</summary>

- **Theme:** Symptoms and remote monitoring
- **Nursing science connection:** Repeated voice measurements and Parkinson disease symptom-severity scores.
- **Official source:** [UCI dataset 189](https://archive.ics.uci.edu/dataset/189/parkinsons+telemonitoring)
- **Version:** dataset year 2009; record last updated Fri Nov 03 2023
- **Source/participant size:** 5,875 source rows; 5,000 participant rows; 22 source variables
- **Official target(s):** `motor_UPDRS`, `total_UPDRS`
- **Weighting:** No weighting variable supplied
- **Selected variables:** `subject#`, `age`, `sex`, `motor_UPDRS`, `total_UPDRS`, `test_time`, `Jitter(%)`, `Jitter(Abs)`, `Jitter:RAP`, `Jitter:PPQ5`, `Jitter:DDP`, `Shimmer`, `Shimmer(dB)`, `Shimmer:APQ3`, `Shimmer:APQ5`, `Shimmer:APQ11`, `Shimmer:DDA`, `NHR`, `HNR`, `RPDE`, `DFA`, `PPE`
- **Potential research questions:**

  1. Which voice features are most strongly associated with motor UPDRS severity?
  2. How do voice measurements and symptom scores change over study time?
  3. How should repeated observations from the same participant be handled during model validation?

Artifacts: [`participant.csv`](../data/processed/portfolio/parkinsons_telemonitoring/participant.csv) · [`data dictionary`](../metadata/portfolio/parkinsons_telemonitoring/data_dictionary.csv) · [`provenance`](../metadata/portfolio/parkinsons_telemonitoring/provenance.json) · [`risk flags`](../metadata/portfolio/parkinsons_telemonitoring/risk_flags.csv) · [`validation`](../metadata/portfolio/parkinsons_telemonitoring/validation_report.json)

</details>

<a id="diabetic-retinopathy"></a>

<details>
<summary><strong>Diabetic Retinopathy Debrecen</strong> — Retinal image-derived features for diabetic retinopathy screening.</summary>

- **Theme:** Screening and diagnostic support
- **Nursing science connection:** Retinal image-derived features for diabetic retinopathy screening.
- **Official source:** [UCI dataset 329](https://archive.ics.uci.edu/dataset/329/diabetic+retinopathy+debrecen)
- **Version:** dataset year 2014; record last updated Fri Nov 03 2023
- **Source/participant size:** 1,151 source rows; 1,151 participant rows; 20 source variables
- **Official target(s):** `Class`
- **Weighting:** No weighting variable supplied
- **Selected variables:** `Class`, `quality`, `pre_screening`, `ma1`, `ma2`, `ma3`, `ma4`, `ma5`, `ma6`, `exudate1`, `exudate2`, `exudate3`, `exudate5`, `exudate6`, `exudate7`, `exudate8`, `macula_opticdisc_distance`, `opticdisc_diameter`, `am_fm_classification`, `exudate3.1`
- **Potential research questions:**

  1. Which retinal image features are associated with diabetic retinopathy screening classification?
  2. How does image quality affect classification performance?
  3. What sensitivity-specificity tradeoff would be appropriate for a screening workflow?

Artifacts: [`participant.csv`](../data/processed/portfolio/diabetic_retinopathy/participant.csv) · [`data dictionary`](../metadata/portfolio/diabetic_retinopathy/data_dictionary.csv) · [`provenance`](../metadata/portfolio/diabetic_retinopathy/provenance.json) · [`risk flags`](../metadata/portfolio/diabetic_retinopathy/risk_flags.csv) · [`validation`](../metadata/portfolio/diabetic_retinopathy/validation_report.json)

</details>

<a id="infrared-thermography-temperature"></a>

<details>
<summary><strong>Infrared Thermography Temperature</strong> — Infrared facial temperatures, oral temperature, environment, and participant characteristics.</summary>

- **Theme:** Screening and measurement science
- **Nursing science connection:** Infrared facial temperatures, oral temperature, environment, and participant characteristics.
- **Official source:** [UCI dataset 925](https://archive.ics.uci.edu/dataset/925/infrared+thermography+temperature+dataset)
- **Version:** dataset year 2021; record last updated Tue Dec 12 2023
- **Source/participant size:** 1,020 source rows; 1,020 participant rows; 30 source variables
- **Official target(s):** `aveOralF`, `aveOralM`
- **Weighting:** No weighting variable supplied
- **Selected variables:** `SubjectID`, `Gender`, `Age`, `Ethnicity`, `T_atm`, `Humidity`, `Distance`, `T_offset1`, `Max1R13_1`, `Max1L13_1`, `aveAllR13_1`, `aveAllL13_1`, `T_RC1`, `T_LC1`, `RCC1`, `LCC1`, `canthiMax1`, `canthi4Max1`, `T_FHCC1`, `T_FHRC1`, `T_FHLC1`, `T_FHBC1`, `T_FHTC1`, `T_FH_Max1`, `T_FHC_Max1`, `T_Max1`, `T_OR1`, `T_OR_Max1`, `aveOralF`, `aveOralM`
- **Potential research questions:**

  1. How accurately do facial infrared measurements estimate oral temperature?
  2. How do ambient temperature, humidity, and measurement distance affect agreement?
  3. Does measurement error differ across age, gender, or ethnicity groups?

Artifacts: [`participant.csv`](../data/processed/portfolio/infrared_thermography_temperature/participant.csv) · [`data dictionary`](../metadata/portfolio/infrared_thermography_temperature/data_dictionary.csv) · [`provenance`](../metadata/portfolio/infrared_thermography_temperature/provenance.json) · [`risk flags`](../metadata/portfolio/infrared_thermography_temperature/risk_flags.csv) · [`validation`](../metadata/portfolio/infrared_thermography_temperature/validation_report.json)

</details>

<a id="eeg-eye-state"></a>

<details>
<summary><strong>EEG Eye State</strong> — EEG channel measurements paired with open-versus-closed eye state.</summary>

- **Theme:** Neurophysiology and monitoring
- **Nursing science connection:** EEG channel measurements paired with open-versus-closed eye state.
- **Official source:** [UCI dataset 264](https://archive.ics.uci.edu/dataset/264/eeg+eye+state)
- **Version:** dataset year 2013; record last updated Thu Mar 21 2024
- **Source/participant size:** 14,980 source rows; 5,000 participant rows; 15 source variables
- **Official target(s):** `eyeDetection`
- **Weighting:** No weighting variable supplied
- **Selected variables:** `eyeDetection`, `AF3`, `F7`, `F3`, `FC5`, `T7`, `P7`, `O1`, `O2`, `P8`, `T8`, `FC6`, `F4`, `F8`, `AF4`
- **Potential research questions:**

  1. Which EEG channels best distinguish open from closed eye state?
  2. How stable is classification across time-ordered segments?
  3. How do artifacts and extreme channel values affect model performance?

Artifacts: [`participant.csv`](../data/processed/portfolio/eeg_eye_state/participant.csv) · [`data dictionary`](../metadata/portfolio/eeg_eye_state/data_dictionary.csv) · [`provenance`](../metadata/portfolio/eeg_eye_state/provenance.json) · [`risk flags`](../metadata/portfolio/eeg_eye_state/risk_flags.csv) · [`validation`](../metadata/portfolio/eeg_eye_state/validation_report.json)

</details>

<a id="obesity-lifestyle"></a>

<details>
<summary><strong>Estimation of Obesity Levels Based On Eating Habits and Physical Condition</strong> — Eating habits, physical activity, transportation, anthropometrics, and obesity category.</summary>

- **Theme:** Health behavior and chronic disease
- **Nursing science connection:** Eating habits, physical activity, transportation, anthropometrics, and obesity category.
- **Official source:** [UCI dataset 544](https://archive.ics.uci.edu/dataset/544/estimation+of+obesity+levels+based+on+eating+habits+and+physical+condition)
- **Version:** dataset year 2019; record last updated Tue Sep 10 2024
- **Source/participant size:** 2,111 source rows; 2,111 participant rows; 17 source variables
- **Official target(s):** `NObeyesdad`
- **Weighting:** No weighting variable supplied
- **Selected variables:** `Gender`, `Age`, `NObeyesdad`, `Height`, `Weight`, `family_history_with_overweight`, `FAVC`, `FCVC`, `NCP`, `CAEC`, `SMOKE`, `CH2O`, `SCC`, `FAF`, `TUE`, `CALC`, `MTRANS`
- **Potential research questions:**

  1. How are physical activity, food patterns, and transportation associated with obesity category?
  2. How does family history modify observed associations between behavior and obesity?
  3. How much apparent predictive performance comes directly from height and weight?

Artifacts: [`participant.csv`](../data/processed/portfolio/obesity_lifestyle/participant.csv) · [`data dictionary`](../metadata/portfolio/obesity_lifestyle/data_dictionary.csv) · [`provenance`](../metadata/portfolio/obesity_lifestyle/provenance.json) · [`risk flags`](../metadata/portfolio/obesity_lifestyle/risk_flags.csv) · [`validation`](../metadata/portfolio/obesity_lifestyle/validation_report.json)

</details>

<a id="drug-consumption"></a>

<details>
<summary><strong>Drug Consumption (Quantified)</strong> — Demographics, personality measures, sensation seeking, and self-reported substance-use categories.</summary>

- **Theme:** Health behavior and substance use
- **Nursing science connection:** Demographics, personality measures, sensation seeking, and self-reported substance-use categories.
- **Official source:** [UCI dataset 373](https://archive.ics.uci.edu/dataset/373/drug+consumption+quantified)
- **Version:** dataset year 2015; record last updated Fri Mar 08 2024
- **Source/participant size:** 1,885 source rows; 1,885 participant rows; 30 source variables
- **Official target(s):** `alcohol`, `amphet`, `benzos`, `caff`, `cannabis`, `coke`, `crack`, `ecstasy`, `heroin`, `ketamine`, `legalh`, `lsd`, `meth`, `mushrooms`, `nicotine`, `semer`, `vsa`
- **Weighting:** No weighting variable supplied
- **Selected variables:** `id`, `age`, `gender`, `education`, `country`, `ethnicity`, `nscore`, `escore`, `oscore`, `ascore`, `cscore`, `impuslive`, `ss`, `alcohol`, `amphet`, `benzos`, `caff`, `cannabis`, `coke`, `crack`, `ecstasy`, `heroin`, `ketamine`, `legalh`, `lsd`, `meth`, `mushrooms`, `nicotine`, `semer`, `vsa`
- **Potential research questions:**

  1. Which personality and sensation-seeking measures are associated with substance-use recency?
  2. What patterns of polysubstance use appear across the recorded drug categories?
  3. How do subgroup imbalance and sensitive demographics affect classification performance?

Artifacts: [`participant.csv`](../data/processed/portfolio/drug_consumption/participant.csv) · [`data dictionary`](../metadata/portfolio/drug_consumption/data_dictionary.csv) · [`provenance`](../metadata/portfolio/drug_consumption/provenance.json) · [`risk flags`](../metadata/portfolio/drug_consumption/risk_flags.csv) · [`validation`](../metadata/portfolio/drug_consumption/validation_report.json)

</details>

<a id="workplace-absenteeism"></a>

<details>
<summary><strong>Absenteeism at work</strong> — Worker characteristics, health behaviors, work context, reasons for absence, and absence duration.</summary>

- **Theme:** Occupational health and workforce
- **Nursing science connection:** Worker characteristics, health behaviors, work context, reasons for absence, and absence duration.
- **Official source:** [UCI dataset 445](https://archive.ics.uci.edu/dataset/445/absenteeism+at+work)
- **Version:** dataset year 2012; record last updated Fri Mar 08 2024
- **Source/participant size:** 740 source rows; 740 participant rows; 21 source variables
- **Official target(s):** `Absenteeism time in hours`
- **Weighting:** No weighting variable supplied
- **Selected variables:** `ID`, `Age`, `Education`, `Absenteeism time in hours`, `Reason for absence`, `Month of absence`, `Day of the week`, `Seasons`, `Transportation expense`, `Distance from Residence to Work`, `Service time`, `Work load Average/day `, `Hit target`, `Disciplinary failure`, `Son`, `Social drinker`, `Social smoker`, `Pet`, `Weight`, `Height`, `Body mass index`
- **Potential research questions:**

  1. How are work context, commuting distance, and service time associated with absence duration?
  2. How do BMI, smoking, and alcohol indicators relate to absenteeism patterns?
  3. Which reasons for absence account for the greatest number of lost work hours?

Artifacts: [`participant.csv`](../data/processed/portfolio/workplace_absenteeism/participant.csv) · [`data dictionary`](../metadata/portfolio/workplace_absenteeism/data_dictionary.csv) · [`provenance`](../metadata/portfolio/workplace_absenteeism/provenance.json) · [`risk flags`](../metadata/portfolio/workplace_absenteeism/risk_flags.csv) · [`validation`](../metadata/portfolio/workplace_absenteeism/validation_report.json)

</details>

<a id="pediatric-appendicitis"></a>

<details>
<summary><strong>Regensburg Pediatric Appendicitis</strong> — Symptoms, physical examination, laboratory tests, ultrasound findings, diagnosis, management, and severity in children with abdominal pain.</summary>

- **Theme:** Pediatric acute care
- **Nursing science connection:** Symptoms, physical examination, laboratory tests, ultrasound findings, diagnosis, management, and severity in children with abdominal pain.
- **Official source:** [UCI dataset 938](https://archive.ics.uci.edu/dataset/938/regensburg+pediatric+appendicitis)
- **Version:** dataset year 2023; record last updated Tue Feb 06 2024
- **Source/participant size:** 782 source rows; 782 participant rows; 30 source variables
- **Official target(s):** `Management`, `Severity`, `Diagnosis`
- **Weighting:** No weighting variable supplied
- **Selected variables:** `Age`, `Sex`, `Management`, `Severity`, `Diagnosis`, `BMI`, `Height`, `Weight`, `Length_of_Stay`, `Alvarado_Score`, `Paedriatic_Appendicitis_Score`, `Appendix_on_US`, `Appendix_Diameter`, `Migratory_Pain`, `Lower_Right_Abd_Pain`, `Contralateral_Rebound_Tenderness`, `Coughing_Pain`, `Nausea`, `Loss_of_Appetite`, `Body_Temperature`, `WBC_Count`, `Neutrophil_Percentage`, `Segmented_Neutrophils`, `Neutrophilia`, `RBC_Count`, `Hemoglobin`, `RDW`, `Thrombocyte_Count`, `Ketones_in_Urine`, `RBC_in_Urine`
- **Potential research questions:**

  1. Which presenting symptoms, examination findings, and laboratory values are associated with appendicitis diagnosis?
  2. How do clinical scores compare with individual nursing assessment and laboratory measures?
  3. Which early findings are associated with surgical management or complicated appendicitis?

Artifacts: [`participant.csv`](../data/processed/portfolio/pediatric_appendicitis/participant.csv) · [`data dictionary`](../metadata/portfolio/pediatric_appendicitis/data_dictionary.csv) · [`provenance`](../metadata/portfolio/pediatric_appendicitis/provenance.json) · [`risk flags`](../metadata/portfolio/pediatric_appendicitis/risk_flags.csv) · [`validation`](../metadata/portfolio/pediatric_appendicitis/validation_report.json)

</details>

<a id="healthy-aging-poll"></a>

<details>
<summary><strong>National Poll on Healthy Aging (NPHA)</strong> — Health, sleep, caregiving, insurance, medication, dental care, and health-service use among adults age 50 and older.</summary>

- **Theme:** Older-adult health and health services
- **Nursing science connection:** Health, sleep, caregiving, insurance, medication, dental care, and health-service use among adults age 50 and older.
- **Official source:** [UCI dataset 936](https://archive.ics.uci.edu/dataset/936/national+poll+on+healthy+aging+(npha))
- **Version:** dataset year 2017; record last updated Mon Dec 11 2023
- **Source/participant size:** 714 source rows; 714 participant rows; 15 source variables
- **Official target(s):** `Number_of_Doctors_Visited`
- **Weighting:** No weighting variable supplied
- **Selected variables:** `Age`, `Race`, `Gender`, `Number_of_Doctors_Visited`, `Physical_Health`, `Mental_Health`, `Dental_Health`, `Employment`, `Stress_Keeps_Patient_from_Sleeping`, `Medication_Keeps_Patient_from_Sleeping`, `Pain_Keeps_Patient_from_Sleeping`, `Bathroom_Needs_Keeps_Patient_from_Sleeping`, `Uknown_Keeps_Patient_from_Sleeping`, `Trouble_Sleeping`, `Prescription_Sleep_Medication`
- **Potential research questions:**

  1. How are sleep and self-rated health associated with the number of doctors an older adult visits?
  2. Which health, medication, dental-care, or caregiving factors identify higher health-service use?
  3. Do patterns of health-service use differ across age, gender, or race and ethnicity groups?

Artifacts: [`participant.csv`](../data/processed/portfolio/healthy_aging_poll/participant.csv) · [`data dictionary`](../metadata/portfolio/healthy_aging_poll/data_dictionary.csv) · [`provenance`](../metadata/portfolio/healthy_aging_poll/provenance.json) · [`risk flags`](../metadata/portfolio/healthy_aging_poll/risk_flags.csv) · [`validation`](../metadata/portfolio/healthy_aging_poll/validation_report.json)

</details>

<a id="cervical-cancer-screening"></a>

<details>
<summary><strong>Cervical Cancer (Risk Factors)</strong> — Demographics, reproductive and sexual health history, smoking, contraception, sexually transmitted infections, and cervical screening results.</summary>

- **Theme:** Women's health and cancer screening
- **Nursing science connection:** Demographics, reproductive and sexual health history, smoking, contraception, sexually transmitted infections, and cervical screening results.
- **Official source:** [UCI dataset 383](https://archive.ics.uci.edu/dataset/383/cervical+cancer+risk+factors)
- **Version:** dataset year 2017; record last updated Sun Mar 10 2024
- **Source/participant size:** 858 source rows; 858 participant rows; 30 source variables
- **Official target(s):** `Hinselmann`, `Schiller`, `Citology`, `Biopsy`
- **Weighting:** No weighting variable supplied
- **Selected variables:** `Age`, `Number of sexual partners`, `Hinselmann`, `Schiller`, `Citology`, `Biopsy`, `First sexual intercourse`, `Num of pregnancies`, `Smokes`, `Smokes (years)`, `Smokes (packs/year)`, `Hormonal Contraceptives`, `Hormonal Contraceptives (years)`, `IUD`, `IUD (years)`, `STDs`, `STDs (number)`, `STDs:condylomatosis`, `STDs:cervical condylomatosis`, `STDs:vaginal condylomatosis`, `STDs:vulvo-perineal condylomatosis`, `STDs:syphilis`, `STDs:pelvic inflammatory disease`, `STDs:genital herpes`, `STDs:molluscum contagiosum`, `STDs:AIDS`, `STDs:HIV`, `STDs:Hepatitis B`, `STDs:HPV`, `STDs: Number of diagnosis`
- **Potential research questions:**

  1. Which documented history and exposure variables are associated with biopsy-confirmed cervical disease?
  2. How do the Hinselmann, Schiller, cytology, and biopsy screening results agree or differ?
  3. How does item nonresponse affect apparent screening-risk patterns?

Artifacts: [`participant.csv`](../data/processed/portfolio/cervical_cancer_screening/participant.csv) · [`data dictionary`](../metadata/portfolio/cervical_cancer_screening/data_dictionary.csv) · [`provenance`](../metadata/portfolio/cervical_cancer_screening/provenance.json) · [`risk flags`](../metadata/portfolio/cervical_cancer_screening/risk_flags.csv) · [`validation`](../metadata/portfolio/cervical_cancer_screening/validation_report.json)

</details>

<a id="air-quality-sensors"></a>

<details>
<summary><strong>Air Quality</strong> — Hourly air-pollutant reference measurements, sensor responses, temperature, and humidity.</summary>

- **Theme:** Environmental health
- **Nursing science connection:** Hourly air-pollutant reference measurements, sensor responses, temperature, and humidity.
- **Official source:** [UCI dataset 360](https://archive.ics.uci.edu/dataset/360/air+quality)
- **Version:** dataset year 2008; record last updated Sun Mar 10 2024
- **Source/participant size:** 9,357 source rows; 5,000 participant rows; 15 source variables
- **Source count caveat:** The UCI record reports 9,358 instances; the official normalized data.csv contains 9,357 rows.
- **Official target(s):** No official target designated
- **Weighting:** No weighting variable supplied
- **Selected variables:** `Date`, `Time`, `CO(GT)`, `PT08.S1(CO)`, `NMHC(GT)`, `C6H6(GT)`, `PT08.S2(NMHC)`, `NOx(GT)`, `PT08.S3(NOx)`, `NO2(GT)`, `PT08.S4(NO2)`, `PT08.S5(O3)`, `T`, `RH`, `AH`
- **Potential research questions:**

  1. How do pollutant concentrations vary by time, temperature, and humidity?
  2. How closely do metal-oxide sensor responses track reference pollutant measurements?
  3. How does the source missing-value code affect daily and seasonal summaries?

Artifacts: [`participant.csv`](../data/processed/portfolio/air_quality_sensors/participant.csv) · [`data dictionary`](../metadata/portfolio/air_quality_sensors/data_dictionary.csv) · [`provenance`](../metadata/portfolio/air_quality_sensors/provenance.json) · [`risk flags`](../metadata/portfolio/air_quality_sensors/risk_flags.csv) · [`validation`](../metadata/portfolio/air_quality_sensors/validation_report.json)

</details>

<a id="beijing-pm25"></a>

<details>
<summary><strong>Beijing PM2.5</strong> — Hourly PM2.5, weather, wind direction, and precipitation measurements.</summary>

- **Theme:** Environmental health
- **Nursing science connection:** Hourly PM2.5, weather, wind direction, and precipitation measurements.
- **Official source:** [UCI dataset 381](https://archive.ics.uci.edu/dataset/381/beijing+pm2+5+data)
- **Version:** dataset year 2015; record last updated Sat Mar 16 2024
- **Source/participant size:** 43,824 source rows; 5,000 participant rows; 13 source variables
- **Official target(s):** `pm2.5`
- **Weighting:** No weighting variable supplied
- **Selected variables:** `No`, `pm2.5`, `year`, `month`, `day`, `hour`, `DEWP`, `TEMP`, `PRES`, `cbwd`, `Iws`, `Is`, `Ir`
- **Potential research questions:**

  1. How do wind direction, wind speed, temperature, and pressure relate to PM2.5?
  2. What seasonal and diurnal patterns appear in PM2.5 concentrations?
  3. How does missing PM2.5 measurement affect trend estimates?

Artifacts: [`participant.csv`](../data/processed/portfolio/beijing_pm25/participant.csv) · [`data dictionary`](../metadata/portfolio/beijing_pm25/data_dictionary.csv) · [`provenance`](../metadata/portfolio/beijing_pm25/provenance.json) · [`risk flags`](../metadata/portfolio/beijing_pm25/risk_flags.csv) · [`validation`](../metadata/portfolio/beijing_pm25/validation_report.json)

</details>

<a id="glioma-grading"></a>

<details>
<summary><strong>Glioma Grading Clinical and Mutation Features</strong> — Clinical and molecular features associated with lower-grade versus glioblastoma tumor classification.</summary>

- **Theme:** Cancer care and precision health
- **Nursing science connection:** Clinical and molecular features associated with lower-grade versus glioblastoma tumor classification.
- **Official source:** [UCI dataset 759](https://archive.ics.uci.edu/dataset/759/glioma+grading+clinical+and+mutation+features+dataset)
- **Version:** dataset year 2022; record last updated Fri Nov 03 2023
- **Source/participant size:** 839 source rows; 839 participant rows; 25 source variables
- **Official target(s):** `Grade`
- **Weighting:** No weighting variable supplied
- **Selected variables:** `Gender`, `Age_at_diagnosis`, `Race`, `Grade`, `IDH1`, `TP53`, `ATRX`, `PTEN`, `EGFR`, `CIC`, `MUC16`, `PIK3CA`, `NF1`, `PIK3R1`, `FUBP1`, `RB1`, `NOTCH1`, `BCOR`, `CSMD3`, `SMARCA4`, `GRIN2A`, `IDH2`, `FAT4`, `PDGFRA`, `Case_ID`
- **Potential research questions:**

  1. Which clinical and molecular features are associated with glioma grade?
  2. How does classification performance differ across demographic groups?
  3. What limitations arise when translating molecular tumor classification to nursing assessment or care planning?

Artifacts: [`participant.csv`](../data/processed/portfolio/glioma_grading/participant.csv) · [`data dictionary`](../metadata/portfolio/glioma_grading/data_dictionary.csv) · [`provenance`](../metadata/portfolio/glioma_grading/provenance.json) · [`risk flags`](../metadata/portfolio/glioma_grading/risk_flags.csv) · [`validation`](../metadata/portfolio/glioma_grading/validation_report.json)

</details>

<a id="hospital-patient-experience"></a>

<details>
<summary><strong>Patient survey (HCAHPS) - Hospital</strong> — Hospital-level HCAHPS measures of nurse communication, discharge information, care transitions, environment, ratings, and willingness to recommend.</summary>

- **Theme:** Patient experience and care quality
- **Nursing science connection:** Hospital-level HCAHPS measures of nurse communication, discharge information, care transitions, environment, ratings, and willingness to recommend.
- **Official source:** [Centers for Medicare & Medicaid Services (CMS)](https://data.cms.gov/provider-data/dataset/dgck-syfz)
- **Version:** dataset year 2026; record last updated 2026-07-22
- **Source/participant size:** 325,720 source rows; 5,000 participant rows; 22 source variables
- **Official target(s):** No official target designated
- **Weighting:** No weighting variable supplied
- **Selected variables:** `Facility ID`, `Facility Name`, `City/Town`, `State`, `ZIP Code`, `County/Parish`, `HCAHPS Measure ID`, `HCAHPS Question`, `HCAHPS Answer Description`, `Patient Survey Star Rating`, `HCAHPS Answer Percent`, `HCAHPS Linear Mean Value`, `Number of Completed Surveys`, `Survey Response Rate Percent`, `Start Date`, `End Date`, `Address`, `Telephone Number`, `Patient Survey Star Rating Footnote`, `HCAHPS Answer Percent Footnote`, `Number of Completed Surveys Footnote`, `Survey Response Rate Percent Footnote`
- **Potential research questions:**

  1. How do nurse-communication ratings vary across hospitals and states?
  2. How are discharge-information and care-transition measures related to overall hospital ratings or willingness to recommend?
  3. How do survey volume, response rate, and missing or suppressed results affect comparisons between hospitals?

Artifacts: [`participant.csv`](../data/processed/portfolio/hospital_patient_experience/participant.csv) · [`data dictionary`](../metadata/portfolio/hospital_patient_experience/data_dictionary.csv) · [`provenance`](../metadata/portfolio/hospital_patient_experience/provenance.json) · [`risk flags`](../metadata/portfolio/hospital_patient_experience/risk_flags.csv) · [`validation`](../metadata/portfolio/hospital_patient_experience/validation_report.json)

</details>
