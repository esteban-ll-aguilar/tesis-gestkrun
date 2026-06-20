from fastapi import HTTPException
from fastapi.responses import JSONResponse
from starlette.requests import Request


class AppException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_type: str = "about:blank",
        errors: list | None = None,
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.error_type = error_type
        self.errors = errors


class NotFoundException(AppException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=404, detail=detail, error_type="not-found")


class UnauthorizedException(AppException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(status_code=401, detail=detail, error_type="unauthorized")


class ForbiddenException(AppException):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(status_code=403, detail=detail, error_type="forbidden")


class ConflictException(AppException):
    def __init__(self, detail: str = "Conflict"):
        super().__init__(status_code=409, detail=detail, error_type="conflict")


class ValidationException(AppException):
    def __init__(self, detail: str = "Validation error", errors: list | None = None):
        super().__init__(
            status_code=422, detail=detail, error_type="validation-error", errors=errors
        )


class DomainException(AppException):
    def __init__(self, detail: str):
        super().__init__(status_code=422, detail=detail, error_type="domain-error")


async def exception_handler(request: Request, exc: AppException):
    body = {
        "type": exc.error_type,
        "title": "error",
        "status": exc.status_code,
        "detail": exc.detail,
    }
    if exc.errors:
        body["errors"] = exc.errors
    return JSONResponse(status_code=exc.status_code, content=body)
