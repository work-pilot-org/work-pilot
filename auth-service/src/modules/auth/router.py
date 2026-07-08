from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.infrastructure.database.session import get_db
from src.modules.auth.schemas import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
    SSOExchangeRequest,
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


from fastapi import Response, Request, HTTPException

@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=200,
)
def login(
    request: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
) -> LoginResponse:
    """
    Authenticate a user and return a JWT access token. Sets refresh token as HttpOnly cookie.
    """
    login_response, refresh_token = auth_service.login(
        db=db,
        request=request,
    )
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True, 
        samesite="none",
        max_age=7 * 24 * 60 * 60, # 7 days
    )
    
    return login_response

@router.post("/sso-exchange")
def sso_exchange(
    request: SSOExchangeRequest,
    response: Response,
    db: Session = Depends(get_db),
) -> dict:
    """
    Exchange a short-lived SSO token for an HttpOnly refresh token cookie on the current domain.
    """
    refresh_token = auth_service.exchange_sso_token(db=db, sso_token=request.sso_token)
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=7 * 24 * 60 * 60,
    )
    
    return {"message": "SSO exchange successful"}

@router.post("/swagger-login", include_in_schema=False)
def swagger_login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> LoginResponse:
    """
    Hidden endpoint just for Swagger UI's Authorize button to work.
    """
    request = LoginRequest(email=form_data.username, password=form_data.password)
    login_response, refresh_token = auth_service.login(db=db, request=request)
    return login_response

@router.post("/refresh", response_model=LoginResponse)
def refresh_token_endpoint(
    request: Request,
    db: Session = Depends(get_db),
) -> LoginResponse:
    """
    Refresh the access token using the HttpOnly refresh token cookie.
    """
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing.")
        
    try:
        return auth_service.refresh_access_token(db=db, refresh_token=refresh_token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/logout")
def logout(response: Response):
    """
    Clear the refresh token cookie.
    """
    response.delete_cookie(key="refresh_token", httponly=True, secure=True, samesite="none")
    return {"message": "Logged out successfully"}

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