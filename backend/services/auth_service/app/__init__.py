"""App package for auth_service.

Keep package initialization minimal to avoid importing submodules at
import time (which can cause ModuleNotFoundError when the package is
imported as a module). Individual modules should import their
dependencies with explicit relative imports (e.g. ``from .api import auth``)
when needed.
"""

__all__ = []