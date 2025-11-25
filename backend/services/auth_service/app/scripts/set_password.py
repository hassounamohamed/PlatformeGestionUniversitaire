import asyncio
import sys
import os

# Ensure local app packages are importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from db.session import AsyncSessionLocal
from services.auth_service import AuthService


async def main():
    email = "chef1@gmail.com"
    new_password = "Password123!"

    async with AsyncSessionLocal() as session:
        auth = AuthService(session)
        user = await auth.get_user_by_email(email)
        if not user:
            print(f"User not found: {email}")
            return

        hashed = auth.get_password_hash(new_password)
        user.hashed_password = hashed
        await session.commit()
        print(f"Password for {email} updated to: {new_password}")


if __name__ == '__main__':
    asyncio.run(main())
