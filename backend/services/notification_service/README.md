# Notification Service

Microservice to send and record notifications (email, push). This scaffold implements a simple email sender and history storage.

Features
- Send email notifications via SMTP (BackgroundTasks)
- Store notification history in a local SQLite DB (or configure PostgreSQL via DATABASE_URL)
- CRUD read/list of sent notifications

Run locally
1. Create and activate a virtualenv and install dependencies from `requirements.txt`.
2. Optionally set `DATABASE_URL` and SMTP settings in `.env` (see `app/core/config.py`).
3. Run `python create_tables.py` to create database tables.
4. Start the server: `uvicorn app.main:app --reload --host 127.0.0.1 --port 8004`.
