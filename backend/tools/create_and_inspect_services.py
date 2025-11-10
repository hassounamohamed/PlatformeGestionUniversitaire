import importlib, os, sys
from sqlalchemy import inspect

proj_root = os.getcwd()
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

services = ['analytic_service','messaging_service','notification_service']

for svc in services:
    print('---', svc, '---')
    try:
        db_mod = importlib.import_module(f"services.{svc}.app.core.database")
        cfg_mod = importlib.import_module(f"services.{svc}.app.core.config")
        engine = getattr(db_mod, 'engine')
        Base = getattr(db_mod, 'Base')
        url = getattr(cfg_mod, 'settings').DATABASE_URL
        print('ENGINE URL:', url)
        inspector = inspect(engine)
        before = inspector.get_table_names()
        print('Before tables:', before)
        # Import models so they register on Base.metadata when necessary
        try:
            if svc == 'analytic_service':
                importlib.import_module('services.analytic_service.app.models.statistic')
            elif svc == 'messaging_service':
                importlib.import_module('services.messaging_service.app.models.message')
            elif svc == 'notification_service':
                # notification uses absolute 'app' imports internally; import via service package
                importlib.import_module('services.notification_service.app.models.notification')
        except Exception:
            pass
        Base.metadata.create_all(bind=engine)
        inspector = inspect(engine)
        after = inspector.get_table_names()
        print('After tables:', after)
    except Exception as e:
        print('ERROR:', e)
    print()
