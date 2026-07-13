from fastapi import APIRouter, Depends, Response, HTTPException, Request
from sqlalchemy.orm import Session
from uuid import UUID

from src.infrastructure.database.session import get_db
from src.core.dependencies import get_current_user_and_set_schema
from src.modules.mfa.schemas import (
    MFASetupResponse,
    MFAVerifyRequest,
    MFADisableRequest,
    MFAStatusResponse,
)
from src.modules.mfa.service import MFAService
from src.modules.auth.schemas import LoginResponse

router = APIRouter(
    prefix="/mfa",
    tags=["MFA"],
)

mfa_service = MFAService()

@router.post("/setup", response_model=MFASetupResponse)
def setup_mfa(
    db: Session = Depends(get_db),
    current_user_payload: dict = Depends(get_current_user_and_set_schema),
) -> MFASetupResponse:
    """
    Generate a TOTP secret and a QR code for setting up MFA.
    """
    user_id = UUID(current_user_payload.get("sub"))
    result = mfa_service.setup_mfa(db, user_id)
    return MFASetupResponse(
        otpauth_url=result["otpauth_url"],
        qr_code=result["qr_code"]
    )

@router.post("/verify", response_model=LoginResponse | dict)
def verify_mfa(
    request: MFAVerifyRequest,
    req: Request,
    response: Response,
    db: Session = Depends(get_db),
) -> LoginResponse | dict:
    """
    Verify a TOTP code during either setup or login.
    """
    from jose import jwt, JWTError
    from src.core.config import settings

    current_user_id = None
    auth_header = req.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=[settings.ALGORITHM]
            )
            sub_val = payload.get("sub")
            if sub_val:
                current_user_id = UUID(sub_val)
        except JWTError:
            pass

    result = mfa_service.verify_mfa(
        db=db,
        code=request.code,
        mfa_token=request.mfa_token,
        current_user_id=current_user_id
    )

    if result is None:
        return {"message": "MFA verified and enabled successfully."}

    # Otherwise it was a login verification returning tokens
    login_response, refresh_token = result
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True, 
        samesite="none",
        max_age=7 * 24 * 60 * 60, # 7 days
    )
    return login_response

@router.post("/disable")
def disable_mfa(
    request: MFADisableRequest,
    db: Session = Depends(get_db),
    current_user_payload: dict = Depends(get_current_user_and_set_schema),
):
    """
    Disable MFA by verifying the current code.
    """
    user_id = UUID(current_user_payload.get("sub"))
    mfa_service.disable_mfa(db, user_id, request.code)
    return {"message": "MFA disabled successfully."}

@router.get("/status", response_model=MFAStatusResponse)
def get_mfa_status(
    db: Session = Depends(get_db),
    current_user_payload: dict = Depends(get_current_user_and_set_schema),
) -> MFAStatusResponse:
    """
    Get the MFA configuration status of the user.
    """
    user_id = UUID(current_user_payload.get("sub"))
    enabled = mfa_service.get_mfa_status(db, user_id)
    return MFAStatusResponse(enabled=enabled)
