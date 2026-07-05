from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.infrastructure.database.session import get_db
from src.modules.auth.schemas import (
    RegisterRequest,
    RegisterResponse,
)
from src.modules.auth.service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

auth_service = AuthService()


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=201,
)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
) -> RegisterResponse:
    """
    Register a new company along with its first organization admin.
    """
    return auth_service.register(
        db=db,
        request=request,
    )