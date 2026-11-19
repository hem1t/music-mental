# setup.ps1

# .data folder is used to store data files, including the cleaned data file and logs.
mkdir .data

# Python setup
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

# Do you want to run the dashboard?
$runDashboard = Read-Host "Do you want to run the dashboard? (y/n)"

if ($runDashboard -eq "y") {
    streamlit run dashboard/main.py
}
