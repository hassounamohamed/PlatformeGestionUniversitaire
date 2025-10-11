from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.user import User
from schemas.user import UserCreate, TokenData
from config import settings
import logging

# Configuration de la sécurité
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Vérifie si le mot de passe correspond au hash"""
        # Truncate to bcrypt's 72 byte limit (work on UTF-8 bytes)
        if not isinstance(plain_password, str):
            plain_password = str(plain_password)
        truncated = plain_password.encode("utf-8", errors="ignore")[:72].decode("utf-8", errors="ignore")
        return pwd_context.verify(truncated, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash un mot de passe"""
        # Ensure password doesn't exceed bcrypt's 72 byte limit by truncating
        # on UTF-8 encoded bytes (bcrypt truncates to 72 bytes)
        if not isinstance(password, str):
            password = str(password)
        truncated = password.encode("utf-8", errors="ignore")[:72].decode("utf-8", errors="ignore")
        return pwd_context.hash(truncated)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Récupère un utilisateur par son email"""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalars().first()

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Récupère un utilisateur par son username"""
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalars().first()

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Récupère un utilisateur par son ID"""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalars().first()

    async def create_user(self, user_data: UserCreate) -> User:
        """Crée un nouvel utilisateur"""
        hashed_password = self.get_password_hash(user_data.password)

        db_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            role=getattr(user_data, "role", "etudiant"),
            is_active=True,
            is_superuser=False
        )

        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)

        # Log to console / application logger that the user has been created
        try:
            self.logger.info(
                "Utilisateur créé: id=%s email=%s username=%s",
                db_user.id,
                db_user.email,
                db_user.username,
            )
        except Exception:
            # Fallback to print if logging configuration isn't set
            print(f"Utilisateur créé: id={db_user.id} email={db_user.email} username={db_user.username}")

        return db_user

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authentifie un utilisateur"""
        user = await self.get_user_by_email(email)

        if not user:
            return None

        if not self.verify_password(password, user.hashed_password):
            return None

        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Crée un token JWT"""
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        return encoded_jwt

    @staticmethod
    async def get_current_user(
            token: str = Depends(oauth2_scheme)
    ) -> dict:
        """Récupère l'utilisateur actuel à partir du token"""
        from db.session import get_db

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Impossible de valider les informations d'identification",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email: str = payload.get("sub")
            user_id: int = payload.get("id")

            if email is None or user_id is None:
                raise credentials_exception

            token_data = TokenData(email=email, id=user_id)

        except JWTError:
            raise credentials_exception

        # Créer une session temporaire pour vérifier l'utilisateur
        from db.session import AsyncSessionLocal
        async with AsyncSessionLocal() as db:
            auth_service = AuthService(db)
            user = await auth_service.get_user_by_email(email=token_data.email)

            if user is None:
                raise credentials_exception

            return {"id": user.id, "email": user.email, "username": user.username}

    async def update_user(self, user_id: int, user_data: UserCreate) -> Optional[User]:
        """Met à jour un utilisateur"""
        user = await self.get_user_by_id(user_id)

        if not user:
            return None

        if user_data.email:
            user.email = user_data.email
        if user_data.username:
            user.username = user_data.username
        if user_data.full_name:
            user.full_name = user_data.full_name
        if user_data.password:
            user.hashed_password = self.get_password_hash(user_data.password)
        # Update role if provided
        if getattr(user_data, "role", None):
            user.role = user_data.role

        user.updated_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def delete_user(self, user_id: int) -> bool:
        """Supprime un utilisateur"""
        user = await self.get_user_by_id(user_id)

        if not user:
            return False

        await self.db.delete(user)
        await self.db.commit()

        return True