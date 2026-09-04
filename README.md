# NINR AI Bootcamp — Day 1: Python, Notebooks, and Real Clinical Data

This repository contains the Day 1 beginner exercises for the NINR AI Bootcamp. The goal is to get participants comfortable with Python, Jupyter notebooks, pandas, and asking simple questions of a real health dataset — **before introducing machine learning**.

## Dataset

The notebook uses the **Diabetes 130-US Hospitals for Years 1999–2008** dataset from the UCI Machine Learning Repository. It contains 101,766 inpatient encounters involving patients diagnosed with diabetes across 130 U.S. hospitals and integrated delivery networks. The original research problem concerns early readmission within 30 days of discharge.

Source: Clore, J., Cios, K., DeShazo, J., & Strack, B. (2014). *Diabetes 130-US Hospitals for Years 1999-2008*. UCI Machine Learning Repository. DOI: https://doi.org/10.24432/C5230J

License: CC BY 4.0. See the source page for the full dataset documentation and attribution requirements.

UCI dataset page: https://archive.ics.uci.edu/dataset/296/diabetes-130-us-hospitals-for-years-1999-2008

## What participants do on Day 1

1. Learn how a Jupyter notebook works.
2. Run and modify basic Python code.
3. Learn about variables, strings, numbers, lists, and dictionaries.
4. Import pandas and load a real clinical dataset.
5. Understand rows, columns, data types, and missing values.
6. Filter data and calculate basic summaries.
7. Make a few simple plots.
8. Investigate one small research question.

There is **no machine learning on Day 1**. The final activity is intentionally exploratory so participants can build confidence before moving to prediction/modeling in a later session.

## Setup

### Easiest option: Google Colab

1. Upload this repository to GitHub or download the ZIP.
2. Open `notebooks/01_day1_python_and_clinical_data.ipynb` in Google Colab.
3. Run the installation cell near the top of the notebook.
4. Run the data-download cell. It will retrieve the UCI dataset and create a small teaching file locally.

### Local Jupyter

```bash
pip install -r requirements.txt
jupyter notebook
```

Then open the notebook in `notebooks/`.

## Repository structure

```text
ninr-day1-diabetes-repo/
├── README.md
├── requirements.txt
├── data/
│   └── README.md
├── docs/
│   └── day1_data_dictionary.md
└── notebooks/
    ├── 01_day1_python_and_clinical_data.ipynb
    └── 01_day1_python_and_clinical_data_SOLUTIONS.ipynb
```

## Teaching note

The notebook intentionally uses plain-language prompts and short exercises. Participants should be able to complete it without prior Python experience. The same dataset can later support Day 2 machine-learning activities around readmission prediction, model evaluation, and responsible AI.
