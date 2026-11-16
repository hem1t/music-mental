# Introduction

Performing Exploratory Data Analysis on the music and mental health dataset ([dataset link](https://www.kaggle.com/datasets/catherinerasgaitis/mxmh-survey-results)). Dataset contains 700+ surveyed data with columns indicating music genre, bpm, favorite genre, perceived result of the participants.

## How to View Report

Either visit [`src/complete_documented_pipe.ipynb`](src/complete_documented_pipe.ipynb). Or if trying to run locally use below steps.

```sh
python -m pip install -r requirements.txt

# Make your choice
python -m pip install notebook jupyterlab

# Download the dataset
python ./setup.py 

jupyter lab eda.ipynb || jupyter notebook eda.ipynb
```

## Questions to ask

1. How many percent of people claim Improvement in Mental Health?
2. Does "Effect" changes across different Mental health issues (OCD, Insomnia, Depression, Anxiety)
3. Does "Effect" changes across different genres listened?
4. "Effect" across age groups?
5. How "Effect" corelates to BPM of the Music?
