# NINR AI Bootcamp — Day 1: Python + Real Clinical Data

This starter repository is designed for nursing scientists who are new to Python and Jupyter notebooks. Day 1 is about becoming comfortable with code and exploring a **real-world clinical dataset**. There is **no machine learning required** in this module.

## Dataset

We use the **Breast Cancer Wisconsin (Diagnostic)** dataset, originally from the University of Wisconsin and distributed through the UCI Machine Learning Repository. It contains 569 observations and measurements computed from digitized images of fine needle aspirates of breast masses. The outcome is benign vs. malignant.

The copy in `data/` is exported from scikit-learn's bundled copy of the UCI dataset so the workshop works without internet access.

**Important:** This is an educational public dataset, not NIH patient data. Do not interpret the exercises as clinical guidance.

Source: UCI Machine Learning Repository, Breast Cancer Wisconsin (Diagnostic), DOI: 10.24432/C5DW2B.

## Day 1 goals

By the end of the session, participants should be able to:

- explain what a Jupyter notebook is
- run and edit a code cell
- recognize strings, numbers, lists, and variables
- import a Python library
- load a CSV with pandas
- inspect rows, columns, and data types
- select a column and filter rows
- calculate simple summaries
- create a basic visualization
- translate a scientific question into a few lines of exploratory code

## Repository structure

```text
ninr-day1-real-world-data/
├── README.md
├── requirements.txt
├── data/
│   ├── README.md
│   └── wisconsin_breast_cancer_diagnostic.csv
└── notebooks/
    ├── 01_day1_python_real_clinical_data.ipynb
    └── 01_day1_python_real_clinical_data_SOLUTIONS.ipynb
```

## Getting started

Open `notebooks/01_day1_python_real_clinical_data.ipynb` in Jupyter or upload it to Google Colab. If using Colab, also upload the CSV from the `data` folder and adjust the path in the data-loading cell if needed.

## Teaching philosophy

Participants should type, change, break, rerun, and discuss code. The notebook uses **Try it**, **Explore**, and **Think like a scientist** prompts rather than long lectures.
