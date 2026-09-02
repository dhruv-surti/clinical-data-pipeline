from extract import extract_trials
from load import load_trials

trials_data = extract_trials()
records_data = load_trials(trials_data)

print(f"Pipeline complete: {records_data} records loaded")