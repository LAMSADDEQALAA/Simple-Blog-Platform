from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
from jwt import PyJWTError
import os
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("SIGNING_KEY")
ALGORITHM = os.getenv("SIGNING_ALGORITHM")

class JWTValidationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.auth_scheme = HTTPBearer()

    async def dispatch(self, request: Request, call_next):
        try:
            credentials: HTTPAuthorizationCredentials = await self.auth_scheme(request)
            token = credentials.credentials
            
            if not token:
                logger.warning("Authorization token is missing")
                raise HTTPException(status_code=401, detail="Authorization token is missing")

            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.state.user = payload

        except HTTPException as http_exc:
            raise http_exc
        except PyJWTError as e:
            logger.error(f"Invalid token: {e}")
            raise HTTPException(status_code=401, detail="Invalid token")
        except Exception as e:
            logger.exception("Unexpected error in JWT validation")
            raise HTTPException(status_code=401, detail="Unauthorized")

        response = await call_next(request)
        return response
