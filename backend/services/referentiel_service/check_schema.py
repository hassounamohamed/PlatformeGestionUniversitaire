import sys
from pathlib import Path

service_dir = Path(__file__).parent
sys.path.insert(0, str(service_dir))

from sqlalchemy import inspect
from app.core.database import engine

def check_tables():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Tables dans la base: {tables}\n")
    
    for table in tables:
        print(f"=== Table: {table} ===")
        columns = inspector.get_columns(table)
        for col in columns:
            print(f"  - {col['name']}: {col['type']}")
        print()

if __name__ == "__main__":
    check_tables()
