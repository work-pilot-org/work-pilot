from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.infrastructure.database.session import get_db
from src.modules.auth.schemas import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
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


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=200,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
) -> LoginResponse:
    """
    Authenticate a user and return a JWT access token.
    """
    return auth_service.login(
        db=db,
        request=request,
    )

@router.post("/swagger-login", include_in_schema=False)
def swagger_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> LoginResponse:
    """
    Hidden endpoint just for Swagger UI's Authorize button to work.
    Swagger UI sends Form Data, so we map it to our JSON Request here.
    """
    request = LoginRequest(email=form_data.username, password=form_data.password)
    return auth_service.login(db=db, request=request)

from src.core.dependencies import get_current_user_and_set_schema

@router.get(
    "/me",
    status_code=200,
)
def get_current_user_info(
    current_user_payload: dict = Depends(get_current_user_and_set_schema),
):
    """
    Test endpoint to verify the JWT and schema switching dependency!
    """
    return {
        "message": "Successfully authenticated and switched schema!",
        "your_jwt_data": current_user_payload,
    }