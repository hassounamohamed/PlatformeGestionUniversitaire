import sys
from pathlib import Path

# Insert service folder at front of sys.path to avoid import collision
service_dir = Path(__file__).parent
sys.path.insert(0, str(service_dir))

from app.main import app

if __name__ == "__main__":
    import uvicorn
    # Run without auto-reloader for a single stable process during development
    uvicorn.run("app.main:app", host="127.0.0.1", port=8003, reload=False)
