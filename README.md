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
* **Gospel listener report 100% improvement, but their are only 12 listeners in total.**
* **Age group 50 & above do not have "Worsen" effect.**
* **And age group 70 & above only show Improvement, but there are only 3 reported listeners.**
* **Most of the reported listeners are from age group of 0-34.**
* **People between 0 & 49 show improvement are within 75% - 80%**
* **There is only reported listener from group 200 - 250.**
* **And Reported listener for group 50 - 69 only count to 15.**
* **People listening to musics of BPM 50 to 199 are likely to see improvement 75% of the time.**
