from datetime import datetime, timedelta
from jose import jwt
from app.config import settings

def create_access_token(data: dict):
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(hours=6)
    payload.update({"exp": expire})
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
