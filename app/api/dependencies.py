from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from app.infrastructure.repositories.database import Session
from app.infrastructure.services.auth_service import oauth2_schema
from app.settings.config import config
from app.domain.models.User import UsuarioModel

class TokenData(BaseModel):
    user_id: Optional[str] = None

async def get_session() -> Generator: # type: ignore
    session: AsyncSession = Session()

    try:
        yield session
    finally:
        await session.close()

def create_credential_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível autenticar a credencial",
        headers={"WWW-Authenticate": "Bearer"}
    )

async def decode_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(
            token,
            config.JWT_SECRET,
            algorithms=[config.ALGORITHM],
            options={"verify_aud": False}
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise create_credential_exception()
        return TokenData(user_id=str(user_id))
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except jwt.InvalidTokenError:
        raise create_credential_exception()

async def get_current_user(db: AsyncSession = Depends(get_session), token: str = Depends(oauth2_schema)) -> UsuarioModel:
    token_data = await decode_token(token)
    query = select(UsuarioModel).filter(UsuarioModel.id == token_data.user_id)
    result = await db.execute(query)
    user = result.scalars().one_or_none()
    if user is None:
        raise create_credential_exception()
    return user