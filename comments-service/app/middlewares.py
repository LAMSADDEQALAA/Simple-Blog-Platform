from fastapi import HTTPException,Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import PyJWTError
import os
import logging 


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SECRET_KEY = os.getenv("SIGNING_KEY")
ALGORITHM = os.getenv("SIGNING_ALGORITHM")

auth_scheme = HTTPBearer()

def jwt_validation(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):

    token = credentials.credentials
    if not token:
        logger.warning("Authorization token is missing")
        raise HTTPException(status_code=401, detail="Authorization token is missing")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")