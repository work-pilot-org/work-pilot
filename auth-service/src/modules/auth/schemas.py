from enum import Enum

from pydantic import BaseModel, EmailStr, Field, field_validator




class RegisterRequest(BaseModel):
    company_name: str = Field(
        ...,
        min_length=2,
        max_length=255
    )

    full_name: str = Field(
        ...,
        min_length=2,
        max_length=255
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        max_length=128
    )

    confirm_password: str


    @field_validator("confirm_password")
    @classmethod
    def validate_passwords(cls, value, info):
        password = info.data.get("password")

        if password != value:
            raise ValueError("Passwords do not match.")

        return value


class RegisterResponse(BaseModel):
    message: str
    tenant_id: int
    company_name: str
    domain: str