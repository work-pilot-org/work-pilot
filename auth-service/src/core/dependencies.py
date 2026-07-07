from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from src.core.config import settings
from src.infrastructure.database.session import get_db
from src.infrastructure.database.tenant_session import set_tenant_schema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/swagger-login")

def get_current_user_and_set_schema(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> dict:
    """
    Validates the JWT token, extracts the schema_name, 
    and sets the PostgreSQL search path to that schema.
    Returns the decoded token payload.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the JWT token
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        
        # Extract the schema_name
        schema_name: str = payload.get("schema_name")
        if schema_name is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception

    # Switch the database schema for the remainder of this request!
    set_tenant_schema(db, schema_name)
    
    return payload
