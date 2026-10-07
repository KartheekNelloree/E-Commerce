import os
from typing import Any, Dict, Optional

import httpx
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from .database import get_db
from .models import User

security = HTTPBearer(auto_error=False)


def _get_dev_user() -> Dict[str, Any]:
    return {
        'id': 'dev-user-id',
        'auth0_user_id': 'dev-user-auth0',
        'name': 'Demo Customer',
        'email': 'demo@example.com',
        'role': 'customer',
    }


def _ensure_user(db: Session, payload: Dict[str, Any]) -> Dict[str, Any]:
    email = payload.get('email') or payload.get('https://example.com/email')
    user_id = payload.get('sub')
    if not email:
        raise HTTPException(status_code=401, detail='Missing user email in token payload')
    if not user_id:
        raise HTTPException(status_code=401, detail='Missing user identifier in token')

    user = db.query(User).filter(User.auth0_user_id == user_id).first()
    email_owner = db.query(User).filter(User.email == email).first()
    if email_owner and email_owner.auth0_user_id != user_id:
        raise HTTPException(status_code=409, detail='Email is already linked to another account')
    if user is None:
        user = User(
            auth0_user_id=user_id,
            name=payload.get('name') or email.split('@')[0],
            email=email,
            role='customer',
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        user.name = payload.get('name') or user.name
        user.email = email
        db.commit()

    return {
        'id': user.id,
        'auth0_user_id': user.auth0_user_id,
        'name': user.name,
        'email': user.email,
        'role': user.role,
    }


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db),
) -> Dict[str, Any]:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Missing bearer token')

    token = credentials.credentials
    dev_mode = os.getenv('DEV_MODE', 'true').lower() == 'true'
    if dev_mode and token == 'dev-token':
        return _get_dev_user()

    domain = os.getenv('AUTH0_DOMAIN')
    audience = os.getenv('AUTH0_API_AUDIENCE')
    if not domain or not audience:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Auth0 is not configured')

    try:
        jwks_url = f'https://{domain}/.well-known/jwks.json'
        jwks_client = jwt.PyJWKClient(jwks_url)
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=[os.getenv('JWT_ALGORITHM', 'RS256')],
            audience=audience,
            issuer=f'https://{domain}/',
        )
    except (jwt.InvalidTokenError, jwt.PyJWKClientError, httpx.HTTPError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid or expired JWT')

    try:
        profile_response = httpx.get(
            f'https://{domain}/userinfo',
            headers={'Authorization': f'Bearer {token}'},
            timeout=5.0,
        )
        profile_response.raise_for_status()
        profile = profile_response.json()
    except httpx.HTTPError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unable to verify Auth0 profile')

    if profile.get('sub') != payload.get('sub'):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Auth0 profile does not match token')

    return _ensure_user(db, profile)


def require_admin(current_user: Dict[str, Any] = Depends(get_current_user)):
    if current_user.get('role') != 'admin':
        raise HTTPException(status_code=403, detail='Admin access required')
    return current_user
