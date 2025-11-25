import sys
from pathlib import Path

service_dir = Path(__file__).parent
sys.path.insert(0, str(service_dir))

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.matiere import Matiere
from app.schemas.matiere import MatiereRead

app = FastAPI()

@app.get("/test-matieres")
def test_matieres(db: Session = Depends(get_db)):
    try:
        matieres = db.query(Matiere).limit(5).all()
        result = []
        for m in matieres:
            result.append({
                "id": m.id,
                "nom": m.nom,
                "code": m.code,
                "niveau_id": m.niveau_id,
                "enseignant_id": m.enseignant_id
            })
        return result
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8005)
