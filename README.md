# Introduction

## How to View Report

Either visit `src/complete_documented_pipe.ipynb`. Or if trying to run locally use below steps.

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
4. What age group benefited the most?
5. How "Effect" corelates to BPM of the Music?