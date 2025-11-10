import importlib
import os
import sys
from sqlalchemy import inspect

# Ensure project root (current working directory) is on sys.path
proj_root = os.getcwd()
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

services = [
    'analytic_service',
    'messaging_service',
    'notification_service',
]

for svc in services:
    try:
        cfg_mod = importlib.import_module(f"services.{svc}.app.core.config")
        db_mod = importlib.import_module(f"services.{svc}.app.core.database")
        engine = getattr(db_mod, 'engine')
        url = getattr(cfg_mod, 'settings').DATABASE_URL
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"{svc} | DATABASE_URL={url}\nTables: {tables}\n")
    except Exception as e:
        print(f"{svc} | ERROR: {e}\n")
