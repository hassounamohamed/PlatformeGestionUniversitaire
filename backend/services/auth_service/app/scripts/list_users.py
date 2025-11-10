import asyncio
import sys
import os

# Ensure local app packages are imported before global packages named 'db' or 'models'
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from db.session import AsyncSessionLocal
from sqlalchemy import select
from models.user import User

async def main():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).order_by(User.id))
        rows = result.scalars().all()
        if not rows:
            print("No users found")
            return
        print("id | email | username | role | is_active")
        for r in rows:
            print(f"{r.id} | {r.email} | {r.username} | {r.role} | {r.is_active}")

if __name__ == '__main__':
    asyncio.run(main())
