"""Custom application exceptions."""
from typing import Optional


class AppException(Exception):
    """Base application exception."""

    def __init__(
        self,
        status_code: int = 500,
        detail: str = "Internal server error",
        error_code: str = "INTERNAL_ERROR",
        headers: Optional[dict] = None,
    ):
        self.status_code = status_code
        self.detail = detail
        self.error_code = error_code
        self.headers = headers
        super().__init__(self.detail)


class ValidationError(AppException):
    """Validation error."""

    def __init__(self, detail: str = "Validation error", **kwargs):
        super().__init__(
            status_code=422,
            detail=detail,
            error_code="VALIDATION_ERROR",
            **kwargs,
        )


class NotFoundError(AppException):
    """Resource not found error."""

    def __init__(self, resource: str = "Resource", **kwargs):
        super().__init__(
            status_code=404,
            detail=f"{resource} not found",
            error_code="NOT_FOUND",
            **kwargs,
        )


class UnauthorizedError(AppException):
    """Unauthorized access error."""

    def __init__(self, detail: str = "Unauthorized", **kwargs):
        super().__init__(
            status_code=401,
            detail=detail,
            error_code="UNAUTHORIZED",
            **kwargs,
        )


class ForbiddenError(AppException):
    """Forbidden access error."""

    def __init__(self, detail: str = "Forbidden", **kwargs):
        super().__init__(
            status_code=403,
            detail=detail,
            error_code="FORBIDDEN",
            **kwargs,
        )


class ConflictError(AppException):
    """Resource conflict error."""

    def __init__(self, detail: str = "Resource conflict", **kwargs):
        super().__init__(
            status_code=409,
            detail=detail,
            error_code="CONFLICT",
            **kwargs,
        )


class RateLimitError(AppException):
    """Rate limit exceeded error."""

    def __init__(self, detail: str = "Rate limit exceeded", **kwargs):
        super().__init__(
            status_code=429,
            detail=detail,
            error_code="RATE_LIMIT_EXCEEDED",
            **kwargs,
        )


class ExternalServiceError(AppException):
    """External service error."""

    def __init__(self, service: str = "Service", **kwargs):
        super().__init__(
            status_code=503,
            detail=f"{service} is unavailable",
            error_code="SERVICE_UNAVAILABLE",
            **kwargs,
        )
