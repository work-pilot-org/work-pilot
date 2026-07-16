from fastapi import HTTPException, status


class UnauthorizedException(HTTPException):

    def __init__(self):

        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )


class ForbiddenException(HTTPException):

    def __init__(self):

        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )


class NotFoundException(HTTPException):

    def __init__(self, detail: str = "Resource not found"):

        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


class BadRequestException(HTTPException):

    def __init__(self, detail: str):

        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )
