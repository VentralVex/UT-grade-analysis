"""Download UT grade distributions from the public Tableau dashboard's CSV export.

URL filters: academic year, term, all prefixes (empty Course Prefix = no filter), and
p.select grade letter detail=1 (expanded +/- grades; default export collapses them).
Output matches the dashboard's manual crosstab download (UTF-16 TSV), e.g. data/grades/fall2024.csv.
"""
import io, os, sys, urllib.parse, urllib.request
import pandas as pd

BASE = "https://iq-analytics.austin.utexas.edu/views/Gradedistributiondashboard/Externaldashboard-Crosstab.csv"
COLS = ['Semester', 'Section Number', 'Course Prefix', 'Course Number', 'Course Title', 'Course',
        'Letter Grade', 'Count of letter grade', 'Department/Program']
OUT = os.path.join(os.path.dirname(__file__), '..', 'data', 'grades')

def fetch(year_span, term):
    q = urllib.parse.urlencode({'Academic Year Span': year_span, 'c.semester select': term,
                                'Course Prefix': '', 'p.select grade letter detail': 1})
    with urllib.request.urlopen(f"{BASE}?{q}", timeout=600) as r:
        body = r.read()
    if not body.strip():  # term not in the dashboard (data begins Summer 2011)
        return pd.DataFrame()
    return pd.read_csv(io.BytesIO(body), thousands=',', dtype={'Course Number': str})

for start in range(2010, 2026):
    for term in ['Fall', 'Spring', 'Summer']:
        cal_year = start if term == 'Fall' else start + 1
        path = os.path.join(OUT, f"{term.lower()}{cal_year}.csv")
        if os.path.exists(path):
            continue
        df = fetch(f"{start}-{start + 1}", term)
        print(term, cal_year, len(df), 'rows', flush=True)
        if len(df):
            df[COLS].to_csv(path, sep='\t', encoding='utf-16', index=False)
