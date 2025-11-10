import importlib, sys, os
sys.path.insert(0, os.getcwd())
try:
    db = importlib.import_module('services.analytic_service.app.core.database')
    mod = importlib.import_module('services.analytic_service.app.models.statistic')
    print('ENGINE URL:', getattr(db,'engine').url)
    print('Base.metadata tables keys:', list(db.Base.metadata.tables.keys()))
    Stat = getattr(mod, 'Statistic', None)
    print('Statistic class:', Stat)
    if Stat is not None:
        print('Stat.__table__.name:', Stat.__table__.name)
        print('Stat.__table__.metadata is Base.metadata ->', Stat.__table__.metadata is db.Base.metadata)
except Exception as e:
    print('ERROR:', e)
