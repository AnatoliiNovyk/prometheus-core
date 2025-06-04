"""
Re-export the FastAPI app from api.server
"""
import sys
from pathlib import Path

# Додаємо кореневу директорію проекту до PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from api.server import app

__all__ = ['app'] 