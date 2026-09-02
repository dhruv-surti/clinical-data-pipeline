# Clinical Trials Data Pipeline

A simple ETL pipeline that extracts clinical trial data from the public ClinicalTrials.gov API, transforms it into a clean flat structure, and loads it into a PostgreSQL database.

## What it does

- **Extract**: Pulls diabetes-related clinical trial records from the ClinicalTrials.gov API (v2)
- **Transform**: Flattens deeply nested JSON into clean records, handling missing fields gracefully (e.g. observational trials with no phase, trials with unknown enrollment counts)
- **Load**: Inserts records into a PostgreSQL database, using upserts (`ON CONFLICT DO UPDATE`) so the pipeline is safe to re-run without creating duplicates or crashing

## Why this project

Built to demonstrate core data engineering skills relevant to regulated industries (pharma/healthcare), including handling messy real-world API data, data validation, and idempotent pipeline design, principles important for GxP-style compliance and audit-ready data systems.

## Tech stack

- Python (requests, psycopg2, python-dotenv)
- PostgreSQL
- ClinicalTrials.gov public API

## Project structure

```
clinical-data-pipeline/
├── extract.py       # Pulls and flattens trial data from the API
├── load.py          # Loads records into PostgreSQL (upsert logic)
├── main.py          # Runs the full pipeline end to end
├── schema.sql        # Database table definition
├── requirements.txt
└── README.md
```

## Setup

1. Clone the repo
```bash
git clone https://github.com/yourusername/clinical-data-pipeline.git
cd clinical-data-pipeline
```

2. Create a virtual environment and install dependencies
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Create a `.env` file with your database credentials
```
HOSTNAME=localhost
DB_NAME=clinical_trials
DB_USER=your_username
DB_PASSWORD=your_password
```

4. Create the database and table
```bash
psql -U your_username -c "CREATE DATABASE clinical_trials;"
psql -U your_username -d clinical_trials -f schema.sql
```

## Usage

Run the full pipeline:
```bash
python main.py
```

This extracts fresh data from the API, saves a raw JSON backup (`raw_trials.json`), and loads/updates records in PostgreSQL.

## Key design decisions

- **Idempotency**: Uses `ON CONFLICT (nct_id) DO UPDATE` so re-running the pipeline updates existing records instead of failing or duplicating data.
- **Missing data handling**: Uses `.get()` with safe defaults (e.g. `None` for missing enrollment counts) instead of crashing on incomplete API responses, avoiding false/misleading placeholder values like `0`.
- **Secrets management**: Database credentials are stored in a `.env` file, excluded from version control via `.gitignore`.

## Future improvements

- Incremental loading (only pull trials updated since last run)
- Data validation layer (flag missing required fields, duplicate IDs)
- Orchestration with Airflow (scheduled daily runs)
- dbt models for further transformation/aggregation inside the warehouse