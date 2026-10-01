# NINR dataset options and research-question catalog

This page compares the 20 reproducible teaching datasets included in the repository. Every raw extract and definition comes from the official UCI Machine Learning Repository record supplied by the original dataset contributor; no Kaggle or third-party mirror is used. Versions were checked on 2026-10-01.

Participant files contain approximately 1,000–5,000 observations and 10–30 source variables, plus `portfolio_row_id`. The occupational absenteeism source contains only 740 records, so its participant file retains all 740 and is the documented size exception.

## Quick comparison

| Dataset | Theme | Participant shape | Weight | Best for |
|---|---|---:|---|---|
| [Diabetes 130-US Hospitals for Years 1999-2008](#diabetes-readmission) | Clinical outcomes and health services | 5,000 × 30 | None supplied | Inpatient diabetes care, utilization, treatment, and 30-day readmission. |
| [SUPPORT2](#support2-serious-illness) | Clinical outcomes and serious illness | 5,000 × 30 | None supplied | Prognosis, mortality, physiology, function, and care decisions among seriously ill hospitalized adults. |
| [Myocardial infarction complications](#myocardial-infarction-complications) | Clinical outcomes and acute care | 1,700 × 30 | None supplied | Pre-admission history, acute measurements, treatment, and complications after myocardial infarction. |
| [AIDS Clinical Trials Group Study 175](#aids-clinical-trial-175) | Clinical trials and infectious disease | 2,139 × 25 | None supplied | Randomized HIV treatment, immune markers, symptoms, and clinical progression. |
| [Hepatitis C Virus (HCV) for Egyptian patients](#hepatitis-c-treatment) | Clinical outcomes and infectious disease | 1,385 × 29 | None supplied | Symptoms, blood tests, viral RNA over time, and baseline liver histology among patients treated for HCV. |
| [Cardiotocography](#cardiotocography) | Maternal and fetal health | 2,126 × 23 | None supplied | Fetal heart-rate and uterine-contraction measurements with expert fetal-state classifications. |
| [Parkinsons Telemonitoring](#parkinsons-telemonitoring) | Symptoms and remote monitoring | 5,000 × 22 | None supplied | Repeated voice measurements and Parkinson disease symptom-severity scores. |
| [Diabetic Retinopathy Debrecen](#diabetic-retinopathy) | Screening and diagnostic support | 1,151 × 20 | None supplied | Retinal image-derived features for diabetic retinopathy screening. |
| [Infrared Thermography Temperature](#infrared-thermography-temperature) | Screening and measurement science | 1,020 × 30 | None supplied | Infrared facial temperatures, oral temperature, environment, and participant characteristics. |
| [EEG Eye State](#eeg-eye-state) | Neurophysiology and monitoring | 5,000 × 15 | None supplied | EEG channel measurements paired with open-versus-closed eye state. |
| [Estimation of Obesity Levels Based On Eating Habits and Physical Condition ](#obesity-lifestyle) | Health behavior and chronic disease | 2,111 × 17 | None supplied | Eating habits, physical activity, transportation, anthropometrics, and obesity category. |
| [Drug Consumption (Quantified)](#drug-consumption) | Health behavior and substance use | 1,885 × 30 | None supplied | Demographics, personality measures, sensation seeking, and self-reported substance-use categories. |
| [Absenteeism at work](#workplace-absenteeism) | Occupational health and workforce | 740 × 21 | None supplied | Worker characteristics, health behaviors, work context, reasons for absence, and absence duration. |
| [Predict Students' Dropout and Academic Success](#student-dropout-sdoh) | Education and social determinants | 4,424 × 30 | None supplied | Educational, financial, demographic, and macroeconomic factors associated with dropout and graduation. |
| [Adult](#adult-income-sdoh) | Economic social determinants | 5,000 × 15 | fnlwgt | Employment, education, work hours, demographics, and income category as an SDOH teaching dataset. |
| [Communities and Crime](#communities-crime-sdoh) | Community social determinants | 1,994 × 30 | None supplied | Community-level demographic, economic, housing, mobility, and public-safety measures. |
| [Air Quality](#air-quality-sensors) | Environmental health | 5,000 × 15 | None supplied | Hourly air-pollutant reference measurements, sensor responses, temperature, and humidity. |
| [Beijing PM2.5](#beijing-pm25) | Environmental health | 5,000 × 13 | None supplied | Hourly PM2.5, weather, wind direction, and precipitation measurements. |
| [Room Occupancy Estimation](#room-occupancy-environment) | Built environment and sensing | 5,000 × 19 | None supplied | Indoor temperature, light, sound, CO2, motion, and room occupancy. |
| [Bike Sharing](#bike-sharing-environment) | Built environment and physical activity | 5,000 × 17 | None supplied | Hourly bike-rental demand with season, weather, workday, and calendar measures. |

## Choosing responsibly

- UCI-hosted clinical and sensor datasets are generally convenience samples, not nationally representative surveys. Only use weights when the source explicitly provides one.
- Define the prediction time before selecting variables. Measurements collected after admission, treatment, or outcome determination can create leakage.
- Demographic and geographic variables can encode structural inequity and proxy protected characteristics. Audit missingness, representation, and subgroup errors.
- Community-level associations do not establish individual-level relationships; avoid ecological fallacy.
- The obesity dataset includes synthetic records according to its official documentation; it is useful for teaching but not population inference.
- Dataset age, geography, and collection context limit transportability to current clinical practice or other populations.

## Dataset details

<a id="diabetes-readmission"></a>

### Diabetes 130-US Hospitals for Years 1999-2008

- **Theme:** Clinical outcomes and health services
- **Why choose it:** Inpatient diabetes care, utilization, treatment, and 30-day readmission.
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

<a id="support2-serious-illness"></a>

### SUPPORT2

- **Theme:** Clinical outcomes and serious illness
- **Why choose it:** Prognosis, mortality, physiology, function, and care decisions among seriously ill hospitalized adults.
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

<a id="myocardial-infarction-complications"></a>

### Myocardial infarction complications

- **Theme:** Clinical outcomes and acute care
- **Why choose it:** Pre-admission history, acute measurements, treatment, and complications after myocardial infarction.
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

<a id="aids-clinical-trial-175"></a>

### AIDS Clinical Trials Group Study 175

- **Theme:** Clinical trials and infectious disease
- **Why choose it:** Randomized HIV treatment, immune markers, symptoms, and clinical progression.
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

<a id="hepatitis-c-treatment"></a>

### Hepatitis C Virus (HCV) for Egyptian patients

- **Theme:** Clinical outcomes and infectious disease
- **Why choose it:** Symptoms, blood tests, viral RNA over time, and baseline liver histology among patients treated for HCV.
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

<a id="cardiotocography"></a>

### Cardiotocography

- **Theme:** Maternal and fetal health
- **Why choose it:** Fetal heart-rate and uterine-contraction measurements with expert fetal-state classifications.
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

<a id="parkinsons-telemonitoring"></a>

### Parkinsons Telemonitoring

- **Theme:** Symptoms and remote monitoring
- **Why choose it:** Repeated voice measurements and Parkinson disease symptom-severity scores.
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

<a id="diabetic-retinopathy"></a>

### Diabetic Retinopathy Debrecen

- **Theme:** Screening and diagnostic support
- **Why choose it:** Retinal image-derived features for diabetic retinopathy screening.
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

<a id="infrared-thermography-temperature"></a>

### Infrared Thermography Temperature

- **Theme:** Screening and measurement science
- **Why choose it:** Infrared facial temperatures, oral temperature, environment, and participant characteristics.
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

<a id="eeg-eye-state"></a>

### EEG Eye State

- **Theme:** Neurophysiology and monitoring
- **Why choose it:** EEG channel measurements paired with open-versus-closed eye state.
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

<a id="obesity-lifestyle"></a>

### Estimation of Obesity Levels Based On Eating Habits and Physical Condition 

- **Theme:** Health behavior and chronic disease
- **Why choose it:** Eating habits, physical activity, transportation, anthropometrics, and obesity category.
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

<a id="drug-consumption"></a>

### Drug Consumption (Quantified)

- **Theme:** Health behavior and substance use
- **Why choose it:** Demographics, personality measures, sensation seeking, and self-reported substance-use categories.
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

<a id="workplace-absenteeism"></a>

### Absenteeism at work

- **Theme:** Occupational health and workforce
- **Why choose it:** Worker characteristics, health behaviors, work context, reasons for absence, and absence duration.
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

<a id="student-dropout-sdoh"></a>

### Predict Students' Dropout and Academic Success

- **Theme:** Education and social determinants
- **Why choose it:** Educational, financial, demographic, and macroeconomic factors associated with dropout and graduation.
- **Official source:** [UCI dataset 697](https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success)
- **Version:** dataset year 2021; record last updated Mon Feb 26 2024
- **Source/participant size:** 4,424 source rows; 4,424 participant rows; 30 source variables
- **Official target(s):** `Target`
- **Weighting:** No weighting variable supplied
- **Selected variables:** `Marital Status`, `Application mode`, `Course`, `Daytime/evening attendance`, `Previous qualification`, `Previous qualification (grade)`, `Mother's qualification`, `Father's qualification`, `Mother's occupation`, `Father's occupation`, `Admission grade`, `Displaced`, `Educational special needs`, `Debtor`, `Tuition fees up to date`, `Gender`, `Scholarship holder`, `Age at enrollment`, `International`, `Curricular units 1st sem (enrolled)`, `Curricular units 1st sem (approved)`, `Curricular units 1st sem (grade)`, `Curricular units 2nd sem (enrolled)`, `Curricular units 2nd sem (approved)`, `Curricular units 2nd sem (grade)`, `Unemployment rate`, `Inflation rate`, `GDP`, `Target`, `Nacionality`
- **Potential research questions:**

  1. How are tuition status, debt, and scholarship support associated with dropout?
  2. How much do first-semester versus second-semester measures change predictive performance?
  3. Do prediction errors differ for displaced, international, older, or special-needs students?

Artifacts: [`participant.csv`](../data/processed/portfolio/student_dropout_sdoh/participant.csv) · [`data dictionary`](../metadata/portfolio/student_dropout_sdoh/data_dictionary.csv) · [`provenance`](../metadata/portfolio/student_dropout_sdoh/provenance.json) · [`risk flags`](../metadata/portfolio/student_dropout_sdoh/risk_flags.csv) · [`validation`](../metadata/portfolio/student_dropout_sdoh/validation_report.json)

<a id="adult-income-sdoh"></a>

### Adult

- **Theme:** Economic social determinants
- **Why choose it:** Employment, education, work hours, demographics, and income category as an SDOH teaching dataset.
- **Official source:** [UCI dataset 2](https://archive.ics.uci.edu/dataset/2/adult)
- **Version:** dataset year 1996; record last updated Tue Sep 24 2024
- **Source/participant size:** 48,842 source rows; 5,000 participant rows; 15 source variables
- **Official target(s):** `income`
- **Weighting:** fnlwgt
- **Selected variables:** `age`, `workclass`, `education`, `education-num`, `marital-status`, `occupation`, `relationship`, `race`, `sex`, `native-country`, `income`, `fnlwgt`, `capital-gain`, `capital-loss`, `hours-per-week`
- **Potential research questions:**

  1. How are education, occupation, and weekly work hours associated with income category?
  2. How do weighted and unweighted descriptions differ when using the provided final weight?
  3. How do model errors and predicted income differ across race and sex groups?

Artifacts: [`participant.csv`](../data/processed/portfolio/adult_income_sdoh/participant.csv) · [`data dictionary`](../metadata/portfolio/adult_income_sdoh/data_dictionary.csv) · [`provenance`](../metadata/portfolio/adult_income_sdoh/provenance.json) · [`risk flags`](../metadata/portfolio/adult_income_sdoh/risk_flags.csv) · [`validation`](../metadata/portfolio/adult_income_sdoh/validation_report.json)

<a id="communities-crime-sdoh"></a>

### Communities and Crime

- **Theme:** Community social determinants
- **Why choose it:** Community-level demographic, economic, housing, mobility, and public-safety measures.
- **Official source:** [UCI dataset 183](https://archive.ics.uci.edu/dataset/183/communities+and+crime)
- **Version:** dataset year 2002; record last updated Mon Mar 04 2024
- **Source/participant size:** 1,994 source rows; 1,994 participant rows; 30 source variables
- **Official target(s):** `ViolentCrimesPerPop`
- **Weighting:** No weighting variable supplied
- **Selected variables:** `state`, `county`, `community`, `communityname`, `population`, `householdsize`, `racepctblack`, `racePctWhite`, `racePctAsian`, `racePctHisp`, `agePct65up`, `pctUrban`, `medIncome`, `pctWPubAsst`, `perCapInc`, `PctPopUnderPov`, `PctNotHSGrad`, `PctUnemployed`, `PctEmploy`, `PctFam2Par`, `PctNotSpeakEnglWell`, `PctPersDenseHous`, `PctHousNoPhone`, `PctWOFullPlumb`, `NumInShelters`, `NumStreet`, `PctForeignBorn`, `PopDens`, `PctUsePubTrans`, `ViolentCrimesPerPop`
- **Potential research questions:**

  1. How are poverty, unemployment, and educational attainment associated with community violent-crime rates?
  2. How do housing conditions, density, and public transportation relate to community outcomes?
  3. How can ecological fallacy and racial proxy discrimination distort interpretations of community-level models?

Artifacts: [`participant.csv`](../data/processed/portfolio/communities_crime_sdoh/participant.csv) · [`data dictionary`](../metadata/portfolio/communities_crime_sdoh/data_dictionary.csv) · [`provenance`](../metadata/portfolio/communities_crime_sdoh/provenance.json) · [`risk flags`](../metadata/portfolio/communities_crime_sdoh/risk_flags.csv) · [`validation`](../metadata/portfolio/communities_crime_sdoh/validation_report.json)

<a id="air-quality-sensors"></a>

### Air Quality

- **Theme:** Environmental health
- **Why choose it:** Hourly air-pollutant reference measurements, sensor responses, temperature, and humidity.
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

<a id="beijing-pm25"></a>

### Beijing PM2.5

- **Theme:** Environmental health
- **Why choose it:** Hourly PM2.5, weather, wind direction, and precipitation measurements.
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

<a id="room-occupancy-environment"></a>

### Room Occupancy Estimation

- **Theme:** Built environment and sensing
- **Why choose it:** Indoor temperature, light, sound, CO2, motion, and room occupancy.
- **Official source:** [UCI dataset 864](https://archive.ics.uci.edu/dataset/864/room+occupancy+estimation)
- **Version:** dataset year 2018; record last updated Wed Aug 16 2023
- **Source/participant size:** 10,129 source rows; 5,000 participant rows; 19 source variables
- **Official target(s):** `Room_Occupancy_Count`
- **Weighting:** No weighting variable supplied
- **Selected variables:** `Room_Occupancy_Count`, `Date`, `Time`, `S1_Temp`, `S2_Temp`, `S3_Temp`, `S4_Temp`, `S1_Light`, `S2_Light`, `S3_Light`, `S4_Light`, `S1_Sound`, `S2_Sound`, `S3_Sound`, `S4_Sound`, `S5_CO2`, `S5_CO2_Slope`, `S6_PIR`, `S7_PIR`
- **Potential research questions:**

  1. Which indoor environmental sensors best distinguish room occupancy levels?
  2. How quickly does CO2 respond to changes in occupancy?
  3. Does model performance remain stable across different dates and times?

Artifacts: [`participant.csv`](../data/processed/portfolio/room_occupancy_environment/participant.csv) · [`data dictionary`](../metadata/portfolio/room_occupancy_environment/data_dictionary.csv) · [`provenance`](../metadata/portfolio/room_occupancy_environment/provenance.json) · [`risk flags`](../metadata/portfolio/room_occupancy_environment/risk_flags.csv) · [`validation`](../metadata/portfolio/room_occupancy_environment/validation_report.json)

<a id="bike-sharing-environment"></a>

### Bike Sharing

- **Theme:** Built environment and physical activity
- **Why choose it:** Hourly bike-rental demand with season, weather, workday, and calendar measures.
- **Official source:** [UCI dataset 275](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset)
- **Version:** dataset year 2013; record last updated Sun Mar 10 2024
- **Source/participant size:** 17,379 source rows; 5,000 participant rows; 17 source variables
- **Source count caveat:** The UCI record reports 17,389 instances; the official normalized data.csv contains 17,379 rows.
- **Official target(s):** `cnt`
- **Weighting:** No weighting variable supplied
- **Selected variables:** `instant`, `cnt`, `dteday`, `season`, `yr`, `mnth`, `hr`, `holiday`, `weekday`, `workingday`, `weathersit`, `temp`, `atemp`, `hum`, `windspeed`, `casual`, `registered`
- **Potential research questions:**

  1. How do temperature, humidity, wind, and weather conditions relate to bike demand?
  2. How do hourly patterns differ between workdays, holidays, and seasons?
  3. Why would using casual and registered counts to predict total count create leakage?

Artifacts: [`participant.csv`](../data/processed/portfolio/bike_sharing_environment/participant.csv) · [`data dictionary`](../metadata/portfolio/bike_sharing_environment/data_dictionary.csv) · [`provenance`](../metadata/portfolio/bike_sharing_environment/provenance.json) · [`risk flags`](../metadata/portfolio/bike_sharing_environment/risk_flags.csv) · [`validation`](../metadata/portfolio/bike_sharing_environment/validation_report.json)

