from pydantic import BaseModel, Field

class MFASetupResponse(BaseModel):
    otpauth_url: str
    qr_code: str  # Base64 encoded QR image

class MFAVerifyRequest(BaseModel):
    code: str = Field(..., min_length=6, max_length=6)
    mfa_token: str | None = None  # Needed for login verification

class MFADisableRequest(BaseModel):
    code: str = Field(..., min_length=6, max_length=6)

class MFAStatusResponse(BaseModel):
    enabled: bool
