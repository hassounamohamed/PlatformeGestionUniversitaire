import importlib, os, sys, json
from fastapi.testclient import TestClient

# Ensure project root on path
proj_root = os.getcwd()
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

services = [
    'absence_service',
    'analytic_service',
    'emploi_service',
    'event_service',
    'messaging_service',
    'notification_service',
]

results = {}

for svc in services:
    print('\n=== Testing', svc, '===')
    try:
        try:
            # Try the standard package import first
            mod = importlib.import_module(f"services.{svc}.app.main")
            app = getattr(mod, 'app')
        except Exception:
            # Fall back: temporarily add the service folder to sys.path and import as top-level "app"
            svc_dir = os.path.join(proj_root, 'services', svc)
            svc_app_dir = os.path.join(svc_dir, 'app')
            if not os.path.isdir(svc_app_dir):
                raise
            # Insert service folder so `import app` resolves to this service's app package
            sys.path.insert(0, svc_dir)
            # Backup any existing app modules to avoid clobbering
            existing_app_keys = [k for k in list(sys.modules.keys()) if k == 'app' or k.startswith('app.')]
            existing_apps = {k: sys.modules[k] for k in existing_app_keys}
            try:
                app_mod = importlib.import_module('app.main')
                app = getattr(app_mod, 'app')
            finally:
                # Clean up: remove inserted path and remove the temporary app package modules so next service can import cleanly
                try:
                    sys.path.remove(svc_dir)
                except ValueError:
                    pass
                # Remove any modules that start with 'app' added by this import
                for key in list(sys.modules.keys()):
                    if key == 'app' or key.startswith('app.'):
                        # if it was present before, restore; otherwise delete
                        if key in existing_apps:
                            sys.modules[key] = existing_apps[key]
                        else:
                            del sys.modules[key]
        client = TestClient(app)

        # root
        r = client.get('/')
        print('GET / ->', r.status_code, r.json())

        # service-specific POSTs
        if svc == 'absence_service':
            payload = {"etudiant_id": 1, "emploi_id": None, "motif": "sick", "statut": "pending"}
            r = client.post('/absences/', json=payload)
            print('POST /absences/ ->', r.status_code, r.json() if r.status_code < 500 else r.text)

        elif svc == 'analytic_service':
            payload = {"name": "attendance_rate", "value": 95.5, "details": '{"class":"A"}'}
            r = client.post('/analytics/', json=payload)
            print('POST /analytics/ ->', r.status_code, r.json() if r.status_code < 500 else r.text)

        elif svc == 'emploi_service':
            # create salle first
            salle = {"code": "S200", "type": "classroom", "capacite": 40}
            r1 = client.post('/salles/', json=salle)
            print('POST /salles/ ->', r1.status_code, r1.json() if r1.status_code < 500 else r1.text)
            salle_id = r1.json().get('id') if r1.status_code == 200 else 1
            emploi = {"date": "2025-11-11", "heure_debut": "09:00:00", "heure_fin": "11:00:00", "salle_id": salle_id}
            r2 = client.post('/emplois/', json=emploi)
            print('POST /emplois/ ->', r2.status_code, r2.json() if r2.status_code < 500 else r2.text)

        elif svc == 'event_service':
            payload = {"titre": "Conférence IA", "type": "conference", "date": "2025-12-01T09:00:00Z", "description": "Talk"}
            r = client.post('/events/', json=payload)
            print('POST /events/ ->', r.status_code, r.json() if r.status_code < 500 else r.text)

        elif svc == 'messaging_service':
            payload = {"id_expediteur": 1, "id_destinataire": 2, "contenu": "Hello"}
            r = client.post('/messages/', json=payload)
            print('POST /messages/ ->', r.status_code, r.json() if r.status_code < 500 else r.text)

        elif svc == 'notification_service':
            payload = {"to": "test@example.com", "subject": "Hi", "body": "Test", "type": "email"}
            r = client.post('/notifications/', json=payload)
            print('POST /notifications/ ->', r.status_code, r.json() if r.status_code < 500 else r.text)

        results[svc] = 'ok'
    except Exception as e:
        print('ERROR testing', svc, e)
        results[svc] = f'error: {e}'

print('\nSummary:')
for k, v in results.items():
    print(k, v)
