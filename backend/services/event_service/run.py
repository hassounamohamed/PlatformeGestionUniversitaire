import os
import sys

# Ensure the local service directory is first on sys.path so the local `app` package
# is imported instead of any globally installed package named `app`.
HERE = os.path.dirname(__file__)
if HERE and HERE not in sys.path:
    sys.path.insert(0, HERE)

# Import the FastAPI app from the local package
from app.main import app  # noqa: E402

__all__ = ('app',)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8005, reload=True)
