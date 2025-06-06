import logging
from fastapi import Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
import jwt
from decouple import config
from fastapi.security import OAuth2PasswordBearer
from src.models.user_model import User
from src.models.user_model import User
from src.database.db import db
from typing import Annotated

oauth_scheme = OAuth2PasswordBearer(tokenUrl='/auth')

class AuthService:
    def __init__(self, session: AsyncSession = None):
        self.session = session

    async def get_token(self, user:User):
        return  {
            'token': await self.create_token(user),
        }

    async def create_token(self, user: User, hs: int = 2):
        logging.info("Creando token")
        data = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
        }
        encoded_jwt = jwt.encode(data, config('SECRET_KEY'), algorithm="HS256")
        logging.info("Token obtenido")
        return encoded_jwt

    async def decode_token(self, token):
        try:
            logging.info("Decodificando token")
            data = jwt.decode(token, config('SECRET_KEY'), algorithms=["HS256"])
            return data
        except jwt.ExpiredSignatureError:
            logging.error("Error al decodificar token")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except Exception as e:
            logging.error("Error al decodificar token")
            return None

    async def get_current_user(self, token: Annotated[str, Depends(oauth_scheme)], session: AsyncSession = Depends(db.get_session)):
        try:
            logging.info("Obteniendo usuario actual")
            if not token:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="No se encontró un token de autenticación",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            data = await self.decode_token(token)

            if not data:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Access Token no válido",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            user: User | None = await session.get(User, data['user_id'] )

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado",
                )
            logging.info("Usuario obtendio")

            return user
        except Exception as e:
            logging.error(f"Error al obtener usuario: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access Token no válido",
                headers={"WWW-Authenticate": "Bearer"},
            )

