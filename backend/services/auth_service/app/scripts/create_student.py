import asyncio
import sys
import os

# Ensure local app packages are importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from schemas.user import UserCreate
from db.session import AsyncSessionLocal
from services.auth_service import AuthService


async def main():
    email = "student1@example.com"
    username = "student1"
    full_name = "Student One"
    password = "Student123!"
    role = "etudiant"

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
        print("Created student user:")
        print(f" id: {user.id}")
        print(f" email: {user.email}")
        print(f" username: {user.username}")
        print(f" role: {user.role}")
        print("Use the password:", password)


if __name__ == '__main__':
    asyncio.run(main())
