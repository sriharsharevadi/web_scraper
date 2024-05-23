# Retrieve STATIC_TOKEN from environment variables
import os
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from dotenv import load_dotenv

load_dotenv()

AUTH_TOKEN = os.environ.get("AUTH_TOKEN")

if AUTH_TOKEN is None:
    raise EnvironmentError("AUTH_TOKEN not found in the environment variables")

security = HTTPBearer()


def authenticate(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token != AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
