
import sqlite3
import json

connection = sqlite3.connect("database.db")
connection.row_factory = sqlite3.Row

print("\n--- RESUME RECORDS ---")

resumes = connection.execute(
    "SELECT * FROM resumes"
).fetchall()

for resume in resumes:
    print(dict(resume))

print("\n--- RESUME ANALYSIS RECORDS ---")

analyses = connection.execute(
    "SELECT * FROM resume_analysis"
).fetchall()

for analysis in analyses:
    print(dict(analysis))
print("\n--- INTERVIEW ATTEMPTS ---")

attempts = connection.execute(
    "SELECT * FROM interview_attempts"
).fetchall()

for attempt in attempts:
    print(dict(attempt))
connection.close()
