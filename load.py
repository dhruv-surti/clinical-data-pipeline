#psycopg2
'''This is the python library that lets your script talk to postgres, 
connect to the database
create a cursor 
execute your sql commands 
Commit (save) the changes
close the connection
'''
import os 
from dotenv import load_dotenv
import psycopg2
import json


load_dotenv()

def load_trials(all_trials):

    conn = psycopg2.connect(
        host = os.getenv("HOSTNAME"),
        database = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD")

    )

    cursor = conn.cursor()

    print("Connection Successful")


 

    for trial in all_trials:
        cursor.execute(
            """
            INSERT INTO TRIALS (nct_id, title, status, conditions, sponsor, phase, enrollment_count)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (nct_id) DO UPDATE SET
                title = EXCLUDED.title,
                status = EXCLUDED.status,
                conditions = EXCLUDED.conditions,
                sponsor = EXCLUDED.sponsor,
                phase = EXCLUDED.phase,
                enrollment_count = EXCLUDED.enrollment_count
                ;

            """,

            (
                trial["nct_id"],
                trial["title"],
                trial["status"],
                trial["conditions"],
                trial["sponsor"],
                trial["phase"],
                trial["enrollment_count"]
            )
        )
    
    conn.commit() 
    cursor.close()

    conn.close()

    return len(all_trials)
