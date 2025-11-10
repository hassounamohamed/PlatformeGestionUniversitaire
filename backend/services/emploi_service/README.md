# Emploi Service

Microservice for managing room schedules, timetables and absences.

Features
- CRUD for Salle, EmploiTemps (schedule entries) and Absence
- Conflict detection when creating EmploiTemps (same salle/enseignant/groupe overlap)
- Simple create_tables utility

Run locally
1. Create a virtualenv and install requirements from `requirements.txt`.
2. Set `DATABASE_URL` in `.env` if you want to override the default.
3. Run `python create_tables.py` to create tables.
4. Run `uvicorn app.main:app --reload --host 127.0.0.1 --port 8002` to start the server.
