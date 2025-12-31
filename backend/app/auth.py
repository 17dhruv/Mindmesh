"""Simplified authentication."""

import uuid
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .database import get_db, User
from .config import settings

security = HTTPBearer()


async def get_user_from_token(token: str, db: AsyncSession) -> Optional[User]:
    """Get user from JWT token, creating if doesn't exist."""
    try:
        # Decode JWT without audience validation (Supabase tokens have specific audience claims)
        payload = jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            options={"verify_aud": False}  # Skip audience validation
        )
        user_id = payload.get("sub")
        if not user_id:
            return None

        # Try to get existing user
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()

        # If user doesn't exist, create them from JWT payload
        if not user:
            email = payload.get("email")
            if email:
                # Create new user from Supabase auth data
                user = User(
                    id=user_id,
                    email=email,
                    full_name=payload.get("user_metadata", {}).get("full_name") or email.split("@")[0],
                    created_at=datetime.utcnow()
                )
                db.add(user)
                await db.commit()
                await db.refresh(user)

        return user
    except (JWTError, Exception) as e:
        print(f"Error decoding token: {e}")
        return None


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get current authenticated user."""
    user = await get_user_from_token(credentials.credentials, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return user


# Export functions
__all__ = ["get_current_user"]