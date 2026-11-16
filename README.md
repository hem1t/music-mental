# Introduction

Performing Exploratory Data Analysis on the music and mental health dataset ([dataset link](https://www.kaggle.com/datasets/catherinerasgaitis/mxmh-survey-results)). Dataset contains 700+ surveyed data with columns indicating music genre, bpm, favorite genre, perceived result of the participants.

## How to View Report

Either visit [`src/complete_documented_pipe.ipynb`](src/complete_documented_pipe.ipynb). Or if trying to run locally use below steps.
TODO: Add pipeline instructions here, when done with pipeline.

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

## Conclusions

* **Effects of reported improvement is at 75.4%, which can be considered high enough.**
* **Effects are independent of mental health disorders.**
* **Except gospel listener, all show around 75 - 80% Improvement.**
* **It's hard to trust religious people, so ignore the gospel being 100%**
* **Age group 50 & above do not have "Worsen" effect.**
* **And age group 70 & above only show Improvement**
* **People between 0 & 49 show improvement are within 75% - 80%**
* **Group of 200 & above BPM listener show no effects at all.**
* **Group of 50 to 59 shows 20% of worsening effect.**
* **People listening to musics of BPM 50 to 199 are likely to see improvement 75% of the time.**
