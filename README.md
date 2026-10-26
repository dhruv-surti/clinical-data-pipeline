<div align="center">
  <h1>Clinical Trials Idempotent ETL Pipeline</h1>
  <p><strong>End-to-End Data Pipeline: Python, PostgreSQL, REST APIs, and dbt</strong></p>
</div>

<hr>

<h3>Why I Built This</h3>
<p>Working with live healthcare APIs often means dealing with deeply nested JSON formats and missing fields. For data teams in regulated industries, pipelines must be reliable, repeatable, and heavily tested to prevent data corruption or duplication.</p>

<p>I built this automated ETL pipeline to extract live diabetes clinical trial records directly from the <strong>ClinicalTrials.gov REST API (v2)</strong>, flatten the complex JSON structures, and safely load them into a PostgreSQL database. To ensure the data is analytics-ready and reliable, I integrated <strong>dbt (data build tool)</strong> for modular modeling and automated data quality testing.</p>

<hr>

<h3>How the Pipeline Works</h3>
<pre>
[ClinicalTrials.gov API (REST v2)] 
       │
       ▼ (Python: extract.py & load.py)
   [JSON Parsing & Safe Defaults]
       │
       ▼ (psycopg2: Idempotent ON CONFLICT DO UPDATE)
[PostgreSQL Database] 
       │
       ▼ (dbt run & dbt test)
[Staging & Mart Models]
</pre>

<hr>

<h3>Key Engineering Decisions</h3>

<h4>1. Defensive Data Extraction (Python)</h4>
<p>Healthcare data APIs are notoriously inconsistent. I engineered a Python ingestion script (<code>extract.py</code>) using the <code>requests</code> library to pull over 1,000+ live records. To prevent the pipeline from crashing on missing keys, I implemented defensive parsing using <code>.get()</code> with safe defaults when flattening the highly nested JSON responses.</p>

<h4>2. Idempotent Data Loading (PostgreSQL)</h4>
<p>Pipelines should be safe to run multiple times without duplicating data or failing. Using <code>psycopg2</code> in my <code>load.py</code> script, I populated the PostgreSQL database using transactional upsert logic. By implementing <code>ON CONFLICT (nct_id) DO UPDATE</code>, the pipeline guarantees 100% idempotent and corruption-free data loads. Re-running the pipeline simply updates existing trial records with new API data.</p>

<h4>3. Automated Data Quality & Modeling (dbt)</h4>
<p>Instead of running raw SQL scripts for analytics, I integrated <strong>dbt</strong> to build a modern transformation layer. I constructed modular staging and mart models, and implemented <strong>4 automated test suites</strong>. These tests continuously validate strict data integrity checks, such as primary key uniqueness and null-value monitoring.</p>

<h4>4. Secure Secrets Management</h4>
<p>Security is paramount when handling database connections. All PostgreSQL database credentials and environment variables are securely stored in a <code>.env</code> file (via <code>python-dotenv</code>) and strictly excluded from version control.</p>

<hr>

<h3>Repository Structure</h3>
<ul>
  <li><code>main.py</code>: The master orchestration script that runs the extraction and loading processes.</li>
  <li><code>extract.py</code>: Handles the REST API connection and defensive JSON flattening.</li>
  <li><code>load.py</code>: Manages the PostgreSQL connection and executes the idempotent upsert logic.</li>
  <li><code>/dbt/</code>: Contains the dbt project, including staging models, mart models, and the automated YAML test suites.</li>
</ul>
