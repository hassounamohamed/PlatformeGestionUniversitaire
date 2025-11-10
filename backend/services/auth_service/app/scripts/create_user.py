import asyncio
import sys
import os

# Ensure local app packages are importable before any globally installed package named 'schemas'
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from schemas.user import UserCreate
from db.session import AsyncSessionLocal
from services.auth_service import AuthService


async def main():
    """Create a test user for local development.

    WARNING: This script is for local development only. It creates a user with a
    known password so you can log in from the frontend. Do not use in production.
    """
    email = "chef1@gmail.com"
    username = "chef1"
    full_name = "Chef 1"
    password = "Password123!"
    role = "chef_de_departement"

    async with AsyncSessionLocal() as session:
        auth = AuthService(session)
        existing = await auth.get_user_by_email(email)
        if existing:
            print(f"User already exists: id={existing.id} email={existing.email} username={existing.username} role={existing.role}")
            return

        user_data = UserCreate(
            email=email,
            username=username,
            full_name=full_name,
            password=password,
            role=role
        )

        user = await auth.create_user(user_data)
        print("Created user:")
        print(f" id: {user.id}")
        print(f" email: {user.email}")
        print(f" username: {user.username}")
        print(f" role: {user.role}")
        print("Use the password:", password)


if __name__ == '__main__':
    asyncio.run(main())
