# Absence Service

Microservice for managing student absences, justificatifs and rattrapage sessions.

Features
- CRUD for Absence, Rattrapage, Justificatif
- Simple status management for absences (e.g., pending, validated, rejected)

Run locally
1. Create and activate a Python venv and install dependencies from `requirements.txt`.
2. Optionally set `DATABASE_URL` in `.env` (defaults to sqlite local file).
3. Run `python create_tables.py` to create database tables.
4. Start the server: `uvicorn app.main:app --reload --host 127.0.0.1 --port 8003`.
