from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
from jwt import PyJWTError
import os

SECRET_KEY = os.getenv("SIGNING_KEY")
ALGORITHM = os.getenv("SIGNING_ALGORITHM")

class JWTValidationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.auth_scheme = HTTPBearer()

    async def dispatch(self, request: Request, call_next):
        credentials: HTTPAuthorizationCredentials = await self.auth_scheme(request)
        token = credentials.credentials
        
        if not token:
            raise HTTPException(status_code=403, detail="Authorization token is missing")
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.state.user = payload
        except PyJWTError:
            raise HTTPException(status_code=403, detail="Invalid token")
        
        response = await call_next(request)
        return response
