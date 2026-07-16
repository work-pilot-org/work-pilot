from fastapi import Depends
from fastapi import Header

from sqlalchemy.orm import Session

from src.core.exceptions import UnauthorizedException
from src.core.security import verify_access_token
from src.infrastructure.database.session import get_db
from src.infrastructure.database.schema import set_schema


def get_current_user(
    authorization: str = Header(...),
    db: Session = Depends(get_db),
):

    if not authorization.startswith("Bearer "):
        raise UnauthorizedException()

    token = authorization.replace("Bearer ", "")

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
