from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.orm import Session

from src.core.exceptions import UnauthorizedException
from src.core.security import verify_access_token
from src.infrastructure.database.session import get_db
from src.infrastructure.database.schema import set_schema

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):

    token = credentials.credentials

    payload = verify_access_token(token)

    if payload is None:
        raise UnauthorizedException()

    schema_name = payload.get("schema_name")

    if schema_name:
        set_schema(
            db=db,
            schema_name=schema_name,
        )

    return payload
