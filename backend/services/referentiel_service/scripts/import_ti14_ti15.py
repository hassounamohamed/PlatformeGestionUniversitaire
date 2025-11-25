#!/usr/bin/env python3
import csv
import requests
from pathlib import Path

CSV_PATH = Path(r"C:\Users\GIGABYTE\Downloads\emploi_salles_matieres_enseignants_TI14_TI15.csv")
BASE = "http://127.0.0.1:8001"

if not CSV_PATH.exists():
    print("CSV file not found:", CSV_PATH)
    raise SystemExit(1)

subjects = set()
teachers = set()
rooms = set()

with CSV_PATH.open(newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        subjects.add(row.get('Matière','').strip())
        teachers.add(row.get('Enseignant','').strip())
        rooms.add(row.get('Salle','').strip())

session = requests.Session()
session.headers.update({'Content-Type': 'application/json'})

created = {'subjects': [], 'teachers': [], 'rooms': []}

# helper to post unique names, ignore duplicates (400) and print responses
def post_unique(path, name):
    url = f"{BASE}/{path}/"
    payload = {"name": name}
    try:
        r = session.post(url, json=payload, timeout=10)
        if r.status_code in (200,201):
            print(f"Created {path[:-1]}: {name}")
            return True
        elif r.status_code == 400:
            print(f"Already exists {path[:-1]}: {name}")
            return False
        else:
            print(f"Failed {path} {name}: {r.status_code} {r.text}")
            return False
    except Exception as e:
        print(f"Error posting {path} {name}:", e)
        return False

print(f"Found {len(subjects)} subjects, {len(teachers)} teachers, {len(rooms)} rooms")

for s in sorted(subjects):
    if s:
        if post_unique('matieres', s):
            created['subjects'].append(s)

for t in sorted(teachers):
    if t:
        if post_unique('enseignants', t):
            created['teachers'].append(t)

for r in sorted(rooms):
    if r:
        if post_unique('salles', r):
            created['rooms'].append(r)

print('\nImport complete.')
print('Created summary:', created)
