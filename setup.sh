# /usr/bin/env sh

# .data folder is used to store data files, including the cleaned data file and logs.
mkdir .data

# Python setup
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

# Do you want to run the dashboard? (y/n)
read -p "Do you want to run the dashboard? (y/n): " run_dashboard
if [ "$run_dashboard" = "y" ]; then
    streamlit run dashboard/main.py
fi
